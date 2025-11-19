from pydantic import BaseModel

class MachineCreate(BaseModel):
    machine_name: str

class Machine(MachineCreate):
    id: int
    status: str
    model_id: int

    class Config:
        from_attributes = True
