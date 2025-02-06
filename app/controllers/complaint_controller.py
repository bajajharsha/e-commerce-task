# from fastapi import HTTPException, status, Depends
# from app.usecases.complaint_usecase import ComplaintUseCase
# from app.models.schemas.complaint_schema import ComplaintRequest
# # from app.models.domain.complaint import Complaint
# # from models.domain.user import User

# class ComplaintController:
#     def __init__(self, complaint_usecase: ComplaintUseCase = ComplaintUseCase()):
#         self.complaint_usecase = complaint_usecase

#     async def file_complaint(self, current_user, complaint: ComplaintRequest):
#         # Delegate the complaint processing to the UseCase and return the complaint record
#         complaint_record = await self.complaint_usecase.process_complaint(current_user, complaint)
#         return complaint_record

