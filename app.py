from flask import Flask
from flask import request
from flask import render_template
from google.cloud import texttospeech
import base64

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/tts', methods=['get', 'post'])
def tts():
    # Get text area content
    content = request.values.get("content")

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=content)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Return the base 64 encoded string for blob url play and download
    return str(base64.b64encode(response.audio_content))[2:-1]


if __name__ == '__main__':
    app.run()
