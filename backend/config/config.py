import boto3
import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",  # ✅ MUST
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)