import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()  

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")  

ses_client = boto3.client(
    'ses',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def send_email(to_email, subject, body):
    try:
        response = ses_client.send_email(
            Source=os.getenv("SES_VERIFIED_EMAIL"),
            Destination={"ToAddresses": [to_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}}
            }
        )
        print("Email sent! Response:", response)
        return True
    except ClientError as e:
        print("Failed to send email!", e.response['Error']['Message'])
        return False

