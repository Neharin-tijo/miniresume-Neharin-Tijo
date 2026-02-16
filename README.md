# Mini Resume Management API

A FastAPI-based REST API for managing candidate resumes with in-memory storage.

## Features

- Upload resumes (PDF/DOC/DOCX)
- Store candidate metadata
- Filter candidates by skill, experience, graduation year
- Get candidate by ID
- Delete candidate
- In-memory storage (no database required)

## Python Version
- Python 3.13+

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <repo-name>

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
```bash
pip install -r requirements.txt

## Running the Application
``bash
python run.py

The server will start at http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

Method	Endpoint	Description
POST	/api/candidates/	Upload new candidate with resume
GET	/api/candidates/	List all candidates (with filters)
GET	/api/candidates/{id}	Get candidate by ID
PUT	/api/candidates/{id}	Update candidate
DELETE	/api/candidates/{id}	Delete candidate
GET	/health	Health check

## Example API Requests

# Create Candidate
```bash
curl -X POST "http://localhost:8000/api/candidates/" \
  -F "full_name=John Doe" \
  -F "dob=1990-01-01" \
  -F "contact_number=+1234567890" \
  -F "contact_address=123 Main St" \
  -F "education_qualification=BSc CS" \
  -F "graduation_year=2012" \
  -F "years_of_experience=8" \
  -F 'skill_set=["Python","FastAPI"]' \
  -F "resume=@resume.pdf"

## List Candidates with Filters
```bash
# All candidates
curl "http://localhost:8000/api/candidates/"

# Filter by skill
curl "http://localhost:8000/api/candidates/?skill=Python"

# Filter by experience
curl "http://localhost:8000/api/candidates/?experience=5"

# Filter by graduation year
curl "http://localhost:8000/api/candidates/?graduation_year=2012"

## Get Candidate by ID
```bash
curl "http://localhost:8000/api/candidates/1"

## Update Candidate
```bash
curl -X PUT "http://localhost:8000/api/candidates/1" \
  -H "Content-Type: application/json" \
  -d '{"years_of_experience": 9, "skill_set": ["Python","FastAPI","Docker"]}'

## Delete Candidate
```bash
curl -X DELETE "http://localhost:8000/api/candidates/1"

## Example Response
json
{
  "id": 1,
  "full_name": "John Doe",
  "dob": "1990-01-01",
  "contact_number": "+1234567890",
  "contact_address": "123 Main St",
  "education_qualification": "BSc CS",
  "graduation_year": 2012,
  "years_of_experience": 8,
  "skill_set": ["Python", "FastAPI"],
  "resume_path": "uploads/John_Doe_20260217_123456_abc123.pdf",
  "created_at": "2026-02-17T12:34:56.789Z",
  "updated_at": "2026-02-17T12:34:56.789Z"
}

