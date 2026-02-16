# app/state.py
from typing import Dict, List, Optional
from datetime import datetime
import json

class AppState:
    """Singleton class to hold application state"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.candidates_db = {}
            cls._instance.id_counter = 0
        return cls._instance
    
    def get_next_id(self) -> int:
        self.id_counter += 1
        return self.id_counter
    
    def add_candidate(self, candidate_data: dict, resume_path: str) -> dict:
        candidate_id = self.get_next_id()
        candidate = {
            'id': candidate_id,
            **candidate_data,
            'resume_path': resume_path,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.candidates_db[candidate_id] = candidate
        print(f"DEBUG - Added candidate {candidate_id}. Total: {len(self.candidates_db)}")
        return candidate
    
    def get_candidate(self, candidate_id: int) -> Optional[dict]:
        return self.candidates_db.get(candidate_id)
    
    def get_all_candidates(self) -> List[dict]:
        return list(self.candidates_db.values())
    
    def update_candidate(self, candidate_id: int, update_data: dict) -> Optional[dict]:
        if candidate_id in self.candidates_db:
            self.candidates_db[candidate_id].update(update_data)
            self.candidates_db[candidate_id]['updated_at'] = datetime.now().isoformat()
            return self.candidates_db[candidate_id]
        return None
    
    def delete_candidate(self, candidate_id: int) -> bool:
        if candidate_id in self.candidates_db:
            del self.candidates_db[candidate_id]
            print(f"DEBUG - Deleted candidate {candidate_id}. Total: {len(self.candidates_db)}")
            return True
        return False
    
    def filter_candidates(self, skill: Optional[str] = None, experience: Optional[int] = None, 
                         graduation_year: Optional[int] = None) -> List[dict]:
        results = list(self.candidates_db.values())
        print(f"DEBUG - Filtering {len(results)} candidates")
        
        if skill:
            filtered = []
            for c in results:
                try:
                    skills = c['skill_set']
                    if isinstance(skills, str):
                        skills = json.loads(skills)
                    if any(skill.lower() in s.lower() for s in skills):
                        filtered.append(c)
                except Exception as e:
                    print(f"DEBUG - Error parsing skills: {e}")
                    continue
            results = filtered
        
        if experience is not None:
            results = [c for c in results if c['years_of_experience'] >= experience]
        
        if graduation_year is not None:
            results = [c for c in results if c['graduation_year'] == graduation_year]
        
        return results
    
    def clear_all(self):
        """Clear all data (for testing)"""
        self.candidates_db.clear()
        self.id_counter = 0
        print("DEBUG - Cleared all data")

# Create a global instance
app_state = AppState()