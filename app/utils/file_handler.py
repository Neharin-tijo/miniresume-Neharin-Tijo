# app/utils/file_handler.py
import os
import aiofiles
from fastapi import UploadFile, HTTPException
from datetime import datetime
import uuid

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_resume_file(file: UploadFile, candidate_name: str) -> str:
    """Save uploaded resume file and return the file path"""
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed types: {ALLOWED_EXTENSIONS}"
        )
    
    # Check file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    await file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, 
            detail=f"File too large. Max size: {MAX_FILE_SIZE//(1024*1024)}MB"
        )
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    safe_name = "".join(c for c in candidate_name if c.isalnum() or c.isspace()).replace(" ", "_")
    filename = f"{safe_name}_{timestamp}_{unique_id}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save file
    async with aiofiles.open(file_path, "wb") as buffer:
        content = await file.read()
        await buffer.write(content)
    
    return file_path

async def delete_resume_file_async(file_path: str):
    """Delete resume file from filesystem (async version)"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"DEBUG - Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

def delete_resume_file_sync(file_path: str):
    """Delete resume file from filesystem (sync version)"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"DEBUG - Deleted file: {file_path}")
            return True
    except Exception as e:
        print(f"Error deleting file: {e}")
    return False

def get_file_url(file_path: str) -> str:
    """Get file URL from file path"""
    if file_path and os.path.exists(file_path):
        filename = os.path.basename(file_path)
        return f"/uploads/{filename}"
    return None