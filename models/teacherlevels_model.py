from pydantic import BaseModel

class TeacherLevels(BaseModel):
    teacherlevel_id: int = None
    name: str