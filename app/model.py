from typing import Annotated
from pydantic import AfterValidator, BaseModel, Field
from typing_extensions import TypedDict
from operator import add

def validate_phrase(value: str) -> str:
    value = value.lower()
    if  not value in {"preference", "declarative", "other"}:
        print("chat type validation error: ", value)
        return "other"
    return value


class PhraseClassification(BaseModel):
    phrase_type: Annotated[str,Field(description="Tipo de frase classificada."), AfterValidator(validate_phrase)]



class State(TypedDict):
    chat_type: str
    assistant_message: str
    sot_messages: list
    sot_context: str
    messages: Annotated[list, add]
    test: list

