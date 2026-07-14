from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException

from auth.deps import require_admin
from services.file_service import save_uploaded_files
from services.extraction_service import TextExtractor

from engines.code_engine import CodeEngine
from engines.code_repository_engine import CodeRepositoryEngine

router = APIRouter(
    prefix="/code",
    tags=["Code Plagiarism"]
)

code_engine = CodeEngine()
repository_engine = CodeRepositoryEngine()

@router.post("/compare")
async def compare_code(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):

    try:

        uploaded = await save_uploaded_files(file1, file2)

        path1 = uploaded["files"][0]["path"]
        path2 = uploaded["files"][1]["path"]

        code1 = TextExtractor.extract_text(path1)
        code2 = TextExtractor.extract_text(path2)

        result = code_engine.compare(code1, code2)

        return {

            "success": True,

            "mode": "Two Code Files",

            "file1": uploaded["files"][0]["original_name"],

            "file2": uploaded["files"][1]["original_name"],

            "result": result

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/paste")
async def paste_code(
    code1: str = Form(...),
    code2: str = Form(...)
):

    try:

        result = code_engine.compare(code1, code2)

        return {

            "success": True,

            "mode": "Paste Code",

            "result": result

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/upload")
async def upload_code(
    file: UploadFile = File(...)
):

    try:

        uploaded = await save_uploaded_files(file)

        path = uploaded["files"][0]["path"]

        result = repository_engine.compare(path)

        return {

            "success": True,

            "mode": "Repository Comparison",

            "uploaded_file": uploaded["files"][0]["original_name"],

            "result": result

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/documents",dependencies=[Depends(require_admin)])
def list_documents():

    return {

        "success": True,

        "documents": repository_engine.documents()

    }


@router.get("/statistics", dependencies=[Depends(require_admin)])
def statistics():

    docs = repository_engine.documents()

    return {

        "success": True,

        "total_documents": len(docs),

        "documents": docs

    }

@router.delete("/document/{filename}", dependencies=[Depends(require_admin)])
def delete_document(filename: str):

    deleted = repository_engine.delete(filename)

    return {

        "success": deleted,

        "message":

            "Deleted Successfully"

            if deleted

            else

            "File Not Found"

    }