# from app.services.complaint_service import ComplaintService
# from app.models.schemas.complaint_schema import ComplaintRequest
# # from app.models.domain.complaint import Complaint
# from app.models.domain.user import User

# class ComplaintUseCase:
#     def __init__(self, complaint_service: ComplaintService = ComplaintService()):
#         self.complaint_service = complaint_service

#     async def process_complaint(self, current_user: User, complaint: ComplaintRequest):
#         # All business logic here
#         complaint_record = await self.complaint_service.create_complaint(
#             user_id=current_user.id, 
#             issue=complaint.issue,
#             product_id=complaint.product_id,
#             image_url=complaint.image_url
#         )
#         return complaint_record