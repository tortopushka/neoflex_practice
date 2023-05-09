from datetime import datetime
from pydantic import BaseModel

class Cashe_add(BaseModel):
    text_of_message: str
    language_code: str
    translated_text: str
    date: datetime = datetime.now()


class Cashe_all(BaseModel):
    id: int
    date: datetime = datetime.now()
    text_of_message: str
    language_code: str
    translated_text: str

