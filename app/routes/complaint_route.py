# routes/complaint_routes.py
from fastapi import APIRouter, Depends, Response
from app.controllers.complaint_controller import ComplaintController
from app.models.schemas.complaint_schema import ComplaintCreate
from app.models.schemas.response_schema import BaseResponse
from app.utils.dependencies import RoleChecker
from app.utils.auth import get_current_user

router = APIRouter(prefix="/complaints", tags=["Complaint"])

@router.post("/", response_model=BaseResponse)
async def file_complaint(complaint: ComplaintCreate, user_id: str = Depends(get_current_user), complaint_controller: ComplaintController = Depends()):
    return await complaint_controller.file_complaint(complaint, user_id)
