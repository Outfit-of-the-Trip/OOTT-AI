from pydantic import BaseModel
from fastapi import Form
from typing import List


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True
        
class CameraPredictIn(OurBaseModel):
    base64_image: str= Form()
    
class CameraPredictOut(OurBaseModel):
    label: str
    color: str
    
class BatchPredictIn(OurBaseModel):
    base64_images: List[str] = Form()
    recommend_type: str
    
class BatchPredictOut(OurBaseModel):
    result: bool