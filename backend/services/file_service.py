import os
import uuid
from fastapi import UploadFile, HTTPException


TEMP_UPLOAD_FOLDER = "uploads"
REPOSITORY_FOLDER = "database/documents"

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".py",
    ".java",
    ".js",
    ".c",
    ".cpp"
}

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

os.makedirs(TEMP_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPOSITORY_FOLDER, exist_ok=True)


async def save_uploaded_files(*files, repository=False):

    uploaded_files = []

    destination_folder = (
        REPOSITORY_FOLDER
        if repository
        else TEMP_UPLOAD_FOLDER
    )

    for file in files:

        if file is None:
            continue

        extension = os.path.splitext(file.filename)[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {extension}"
            )

        content = await file.read()

        if len(content) == 0:
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is empty."
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} exceeds the 20 MB limit."
            )

        unique_name = f"{uuid.uuid4()}_{file.filename}"

        file_path = os.path.join(
            destination_folder,
            unique_name
        )

        with open(file_path, "wb") as f:
            f.write(content)

        uploaded_files.append({

            "original_name": file.filename,

            "stored_name": unique_name,

            "path": file_path,

            "size": len(content),

            "extension": extension

        })

    return {

        "success": True,

        "files": uploaded_files

    }