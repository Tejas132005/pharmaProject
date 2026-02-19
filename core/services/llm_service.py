import os
import json
import requests
from django.conf import settings


class LLMService:
    """LLM Service using Groq API (LLaMA models via Groq Cloud)."""

    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self):
        self.api_key = getattr(settings, 'GROQ_API_KEY', None)

    def generate_explanation(self, data):
        """
        Generates clinical explanation using Groq.
        Expected data keys: gene, drug, phenotype, risk_label, detected_variants (list)
        """
        if not self.api_key:
            return {
                "summary": "LLM Service not configured. Set GROQ_API_KEY in .env",
                "biological_mechanism": "N/A",
                "clinical_impact": "N/A",
                "variant_evidence": "N/A",
                "success": False,
            }

        detected_rsids = ', '.join(
            [v.get('rsid', 'unknown') for v in data.get('detected_variants', [])]
        ) or 'None detected'

        prompt = (
            "Act as a clinical pharmacogenomics expert. "
            "Provide a structured clinical explanation for the following pharmacogenomic assessment.\n\n"
            f"Drug: {data.get('drug', 'N/A')}\n"
            f"Primary Gene: {data.get('gene', 'N/A')}\n"
            f"Inferred Phenotype: {data.get('phenotype', 'N/A')}\n"
            f"Risk Level: {data.get('risk_label', 'N/A')}\n"
            f"Detected rsIDs: {detected_rsids}\n\n"
            "Return ONLY a JSON object with exactly these four keys:\n"
            '{\n'
            '  "summary": "A concise clinical summary",\n'
            '  "biological_mechanism": "How the genetic variant affects drug metabolism or transport",\n'
            '  "clinical_impact": "What this means for the patient (toxicity, efficacy, etc.)",\n'
            '  "variant_evidence": "Mention the rsIDs and CPIC alignment notes"\n'
            '}\n\n'
            "Keep it professional, clear, and actionable. Return ONLY valid JSON, no markdown."
        )

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a clinical pharmacogenomics expert. Always respond with valid JSON only.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                "temperature": 0.3,
                "max_tokens": 1024,
            }

            response = requests.post(
                self.GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            # Parse JSON from LLM response
            sections = self._parse_json_response(content)
            sections['success'] = True
            return sections

        except requests.exceptions.RequestException as e:
            return {
                "summary": f"Groq API request failed: {str(e)}",
                "biological_mechanism": "Error in LLM generation.",
                "clinical_impact": "Error in LLM generation.",
                "variant_evidence": "Error in LLM generation.",
                "success": False,
            }
        except Exception as e:
            return {
                "summary": f"Failed to generate explanation: {str(e)}",
                "biological_mechanism": "Error in LLM generation.",
                "clinical_impact": "Error in LLM generation.",
                "variant_evidence": "Error in LLM generation.",
                "success": False,
            }

    def _parse_json_response(self, text):
        """Parse the LLM response, expecting JSON."""
        # Clean up markdown code blocks if present
        text = text.strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1] if '\n' in text else text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()

        try:
            parsed = json.loads(text)
            return {
                "summary": parsed.get("summary", ""),
                "biological_mechanism": parsed.get("biological_mechanism", ""),
                "clinical_impact": parsed.get("clinical_impact", ""),
                "variant_evidence": parsed.get("variant_evidence", ""),
            }
        except json.JSONDecodeError:
            # Fallback: use raw text as summary
            return {
                "summary": text[:300],
                "biological_mechanism": "Unable to parse structured response.",
                "clinical_impact": "Unable to parse structured response.",
                "variant_evidence": "Unable to parse structured response.",
            }
