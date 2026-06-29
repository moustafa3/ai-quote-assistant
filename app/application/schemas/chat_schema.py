from pydantic import BaseModel, Field


class ChatAskRequest(BaseModel):
    """
    API request model for asking a question over local business documents.
    """

    question: str = Field(
        ...,
        min_length=3,
        examples=["Quelle remise appliquer pour une ETI ?"],
    )


class ChatAskResponse(BaseModel):
    """
    API response model for a RAG answer.
    """

    answer: str = Field(
        ...,
        examples=["Les clients ETI bénéficient d'une remise de 10 %."],
    )
    sources: list[str] = Field(
        default_factory=list,
        examples=[["commercial_conditions.txt"]],
    )