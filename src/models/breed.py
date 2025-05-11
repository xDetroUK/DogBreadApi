from pydantic import BaseModel

class Breed(BaseModel):
    name: str
    lifespan: str  

class BreedLifespanResponse(BaseModel):
    name: str
    lifespan: str
