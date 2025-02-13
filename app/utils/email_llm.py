import google.generativeai as genai
from app.config.settings import settings

async def prepare_draft(complaint_data):
        
    
    # print(f"Analyzing sentiment for text: {extracted_text}")
    genai.configure(api_key=settings.google_gemini_api_key)

    prompt = f"""
    Act as an email assistant and generate a professional and structured email based on the following buyer complaint details:

    **Complaint Details:**
    - User ID: {complaint_data['user_id']}
    - Order ID: {complaint_data['order_id']}
    - Product ID: {complaint_data['product_id']}
    - Issue Summary: {complaint_data['issue']}
    - Image URL (if any): {complaint_data.get('image_url', 'No image uploaded')}

    The email should be formatted exactly as it would appear when sent, including line breaks, spacing, and proper email etiquette.

    **Email Format:**
    
    ---
    **Subject:** Urgent: Buyer Complaint Regarding Product Issue  

    **To:** Seller, Admin  
    **From:** Customer Support Team  

    **Body:**  

    Dear [Seller/Admin],  

    We hope this email finds you well.  

    A Buyer has reported an issue with their order, and we request your immediate attention to resolve the matter. Below are the details of the complaint:  

    **User ID:** {complaint_data['user_id']}  
    **Order ID:** {complaint_data['order_id']}  
    **Product ID:** {complaint_data['product_id']}  

    **Issue Summary:**  
    {complaint_data['issue']}  

    **Uploaded Image (if any):**  
    {complaint_data.get('image_url', 'No image uploaded')}  

    Please review the complaint and take the necessary action at the earliest. If you require any additional details, feel free to reach out.  

    Best Regards,  
    **Customer Support Team**  
    """


    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text