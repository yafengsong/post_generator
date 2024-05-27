# First install the libraries:
# pip install IBM_WATSON
# pip install PYAUDIO

import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyaudio 
import wave

# specific values with our own api credentials for the Speech to text service in our Hirslanden Group on IBM Cloud
speech_to_text_apikey = "x73dIoCwdW640FhVnog_3nnYe41fr1epaaUxPzJArR-V"
speech_to_text_url = "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/29474d6b-3053-4ee1-a211-aa23fea0b458"

authenticator_stt = IAMAuthenticator(speech_to_text_apikey)
speech_to_text = SpeechToTextV1(authenticator = authenticator_stt)
speech_to_text.set_service_url(speech_to_text_url)

def record_audio(filename): 
    chunk = 1024 
    format = pyaudio.paInt16
    channels = 1 
    rate = 44100 
    record_seconds = 5

    audio = pyaudio.PyAudio()

    stream = audio.open(format=format, 
                        channels=channels, 
                        rate=rate, 
                        input=True, 
                        frames_per_buffer=chunk) 

    print("recording...")
 
    frames = [] 
    for i in range(0, int(rate / chunk * record_seconds)): 
        data = stream.read(chunk) 
        frames.append(data) 
    
    print("finished recording.")

    stream.stop_stream() 
    stream.close() 
    audio.terminate() 

    wf = wave.open(filename, 'wb') 
    wf.setnchannels(channels) 
    wf.setsampwidth(audio.get_sample_size(format)) 
    wf.setframerate(rate) 
    wf.writeframes(b''.join(frames)) 
    wf.close() 

def convert_speech_to_text(filename, language):
    # Define model based on language
    language_models = {
        "english": "en-US_BroadbandModel",
        "french": "fr-FR_BroadbandModel",
        "german": "de-DE_BroadbandModel"
    }
    
    model = language_models.get(language.lower(), "en-US_BroadbandModel")
    
    try:
        with open(filename, 'rb') as audio_file:
            result = speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/wav',
                model=model
            ).get_result()
        text = result['results'][0]['alternatives'][0]['transcript'].strip()
        return text
    except Exception as e:
        print(f"Error during speech to text conversion: {e}")
        return ""

# Test the connection
try:
    models = speech_to_text.list_models().get_result()
    print("Connection successful! Available models:")
    for model in models['models']:
        print(f" - {model['name']}")
except Exception as e:
    print(f"Connection failed: {e}")
    
# Capture audio and save it as 'audio.wav'
record_audio("audio.wav")

# Convert speech to text for different languages
languages = ["english", "french", "german"]
for language in languages:
    user_input = convert_speech_to_text("audio.wav", language)
    print(f"You said in {language}:", user_input)