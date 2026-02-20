# CPIC-based logic and drug-gene associations

DRUG_GENE_MAPPING = {
    "CODEINE": "CYP2D6",
    "WARFARIN": "CYP2C9",
    "CLOPIDOGREL": "CYP2C19",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}

GENE_PH_MAPPING = {
    "CYP2D6": {
        "PM": "Poor Metabolizer",
        "IM": "Intermediate Metabolizer",
        "NM": "Normal Metabolizer",
        "UM": "Ultra-rapid Metabolizer"
    },
    "CYP2C19": {
        "PM": "Poor Metabolizer",
        "IM": "Intermediate Metabolizer",
        "NM": "Normal Metabolizer",
        "RM": "Rapid Metabolizer",
        "UM": "Ultra-rapid Metabolizer"
    },
    "CYP2C9": {
        "PM": "Poor Metabolizer",
        "IM": "Intermediate Metabolizer",
        "NM": "Normal Metabolizer"
    },
    "SLCO1B1": {
        "deficient": "Deficient Transporter Function",
        "low": "Decreased Transporter Function",
        "normal": "Normal Transporter Function"
    },
    "TPMT": {
        "low": "Low/Intermediate Activity",
        "deficient": "No Activity (Poor Metabolizer)",
        "normal": "Normal Activity"
    },
    "DPYD": {
        "deficient": "Deficient Metabolism (Poor)",
        "low": "Decreased Metabolism (Intermediate)",
        "normal": "Normal Metabolism"
    }
} 

RULES = {
    "CODEINE": {
        "CYP2D6": {
            "PM": {"risk": "Ineffective", "severity": "High", "action": "Avoid codeine; use alternative analgesic."},
            "UM": {"risk": "Toxic", "severity": "High", "action": "Avoid codeine; high risk of respiratory depression."},
            "NM": {"risk": "Safe", "severity": "Low", "action": "Normal therapeutic dose."},
            "IM": {"risk": "Adjust Dosage", "severity": "Medium", "action": "Use standard starting dose, monitor for efficacy."}
        }
    },
    "WARFARIN": {
        "CYP2C9": {
            "PM": {"risk": "Toxic", "severity": "High", "action": "Significant dose reduction required."},
            "IM": {"risk": "Adjust Dosage", "severity": "Medium", "action": "Lower starting dose recommended."},
            "NM": {"risk": "Safe", "severity": "Low", "action": "Standard starting dose."}
        }
    },
    "CLOPIDOGREL": {
        "CYP2C19": {
            "PM": {"risk": "Ineffective", "severity": "High", "action": "Avoid clopidogrel; use prasugrel or ticagrelor."},
            "IM": {"risk": "Adjust Dosage", "severity": "Medium", "action": "Consider alternative antiplatelet therapy."},
            "NM": {"risk": "Safe", "severity": "Low", "action": "Standard dose."}
        }
    },
    "SIMVASTATIN": {
        "SLCO1B1": {
            "deficient": {"risk": "Toxic", "severity": "High", "action": "Lower dose or alternative statin recommended (e.g., Rosuvastatin)."},
            "normal": {"risk": "Safe", "severity": "Low", "action": "Standard dose."}
        }
    },
    "AZATHIOPRINE": {
        "TPMT": {
            "low": {"risk": "Toxic", "severity": "High", "action": "Reduce dose by 90% or use alternative."},
            "normal": {"risk": "Safe", "severity": "Low", "action": "Standard dose."}
        }
    },
    "FLUOROURACIL": {
        "DPYD": {
            "deficient": {"risk": "Toxic", "severity": "High", "action": "Avoid or drastically reduce dose."},
            "normal": {"risk": "Safe", "severity": "Low", "action": "Standard dose."}
        }
    }
}
