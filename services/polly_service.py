import boto3
import os

def text_to_speech(text):

    polly = boto3.client(
        "polly",
        region_name="ap-south-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Joanna"
    )

    audio_stream = response.get("AudioStream")

    if audio_stream:
        return audio_stream.read()

    return None