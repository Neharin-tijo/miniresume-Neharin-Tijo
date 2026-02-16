# app/crud.py
from typing import Optional, List, Tuple
import json
from datetime import datetime

from app import schemas
from app.state import app_state  # Import the global state

def create_candidate(candidate: schemas.CandidateCreate, resume_path: str) -> dict:
    """Create a new candidate in memory"""
    candidate_data = {
        'full_name': candidate.full_name,
        'dob': candidate.dob.isoformat(),  # Store as string
        'contact_number': candidate.contact_number,
        'contact_address': candidate.contact_address,
        'education_qualification': candidate.education_qualification,
        'graduation_year': candidate.graduation_year,
        'years_of_experience': candidate.years_of_experience,
        'skill_set': json.dumps(candidate.skill_set)
    }
    return app_state.add_candidate(candidate_data, resume_path)

def get_candidate(candidate_id: int) -> Optional[dict]:
    """Get a candidate by ID"""
    candidate = app_state.get_candidate(candidate_id)
    if candidate:
        # Convert skill_set back to list
        if isinstance(candidate['skill_set'], str):
            candidate['skill_set'] = json.loads(candidate['skill_set'])
        
        # Convert date string back to date object ONLY if it's a string
        if isinstance(candidate['dob'], str):
            candidate['dob'] = datetime.strptime(candidate['dob'], '%Y-%m-%d').date()
        # If it's already a date object, leave it as is
    
    return candidate

def get_candidates(
    skip: int = 0,
    limit: int = 100,
    skill: Optional[str] = None,
    experience: Optional[int] = None,
    graduation_year: Optional[int] = None
) -> Tuple[int, List[dict]]:
    """Get all candidates with optional filters"""
    try:
        # Get all candidates first
        all_candidates = app_state.get_all_candidates()
        print(f"DEBUG CRUD - Total candidates in storage: {len(all_candidates)}")
        
        # Apply filters
        filtered = app_state.filter_candidates(skill, experience, graduation_year)
        print(f"DEBUG CRUD - After filters: {len(filtered)}")
        
        # Apply pagination
        total = len(filtered)
        paginated = filtered[skip:skip + limit]
        
        # Format each candidate for response
        formatted_candidates = []
        for candidate in paginated:
            candidate_copy = candidate.copy()
            
            # Parse skill_set if it's a string
            if isinstance(candidate_copy['skill_set'], str):
                candidate_copy['skill_set'] = json.loads(candidate_copy['skill_set'])
            
            # Parse date ONLY if it's a string
            if isinstance(candidate_copy['dob'], str):
                candidate_copy['dob'] = datetime.strptime(candidate_copy['dob'], '%Y-%m-%d').date()
            # If it's already a date object, leave it as is
            
            formatted_candidates.append(candidate_copy)
        
        return total, formatted_candidates
        
    except Exception as e:
        print(f"Error in get_candidates: {e}")
        return 0, []

def update_candidate(candidate_id: int, candidate_update: schemas.CandidateUpdate) -> Optional[dict]:
    """Update a candidate"""
    existing = app_state.get_candidate(candidate_id)
    if not existing:
        return None
    
    update_data = candidate_update.model_dump(exclude_unset=True)
    
    if "skill_set" in update_data and update_data["skill_set"] is not None:
        update_data["skill_set"] = json.dumps(update_data["skill_set"])
    
    if "dob" in update_data and update_data["dob"] is not None:
        update_data["dob"] = update_data["dob"].isoformat()
    
    updated = app_state.update_candidate(candidate_id, update_data)
    
    if updated:
        if isinstance(updated['skill_set'], str):
            updated['skill_set'] = json.loads(updated['skill_set'])
        
        if isinstance(updated['dob'], str):
            updated['dob'] = datetime.strptime(updated['dob'], '%Y-%m-%d').date()
    
    return updated

def delete_candidate(candidate_id: int) -> bool:
    """Delete a candidate"""
    return app_state.delete_candidate(candidate_id)