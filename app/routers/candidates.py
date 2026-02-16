from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from typing import Optional
import json
from datetime import datetime

# IMPORTANT: These imports must be correct
from app import crud, schemas
from app.utils import file_handler

router = APIRouter(prefix="/api/candidates", tags=["candidates"])

# ========== POST ENDPOINT ==========
@router.post("/", response_model=schemas.CandidateResponse, status_code=201)
async def create_candidate(
    full_name: str = Form(...),
    dob: str = Form(...),
    contact_number: str = Form(...),
    contact_address: str = Form(...),
    education_qualification: str = Form(...),
    graduation_year: int = Form(...),
    years_of_experience: int = Form(...),
    skill_set: str = Form(...),
    resume: UploadFile = File(...)
):
    """Upload a new candidate with resume"""
    try:
        # Parse skill_set from JSON string
        skills = json.loads(skill_set)
        if not isinstance(skills, list):
            raise ValueError("skill_set must be a JSON array")
        
        # Parse date
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Save resume file
        resume_path = await file_handler.save_resume_file(resume, full_name)
        
        # Create candidate in memory
        candidate_data = schemas.CandidateCreate(
            full_name=full_name,
            dob=dob_date,
            contact_number=contact_number,
            contact_address=contact_address,
            education_qualification=education_qualification,
            graduation_year=graduation_year,
            years_of_experience=years_of_experience,
            skill_set=skills
        )
        
        db_candidate = crud.create_candidate(candidate_data, resume_path)
        print(f"DEBUG - Created candidate: {db_candidate['id']}")  # Debug line
        
        # Format response
        return schemas.CandidateResponse(
            id=db_candidate['id'],
            full_name=db_candidate['full_name'],
            dob=datetime.strptime(db_candidate['dob'], '%Y-%m-%d').date(),
            contact_number=db_candidate['contact_number'],
            contact_address=db_candidate['contact_address'],
            education_qualification=db_candidate['education_qualification'],
            graduation_year=db_candidate['graduation_year'],
            years_of_experience=db_candidate['years_of_experience'],
            skill_set=skills,
            resume_path=db_candidate['resume_path'],
            created_at=datetime.fromisoformat(db_candidate['created_at']),
            updated_at=datetime.fromisoformat(db_candidate['updated_at']) if db_candidate.get('updated_at') else None
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid skill_set format. Must be a JSON array.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Clean up uploaded file if operation fails
        if 'resume_path' in locals():
            await file_handler.delete_resume_file_async(resume_path)
        print(f"ERROR in create_candidate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating candidate: {str(e)}")


# ========== GET ALL CANDIDATES ==========
@router.get("/", response_model=schemas.CandidateListResponse)
def list_candidates(
    skill: Optional[str] = Query(None, description="Filter by skill"),
    experience: Optional[int] = Query(None, description="Minimum years of experience"),
    graduation_year: Optional[int] = Query(None, description="Filter by graduation year"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
):
    """List all candidates with optional filters"""
    try:
        total, candidates = crud.get_candidates(
            skip=skip,
            limit=limit,
            skill=skill,
            experience=experience,
            graduation_year=graduation_year
        )
        
        print(f"DEBUG - Listing candidates: total={total}, count={len(candidates)}")  # Debug line
        
        # Format candidates for response
        formatted_candidates = []
        for c in candidates:
            formatted_candidates.append(schemas.CandidateResponse(
                id=c['id'],
                full_name=c['full_name'],
                dob=c['dob'],
                contact_number=c['contact_number'],
                contact_address=c['contact_address'],
                education_qualification=c['education_qualification'],
                graduation_year=c['graduation_year'],
                years_of_experience=c['years_of_experience'],
                skill_set=c['skill_set'],
                resume_path=c['resume_path'],
                created_at=datetime.fromisoformat(c['created_at']),
                updated_at=datetime.fromisoformat(c['updated_at']) if c.get('updated_at') else None
            ))
        
        return {"total": total, "candidates": formatted_candidates}
        
    except Exception as e:
        print(f"ERROR in list_candidates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing candidates: {str(e)}")


# ========== GET CANDIDATE BY ID ==========
@router.get("/{candidate_id}", response_model=schemas.CandidateResponse)
def get_candidate(candidate_id: int):
    """Get a specific candidate by ID"""
    try:
        candidate = crud.get_candidate(candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        print(f"DEBUG - Got candidate {candidate_id}")  # Debug line
        
        return schemas.CandidateResponse(
            id=candidate['id'],
            full_name=candidate['full_name'],
            dob=candidate['dob'],
            contact_number=candidate['contact_number'],
            contact_address=candidate['contact_address'],
            education_qualification=candidate['education_qualification'],
            graduation_year=candidate['graduation_year'],
            years_of_experience=candidate['years_of_experience'],
            skill_set=candidate['skill_set'],
            resume_path=candidate['resume_path'],
            created_at=datetime.fromisoformat(candidate['created_at']),
            updated_at=datetime.fromisoformat(candidate['updated_at']) if candidate.get('updated_at') else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in get_candidate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving candidate: {str(e)}")


# ========== UPDATE CANDIDATE ==========
@router.put("/{candidate_id}", response_model=schemas.CandidateResponse)
def update_candidate(
    candidate_id: int,
    candidate_update: schemas.CandidateUpdate
):
    """Update a candidate's information"""
    try:
        updated_candidate = crud.update_candidate(candidate_id, candidate_update)
        if not updated_candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        print(f"DEBUG - Updated candidate {candidate_id}")  # Debug line
        
        return schemas.CandidateResponse(
            id=updated_candidate['id'],
            full_name=updated_candidate['full_name'],
            dob=updated_candidate['dob'],
            contact_number=updated_candidate['contact_number'],
            contact_address=updated_candidate['contact_address'],
            education_qualification=updated_candidate['education_qualification'],
            graduation_year=updated_candidate['graduation_year'],
            years_of_experience=updated_candidate['years_of_experience'],
            skill_set=updated_candidate['skill_set'],
            resume_path=updated_candidate['resume_path'],
            created_at=datetime.fromisoformat(updated_candidate['created_at']),
            updated_at=datetime.fromisoformat(updated_candidate['updated_at'])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in update_candidate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating candidate: {str(e)}")


# ========== DELETE CANDIDATE ==========
@router.delete("/{candidate_id}", status_code=204)
def delete_candidate(candidate_id: int):
    """Delete a candidate by ID"""
    try:
        # Get candidate to delete resume file
        candidate = crud.get_candidate(candidate_id)
        
        # Delete from storage
        deleted = crud.delete_candidate(candidate_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        # Delete resume file if it exists
        if candidate and candidate.get('resume_path'):
            file_handler.delete_resume_file_sync(candidate['resume_path'])
        
        print(f"DEBUG - Deleted candidate {candidate_id}")  # Debug line
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in delete_candidate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting candidate: {str(e)}")