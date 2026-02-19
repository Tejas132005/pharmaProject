from django.urls import path
from . import views

urlpatterns = [
    path('', views.UploadView.as_view(), name='upload'),
    path('results/<int:patient_id>/', views.ResultsView.as_view(), name='results'),
    path('api/assessment/<int:assessment_id>/', views.AssessmentDetailAPI.as_view(), name='assessment_detail'),
]
