from .cpic_guidelines import RULES, DRUG_GENE_MAPPING

class RiskEngine:
    def __init__(self, variants):
        self.variants = variants

    def predict(self, drug_name):
        drug_name = drug_name.upper().strip()
        gene = DRUG_GENE_MAPPING.get(drug_name)
        
        if not gene:
            return {
                "risk_label": "Unknown",
                "severity": "Low",
                "confidence_score": 0.0,
                "action": "Drug not supported in current database.",
                "gene": "N/A",
                "phenotype": "Unknown"
            }

        # Find variants for this gene
        gene_variants = [v for v in self.variants if v['gene'] == gene]
        
        # Logic to determine phenotype from variants (simplified for hackathon)
        phenotype = self._infer_phenotype(gene, gene_variants)
        
        rule = RULES.get(drug_name, {}).get(gene, {}).get(phenotype)
        
        if rule:
            return {
                "risk_label": rule["risk"],
                "severity": rule["severity"],
                "confidence_score": 0.95 if gene_variants else 0.5,
                "action": rule["action"],
                "gene": gene,
                "phenotype": phenotype,
                "detected_variants": gene_variants
            }
        
        return {
            "risk_label": "Safe", # Default if no risk variants found
            "severity": "Low",
            "confidence_score": 0.8,
            "action": "No specific risk variants detected for this gene.",
            "gene": gene,
            "phenotype": "Normal Metabolizer",
            "detected_variants": gene_variants
        }

    def _infer_phenotype(self, gene, variants):
        """
        Infers phenotype from variants. 
        In production, this would use a diplotype caller like Aldy or Stargazer.
        For the hackathon, we use simple rule-of-thumb inference.
        """
        if not variants:
            return "NM" # Default to Normal Metabolizer if no variants found
        
        # Example: if rs12248560 (*17) is found in CYP2C19, it might be UM
        # If rs1057910 (*3) is found in CYP2C9, it might be PM
        for v in variants:
            if v['rsid'] == 'rs12248560': return 'UM'
            if v['rsid'] == 'rs1057910': return 'PM'
            if v['rsid'] == 'rs4149056': return 'deficient'
            if v['rsid'] == 'rs1142345': return 'low'
            if v['rsid'] == 'rs1801133': return 'deficient'
        
        return "NM"
