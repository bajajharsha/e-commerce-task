from fastapi import Depends, Response
from app.usecases.complaint_usecase import ComplaintUseCase
from app.models.schemas.complaint_schema import ComplaintCreate
from app.models.schemas.response_schema import BaseResponse

class ComplaintController:
    def __init__(self, complaint_usecase: ComplaintUseCase = Depends()):
        self.complaint_usecase = complaint_usecase

    async def file_complaint(self, complaint: ComplaintCreate, user_id: str) -> BaseResponse:
        return await self.complaint_usecase.file_complaint(complaint, user_id)
    
