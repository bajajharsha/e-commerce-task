from fastapi import Depends, status, Response
from app.repositories.complaint_repository import ComplaintRepository
from app.models.schemas.complaint_schema import ComplaintCreate
from app.models.schemas.response_schema import BaseResponse 
from fastapi.responses import JSONResponse
from app.utils.email_llm import prepare_draft
from app.repositories.user_repository import UserRepository
from app.utils.gmail_api import send_email

class ComplaintService:
    def __init__(self, complaint_repo: ComplaintRepository = Depends(), user_repo: UserRepository = Depends()):
        self.complaint_repo = complaint_repo
        self.user_repo = user_repo
        

    async def file_complaint(self, complaint_data: ComplaintCreate, user_id: str) -> BaseResponse:  # Return BaseResponse instead of UserResponse
        
        complaint_data = complaint_data.model_dump()
        complaint_data["user_id"] = user_id
        complaint_data["status"] = "open"
        
        # use the repository to save the complaint
        complaint_id = await self.complaint_repo.create_complaint(complaint_data)
        
        complaint_data["complaint_id"] = complaint_id
        print(complaint_data)
        
        # based on the complaint_data, feed it to an llm to generate the email draft
        
        email_draft = await prepare_draft(complaint_data)
        
        # fetch seller and admin details
        # for seller id, use the product id to fetch the seller id
        seller_email = await self.user_repo.find_seller(complaint_data["product_id"])
        admin_emails = await self.user_repo.get_admin_emails()
        
        # response = await send_email(email_draft, seller_email, admin_emails)
        
        # send email to the particular seller and all admins

        return BaseResponse(
            data=complaint_id,
            message="Complaint Filed successfully",
            code=status.HTTP_200_OK,
            error=None
        )
        
    