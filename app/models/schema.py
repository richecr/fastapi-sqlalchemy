from pydantic import BaseModel, ConfigDict


class NoteSchema(BaseModel):
    id: int
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)
