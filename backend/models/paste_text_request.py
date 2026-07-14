from pydantic import BaseModel, Field

class PasteTextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=20,
        max_length=20000
    )