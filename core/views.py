import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.utils.html import format_html
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import VCFUploadForm 
from .models import Patient, DrugAssessment 
from .services.vcf_parser import VCFParser 
from .services.risk_engine import RiskEngine
from .services.llm_service import LLMService
from .services.json_formatter import JSONFormatter


class LandingView(View):
    def get(self, request):
        return render(request, 'core/landing.html')

    def post(self, request):
        # We handle the upload logic directly on the landing page
        uploaded_file = request.FILES.get('uploaded_file')
        drug_input = request.POST.get('drugs', '')

        if not uploaded_file or not drug_input:
            return render(request, 'core/landing.html', {'error': 'Please provide both a VCF file and target medications.'})

        # Create Patient record
        patient = Patient.objects.create(
            uploaded_file=uploaded_file
        )

        drug_names = drug_input.split(',')

        # Step 1: Parse VCF
        parser = VCFParser(patient.uploaded_file.path)
        validation_ok, msg = parser.validate()
        if not validation_ok:
            return render(request, 'core/landing.html', {
                'error': msg
            })

        parsing_results = parser.parse()
        if not parsing_results['success']:
            return render(request, 'core/landing.html', {
                'error': parsing_results['error']
            })

        # Step 2: Risk Prediction & LLM Explanation
        risk_engine = RiskEngine(parsing_results['variants'])
        llm_service = LLMService()

        for drug_name in drug_names:
            drug_name = drug_name.strip()
            if not drug_name:
                continue

            prediction = risk_engine.predict(drug_name)
            prediction['drug'] = drug_name

            # Generate LLM explanation
            explanation = llm_service.generate_explanation({
                'drug': drug_name,
                'gene': prediction['gene'],
                'phenotype': prediction['phenotype'],
                'risk_label': prediction['risk_label'],
                'detected_variants': prediction.get('detected_variants', []),
            })

            # Format to Strict JSON
            final_json = JSONFormatter.format_output(
                prediction, explanation, patient.patient_id
            )

            # Save Assessment
            DrugAssessment.objects.create(
                patient=patient,
                drug_name=drug_name,
                risk_label=prediction['risk_label'],
                confidence_score=prediction['confidence_score'],
                severity=prediction['severity'],
                json_output=final_json,
            )

        return redirect('results', patient_id=patient.id)


class UploadView(View):
    def get(self, request):
        form = VCFUploadForm()
        return render(request, 'core/upload.html', {'form': form})

    def post(self, request):
        form = VCFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save()
            drug_names = form.cleaned_data['drugs'].split(',')

            # Step 1: Parse VCF
            parser = VCFParser(patient.uploaded_file.path)
            validation_ok, msg = parser.validate()
            if not validation_ok:
                return render(request, 'core/upload.html', {
                    'form': form, 'error': msg
                })

            parsing_results = parser.parse()
            if not parsing_results['success']:
                return render(request, 'core/upload.html', {
                    'form': form, 'error': parsing_results['error']
                })

            # Step 2: Risk Prediction & LLM Explanation
            risk_engine = RiskEngine(parsing_results['variants'])
            llm_service = LLMService()

            for drug_name in drug_names:
                drug_name = drug_name.strip()
                if not drug_name:
                    continue

                prediction = risk_engine.predict(drug_name)
                prediction['drug'] = drug_name

                # Generate LLM explanation
                explanation = llm_service.generate_explanation({
                    'drug': drug_name,
                    'gene': prediction['gene'],
                    'phenotype': prediction['phenotype'],
                    'risk_label': prediction['risk_label'],
                    'detected_variants': prediction.get(
                        'detected_variants', []
                    ),
                })

                # Format to Strict JSON
                final_json = JSONFormatter.format_output(
                    prediction, explanation, patient.patient_id
                )

                # Save Assessment
                DrugAssessment.objects.create(
                    patient=patient,
                    drug_name=drug_name,
                    risk_label=prediction['risk_label'],
                    confidence_score=prediction['confidence_score'],
                    severity=prediction['severity'],
                    json_output=final_json,
                )

            return redirect('results', patient_id=patient.id)

        return render(request, 'core/upload.html', {'form': form})


class ResultsView(View):
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        raw_assessments = patient.assessments.all()

        # Pre-process assessments so the template
        # never needs deep dictionary lookups or nested loops
        assessments = []
        for a in raw_assessments:
            jo = a.json_output or {}
            profile = jo.get('pharmacogenomic_profile', {})
            llm = jo.get('llm_generated_explanation', {})
            rec = jo.get('clinical_recommendation', {})
            variants = profile.get('detected_variants', [])

            # Build variant HTML table rows
            rows = []
            for v in variants:
                rows.append(
                    '<tr><td><code>{}</code></td>'
                    '<td>{}</td><td>{}</td></tr>'.format(
                        v.get('rsid', ''),
                        v.get('chromosome', ''),
                        v.get('genotype', ''),
                    )
                )

            if rows:
                table_html = (
                    '<table class="table table-sm"><thead><tr>'
                    '<th>rsID</th><th>Chromosome</th><th>Genotype</th>'
                    '</tr></thead><tbody>'
                    + ''.join(rows)
                    + '</tbody></table>'
                )
            else:
                table_html = '<p class="text-muted">No variants detected.</p>'

            # CSS class for risk badge (no spaces)
            risk_css = a.risk_label.replace(' ', '') if a.risk_label else 'Unknown'

            assessments.append({
                'id': a.id,
                'drug_name': a.drug_name,
                'risk_label': a.risk_label,
                'risk_css': risk_css,
                'gene_name': profile.get('primary_gene', 'N/A'),
                'summary': llm.get('summary', 'No summary available.'),
                'mechanism': llm.get('biological_mechanism', 'N/A'),
                'evidence': llm.get('variant_evidence', 'N/A'),
                'action': rec.get('action', 'No recommendation.'),
                'variant_table': table_html,
                'json_pretty': json.dumps(jo, indent=2),
            })

        return render(request, 'core/results.html', {
            'patient': patient,
            'assessments': assessments,
        })


class AssessmentDetailAPI(APIView):
    def get(self, request, assessment_id):
        assessment = get_object_or_404(DrugAssessment, id=assessment_id)
        return Response(assessment.json_output)
