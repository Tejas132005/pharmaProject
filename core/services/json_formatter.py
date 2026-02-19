from datetime import datetime

class JSONFormatter:
    @staticmethod
    def format_output(assessment_data, llm_data, patient_id):
        """
        Formats findings into the STRICT JSON schema required.
        """
        return {
            "patient_id": str(patient_id),
            "drug": assessment_data['drug'],
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "risk_assessment": {
                "risk_label": assessment_data['risk_label'],
                "confidence_score": assessment_data['confidence_score'],
                "severity": assessment_data['severity']
            },
            "pharmacogenomic_profile": {
                "primary_gene": assessment_data['gene'],
                "diplotype": assessment_data.get('diplotype', "*X/*Y"), # Simplified
                "phenotype": assessment_data['phenotype'],
                "detected_variants": [
                    {
                        "rsid": v['rsid'],
                        "chromosome": v['chromosome'],
                        "position": str(v['position']),
                        "genotype": v['genotype']
                    } for v in assessment_data.get('detected_variants', [])
                ]
            },
            "clinical_recommendation": {
                "action": assessment_data['action'],
                "cpic_guideline_reference": f"https://cpicpgx.org/guidelines/guideline-for-{assessment_data['drug'].lower()}/",
                "monitoring_required": assessment_data['severity'] != "Low"
            },
            "llm_generated_explanation": {
                "summary": llm_data['summary'],
                "biological_mechanism": llm_data['biological_mechanism'],
                "clinical_impact": llm_data['clinical_impact'],
                "variant_evidence": llm_data['variant_evidence']
            },
            "quality_metrics": {
                "vcf_parsing_success": True,
                "genes_detected_count": len(assessment_data.get('detected_variants', [])),
                "llm_generation_success": llm_data.get('success', False)
            }
        }
