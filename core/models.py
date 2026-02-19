from django.db import models
import uuid

class Patient(models.Model):
    patient_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    uploaded_file = models.FileField(upload_to='vcf_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Patient {self.patient_id}"

class DrugAssessment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='assessments')
    drug_name = models.CharField(max_length=100)
    risk_label = models.CharField(max_length=50) # Safe, Adjust Dosage, Toxic, Ineffective, Unknown
    confidence_score = models.FloatField()
    severity = models.CharField(max_length=50) # Low, Medium, High
    json_output = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.drug_name} assessment for {self.patient.patient_id}"
