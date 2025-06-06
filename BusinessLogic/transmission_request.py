from pydantic import BaseModel


class TransmissionRequest(BaseModel):
    message: str
    frequency: int
    speed: int
