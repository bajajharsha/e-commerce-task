from fastapi import Depends

from app.models.schemas.complaint_schema import ComplaintCreate
from app.models.schemas.response_schema import BaseResponse
from app.services.complaint_service import ComplaintService


class ComplaintUseCase:
    def __init__(self, complaint_service: ComplaintService = Depends()):
        self.complaint_service = complaint_service

    async def file_complaint(
        self, complaint_data: ComplaintCreate, user_id: str
    ) -> BaseResponse:
        return await self.complaint_service.file_complaint(complaint_data, user_id)
