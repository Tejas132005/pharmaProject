# PharmaGuard – Pharmacogenomic Risk Prediction System

**RIFT 2026 Hackathon (HealthTech Track)**

PharmaGuard is an AI-powered pharmacogenomics web application designed to help clinicians and patients understand genetic risks associated with specific medications. By parsing VCF (Variant Call Format) files and applying rule-based logic combined with LLM-powered explanations, PharmaGuard provides actionable clinical insights.

## Features
- **VCF Parsing**: Supports VCF v4.2 files (upto 5MB) for 6 critical genes (CYP2D6, CYP2C19, CYP2C9, SLCO1B1, TPMT, DPYD).
- **Risk Assessment**: Rule-based prediction (Safe, Adjust Dosage, Toxic, Ineffective, Unknown) for key drugs like Warfarin, Codeine, etc.
- **Explainable AI**: Integration with Gemini LLM to provide clinical summaries, biological mechanisms, and CPIC alignment.
- **Strict JSON Output**: Standardized clinical reporting format.
- **Modern UI**: Drag-and-drop upload and color-coded clinical results.

## Tech Stack
- **Backend**: Django, SQLite, Django REST Framework
- **Frontend**: Bootstrap 5, Vanilla JavaScript, HTML/CSS
- **AI**: Google Gemini (via `google-generativeai`)
- **Bioinformatics**: `PyVCF3`

## Architecture Overview
The application follows a modular "Services" architecture within the Django project:
- `vcf_parser.py`: Validates and extracts genetic variants.
- `risk_engine.py`: Implements CPIC-based clinical logic.
- `llm_service.py`: Interfaces with Gemini for natural language summaries.
- `cpic_guidelines.py`: Data store for pharmacogenomic associations.

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd pharma_project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Copy `.env.example` to `.env` and add your `GEMINI_API_KEY`.

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the server**:
   ```bash
   python manage.py runserver
   ```

## Sample VCF Usage
A sample VCF file is provided in `sample_vcf/`. You can upload this file to test the parsing and risk engine for genes like `CYP2D6` and `CYP2C19`.

## Deployment (Render/Vercel)
- **Render**: Connect your GitHub repo, set the build command to `pip install -r requirements.txt` and start command to `gunicorn pharmaguard.wsgi`.
- **Vercel**: Use the `vercel-python` runtime.

## API Documentation
### `POST /core/upload/`
- **Body**: `vcf_file` (File), `drugs` (Comma-separated string)
- **Response**: Detailed JSON clinical assessment.

---
*Developed for RIFT 2026 Hackathon.*
