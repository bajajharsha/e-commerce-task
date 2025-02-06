# from app.repositories.complaint_repository import ComplaintRepository
# from app.models.domain.complaint import Complaint
# from app.utils.gmail_api import send_complaint_email

# class ComplaintService:
#     def __init__(self, complaint_repo: ComplaintRepository = ComplaintRepository()):
#         self.complaint_repo = complaint_repo

#     async def create_complaint(self, user_id: str, issue: str, product_id: str, image_url: str):
#         # Create a new complaint record
#         complaint = Complaint(
#             user_id=user_id,
#             order_id="87643246889",  # Static for now
#             product_id=product_id,
#             issue=issue,
#             image_url=image_url,
#             status="open"
#         )

#         # Store the complaint in the database
#         complaint_record = await self.complaint_repo.create_complaint(complaint)

#         # Send email notifications using Gmail API
#         await send_complaint_email(
#             user_id=user_id,
#             order_id="87643246889",
#             product_id=product_id,
#             issue_summary=issue,
#             image_url=image_url
#         )

#         return complaint_record
