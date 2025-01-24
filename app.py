# IMPORTS
from tools import s3, textract, write_text_to_file, read_text_from_file, create_gpt_json, extract_json
from flask import Flask,  request
import os
import json
import assemblyai as aai

# CONFIG
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route("/transcribe_audio_file", methods=['POST'])
def transcribe_audio_file():
    try:
        if request.method != 'POST':
            raise Exception("404 not found")

        text = request.data.decode('utf-8')
        gpt_json = create_gpt_json(text)
        json_string = extract_json(gpt_json)
        json_object = json.loads(json_string)
        files = json_object["files"]
        links = [file['s3_url_full'] for file in files]

        if len(links) == 0:
            raise Exception("Invalid body")

        link = links[0]

        aai.settings.api_key = os.environ['ASSEMBLY_AI_KEY']

        transcriber = aai.Transcriber()

        audio_file = (
            link
        )

        config = aai.TranscriptionConfig()

        transcript = transcriber.transcribe(audio_file, config)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription failed: {transcript.error}")
            exit(1)
        write_text_to_file(
            transcript.text, "reponses/transcribe_audio_response")
        return transcript.text
    except Exception as e:
        return f"Caught an exception: {e}", 500


@app.route('/ping', methods=['GET'])
def ping():
    # Get the raw request data as plain text
    return "What's up"
