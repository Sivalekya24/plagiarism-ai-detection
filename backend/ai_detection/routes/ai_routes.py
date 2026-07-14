from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from fastapi import UploadFile, File, Form
import os
from ai_detection.engines.ai_engine import AIEngine
import fitz

router = APIRouter(
    prefix="/ai",
    tags=["AI Detection"]
)


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Input text for AI detection"
    )


class CodeRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        description="Input source code"
    )

    language: str = Field(
        ...,
        description="Programming language"
    )


@router.get("/health")
def health():

    return AIEngine.health()


@router.post("/text")
def detect_text(request: TextRequest):

    try:

        result = AIEngine.detect_text(
            request.text
        )

        if not result["success"]:

            raise HTTPException(
                status_code=400,
                detail=result["message"]
            )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post("/text/upload")
async def detect_text_upload(

    file: UploadFile = File(...)

):

    try:

        allowed_extensions = {

            ".txt",

            ".pdf",

            ".docx"

        }

        extension = os.path.splitext(

            file.filename

        )[1].lower()

        if extension not in allowed_extensions:

            raise HTTPException(

                status_code=400,

                detail="Unsupported file type."

            )

        # ----------------------------
        # TXT
        # ----------------------------

        if extension == ".txt":

            text = (

                await file.read()

            ).decode(

                "utf-8",

                errors="ignore"

            )

        # ----------------------------
        # PDF
        # ----------------------------

        elif extension == ".pdf":

            
            pdf = fitz.open(

                stream=await file.read(),

                filetype="pdf"

            )

            text = ""

            for page in pdf:

                text += page.get_text()

        # ----------------------------
        # DOCX
        # ----------------------------

        else:

            from io import BytesIO

            from docx import Document

            document = Document(

                BytesIO(

                    await file.read()

                )

            )

            text = "\n".join(

                paragraph.text

                for paragraph in document.paragraphs

            )

        result = AIEngine.detect_text(

            text

        )

        if not result["success"]:

            raise HTTPException(

                status_code=400,

                detail=result["message"]

            )

        return result

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


@router.post("/code")
def detect_code(request: CodeRequest):

    try:

        result = AIEngine.detect_code(
            request.code,
            request.language
        )

        if not result["success"]:

            raise HTTPException(
                status_code=400,
                detail=result["message"]
            )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post("/code/upload")
async def detect_code_upload(

    file: UploadFile = File(...),

    language: str = Form(None)

):

    try:

        allowed_extensions = {

            ".py": "Python",

            ".java": "Java",

            ".cpp": "C++",

            ".c": "C",

            ".cs": "C#",

            ".js": "JavaScript",

            ".go": "Go",

            ".php": "PHP",

            ".rs": "Rust"

        }

        extension = os.path.splitext(file.filename)[1].lower()

        if extension not in allowed_extensions:

            raise HTTPException(

                status_code=400,

                detail="Unsupported file type."

            )

        code = (

            await file.read()

        ).decode(

            "utf-8",

            errors="ignore"

        )

        if language is None:

            language = allowed_extensions[extension]

        result = AIEngine.detect_code(

            code,

            language

        )

        if not result["success"]:

            raise HTTPException(

                status_code=400,

                detail=result["message"]

            )

        return result

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )