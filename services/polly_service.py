# services/polly_service.py
#
# Text-to-speech using AWS Polly.
# Voice ID and region configurable via .env.

import boto3
from backend.config.settings import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    POLLY_REGION, POLLY_VOICE_ID
)


def text_to_speech(text: str) -> bytes:
    polly = boto3.client(
        "polly",
        region_name=POLLY_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=POLLY_VOICE_ID
    )
    audio_stream = response.get("AudioStream")
    return audio_stream.read() if audio_stream else b""