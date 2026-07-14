from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from providers.statistics_provider import StatisticsProvider
from services.file_service import save_uploaded_files
from engines.repository_engine import RepositoryEngine
from auth.deps import require_admin
router = APIRouter(
    prefix="/repository",
    tags=["Repository"]
)

repository_engine = RepositoryEngine()
statistics_provider = StatisticsProvider()


@router.post("/upload", dependencies=[Depends(require_admin)])
async def upload_document(
    file: UploadFile = File(...),
    
):

    try:

        uploaded = await save_uploaded_files(file, repository=True)

        uploaded_path = uploaded["files"][0]["path"]

        result = repository_engine.compare_against_repository(
            uploaded_path
        )

        return {

    "success": True,

    "uploaded_file": uploaded["files"][0]["original_name"],

    "repository_size": result["repository_size"],

    "highest_similarity": result["highest_similarity"],

    "matched_document": result["matched_document"],

    "risk_level": result["risk_level"],

    "top_matches": result["matches"]

}

    except HTTPException as e:

        raise e

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/documents", dependencies=[Depends(require_admin)])
async def list_documents():

    provider = repository_engine.repository

    return {

        "repository_size": len(provider.get_all_documents()),

        "documents": provider.get_all_documents()

    }

@router.get("/statistics", dependencies=[Depends(require_admin)])
async def repository_statistics():

    return statistics_provider.get_statistics()

@router.delete("/document/{filename}", dependencies=[Depends(require_admin)])
async def delete_document(filename: str):

    import os

    path = os.path.join(
        "database/documents",
        filename
    )

    if not os.path.exists(path):

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    os.remove(path)

    return {

        "success": True,

        "message": f"{filename} deleted successfully."

    }

@router.get("/search", dependencies=[Depends(require_admin)])
async def search_repository(keyword: str):

    import os

    matches = []

    folder = "database/documents"

    for file in os.listdir(folder):

        if keyword.lower() in file.lower():

            matches.append(file)

    return {

        "keyword": keyword,

        "results": matches,

        "count": len(matches)

    }