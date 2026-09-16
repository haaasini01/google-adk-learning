from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field

class EmailContent(BaseModel):
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive"
    )
    body: str = Field(
        description="The body of the email. Should be well=formatted with proper greeting, paragraphs and signature"
    )

root_agent = LlmAgent(
    name='email_agent',
    model='gemini-3.6-flash',
    description='An Email Agent which generates professional emails with structured subject and body',
    instruction="""
    You are an Email Generation Assistant.
    Your task is to generate a professional email based on user's requests.

    GUIDELINES:
    - Create an appropriate subject line (concise and revelant)
    - Write a well-structured email body with:
        * Professional Greeting
        * Clear and concise main content
        * Appropriate closing
        * Your name as signature
    - Suggest relevant attachments if applicable (empty list if none needed)
    - Email tone should match the purpose (formal for business, friendly for colleagues)
    - Keep emails concise but complete

    IMPORTANT: Your response should be a valid JSON matching this structure:
    {
        "subject": "Subject line here",
        "body": "Email body here with proper paragraphs and formatting"
    }

    DO NOT include any additional text outsite of the JSON respone
    """,
    output_schema=EmailContent,
    output_key="email"
)
