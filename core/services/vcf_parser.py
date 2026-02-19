import vcf
import os

class VCFParser:
    REQUIRED_GENES = ['CYP2D6', 'CYP2C19', 'CYP2C9', 'SLCO1B1', 'TPMT', 'DPYD']

    def __init__(self, file_path):
        self.file_path = file_path
        self.variants = []

    def validate(self):
        """Basic validation of VCF extension and existence."""
        if not os.path.exists(self.file_path):
            return False, "File does not exist."
        if not self.file_path.endswith('.vcf'):
            return False, "Not a VCF file."
        return True, ""

    def parse(self):
        """Extracts required gene variants from VCF."""
        results = {
            "variants": [],
            "genes_detected": set(),
            "success": False,
            "error": None
        }

        try:
            vcf_reader = vcf.Reader(filename=self.file_path)
            for record in vcf_reader:
                # In a real scenario, gene info might be in the 'INFO' field or can be mapped via rsID
                # For this hackathon version, we look for 'GENE' or 'CSQ' in INFO or use rsID mapping
                gene_name = record.INFO.get('GENE', [None])[0]
                rsid = record.ID
                
                # Simple mapping if GENE tag missing (demonstration logic)
                # In production, we'd use a more robust lookup
                if not gene_name and rsid:
                    gene_name = self._lookup_gene_by_rsid(rsid)

                if gene_name in self.REQUIRED_GENES:
                    variant_info = {
                        "rsid": rsid,
                        "chromosome": record.CHROM,
                        "position": record.POS,
                        "genotype": "/".join(map(str, record.samples[0].gt_alleles)) if record.samples else "Unknown",
                        "gene": gene_name,
                        "ref": record.REF,
                        "alt": str(record.ALT[0]) if record.ALT else None
                    }
                    results["variants"].append(variant_info)
                    results["genes_detected"].add(gene_name)

            results["success"] = True
            results["genes_detected"] = list(results["genes_detected"])
        except Exception as e:
            results["error"] = str(e)
            results["success"] = False

        return results

    def _lookup_gene_by_rsid(self, rsid):
        # Placeholder for rsID -> Gene mapping
        # In a full app, this would query a local DB or API
        mapping = {
            'rs12248560': 'CYP2C19',
            'rs1057910': 'CYP2C9',
            'rs4149056': 'SLCO1B1',
            'rs1061170': 'CYP2D6',
            'rs1801133': 'DPYD',
            'rs1142345': 'TPMT',
        }
        return mapping.get(rsid)
