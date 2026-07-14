from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from services.file_service import save_uploaded_files
from services.extraction_service import TextExtractor

from engines.document_engine import DocumentEngine
from engines.repository_engine import RepositoryEngine
from engines.paste_engine import PasteEngine
from auth.deps import require_admin

from models.paste_text_request import PasteTextRequest

router = APIRouter(
    prefix="/document",
    tags=["Document Plagiarism"]
)

document_engine = DocumentEngine()
repository_engine = RepositoryEngine()
paste_engine = PasteEngine()


# ======================================================
# Compare Two Documents (Development)
# ======================================================

@router.post("/compare")
async def compare_documents(

    file1: UploadFile = File(...),
    file2: UploadFile = File(...)

):

    try:

        uploaded = await save_uploaded_files(
            file1,
            file2
        )

        path1 = uploaded["files"][0]["path"]
        path2 = uploaded["files"][1]["path"]

        text1 = TextExtractor.extract_text(path1)
        text2 = TextExtractor.extract_text(path2)

        result = document_engine.compare(
            text1,
            text2
        )

        return {

            "success": True,

            "mode": "Two Document Comparison",

            "file1": uploaded["files"][0]["original_name"],

            "file2": uploaded["files"][1]["original_name"],

            "result": result

        }

    except HTTPException as e:

        raise e

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ======================================================
# Upload One Document
# Compare Against Repository
# ======================================================

@router.post("/upload")
async def upload_document(

    file: UploadFile = File(...)

):

    try:

        uploaded = await save_uploaded_files(
            file
        )

        uploaded_path = uploaded["files"][0]["path"]

        result = repository_engine.compare_against_repository(
            uploaded_path
        )

        return {

            "success": True,

            "mode": "Repository Comparison",

            "uploaded_file": uploaded["files"][0]["original_name"],

            "repository_size": result["repository_size"],

            "highest_similarity": result["highest_similarity"],

            "matched_document": result["matched_document"],

            "risk_level": result["risk_level"],

            "matches": result["matches"],

            "message": result["message"]

        }

    except HTTPException as e:

        raise e

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ======================================================
# Paste Text
# ======================================================

@router.post("/paste")
async def paste_text(

    text: str = Form(...)

):

    try:

        result = paste_engine.check_plagiarism(text)

        return {

            "success": True,

            "mode": "Paste Text",

            "repository_size": result["repository_size"],

            "highest_similarity": result["highest_similarity"],

            "matched_document": result["matched_document"],

            "risk_level": result["risk_level"],

            "matches": result["matches"]

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )