# from fastapi import APIRouter, HTTPException, Depends, status
# from app.models.schemas.complaint_schema import ComplaintRequest
# from app.controllers.complaint_controller import ComplaintController
# from app.utils.dependencies import RoleChecker
# from app.utils.auth import get_current_user

# router = APIRouter(prefix="/complaints", tags=["Complaints"])

# @router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RoleChecker(["buyer", "admin"]))])
# async def file_complaint(
#     complaint: ComplaintRequest, 
#     current_user = Depends(get_current_user),
#     complaint_controller: ComplaintController = Depends()
# ):
#     complaint_record = await complaint_controller.file_complaint(current_user, complaint)
#     return complaint_record
