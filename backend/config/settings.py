# backend/config/settings.py
#
# Single source of truth for all configuration.
# ALL variables come from .env through here.
# No other file should use os.getenv() directly.

import os
from dotenv import load_dotenv

load_dotenv()

# ─── PDF ─────────────────────────────────────────────────────
# Training content file. Change in .env to switch courses.
PDF_PATH = os.getenv("PDF_PATH", "data/retail.pdf")

# ─── API ─────────────────────────────────────────────────────
# Backend URL. Change if deploying to a server.
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# ─── AWS Bedrock ─────────────────────────────────────────────
AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION            = os.getenv("AWS_REGION", "us-east-1")
LLAMA_GENERAL         = os.getenv("LLAMA_GENERAL", "meta.llama3-8b-instruct-v1:0")
LLAMA_CODE            = os.getenv("LLAMA_CODE", "meta.llama3-70b-instruct-v1:0")

# ─── AWS Polly ───────────────────────────────────────────────
# Text-to-speech settings. Change voice in .env anytime.
POLLY_REGION   = os.getenv("POLLY_REGION", "ap-south-1")
POLLY_VOICE_ID = os.getenv("POLLY_VOICE_ID", "Joanna")

# ─── App Behaviour ───────────────────────────────────────────
# Minimum words required before evaluation is allowed.
MIN_SUMMARY_WORDS         = int(os.getenv("MIN_SUMMARY_WORDS", "20"))
# How similar user text can be to original before flagged as copied.
COPY_SIMILARITY_THRESHOLD = float(os.getenv("COPY_SIMILARITY_THRESHOLD", "0.7"))

# ─── Quiz ────────────────────────────────────────────────────
SECTION_QUIZ_MCQ_COUNT  = int(os.getenv("SECTION_QUIZ_MCQ_COUNT", "3"))
SECTION_QUIZ_SUBJ_COUNT = int(os.getenv("SECTION_QUIZ_SUBJ_COUNT", "2"))
FINAL_QUIZ_MCQ_COUNT    = int(os.getenv("FINAL_QUIZ_MCQ_COUNT", "10"))
FINAL_QUIZ_SUBJ_COUNT   = int(os.getenv("FINAL_QUIZ_SUBJ_COUNT", "3"))