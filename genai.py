import os
import gradio as gr
import pyperclip
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watsonx_ai.foundation_models import ModelInference

# IBM Watson Speech to Text credentials
speech_to_text_apikey = "x73dIoCwdW640FhVnog_3nnYe41fr1epaaUxPzJArR-V"
speech_to_text_url = "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/29474d6b-3053-4ee1-a211-aa23fea0b458"

authenticator_stt = IAMAuthenticator(speech_to_text_apikey)
speech_to_text = SpeechToTextV1(authenticator=authenticator_stt)
speech_to_text.set_service_url(speech_to_text_url)


def convert_speech_to_text(filename, language):
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


def transcribe(audio, language_dropdown):
    # Read the audio file
    with open(audio, "rb") as f:
        audio_content = f.read()

    # Save the audio content to a file
    filename = "audio.wav"
    with open(filename, "wb") as f:
        f.write(audio_content)

    # Convert speech to text
    text = convert_speech_to_text(filename, language_dropdown)

    # Delete the audio file after processing
    if os.path.exists(filename):
        os.remove(filename)

    return text


def generate(input, words, temperature, language_dropdown, content_type_dropdown):
    model_inference = ModelInference(
        model_id="meta-llama/llama-3-70b-instruct",
        params={
            "decoding_method": "sample",
            "max_new_tokens": 800,
            "temperature": float(temperature),
            "repetition_penalty": 1.1
        },
        credentials={
            "apikey": "OPWfU-YTtgcz3n66AyY3UtzlanrQnKzmV1AdSns1KFKQ",
            "url": "https://us-south.ml.cloud.ibm.com"
        },
        project_id="fd7e73b4-4dfe-452e-99c9-26d8bb98ae77"
    )
    generated_response = "Sorry, no content generated. We are still building this function. Please select other criterion."

    basic_prompt_de = f"Bitte erstellen Sie einen Social-Media-Beitrag auf der Grundlage der angegebenen Informationen: {input}. Der Beitrag sollte etwa {words} Wörter umfassen. Siehe dazu die folgenden Beispiele: \n"
    basic_prompt_en = f"Please generate a social media post based on the provided information: {input}. The post should be around {words} words. Refer to the following examples: \n"
    basic_prompt_fr = f"Veuillez créer un message pour les médias sociaux en vous basant sur les informations fournies : {input}. Le message doit comporter environ {words} mots. Voir les exemples suivants : \n"

    if language_dropdown == "French" and content_type_dropdown == "LinkedIn":
        with open("linkedin_fr.txt", "r") as file:
            contents = file.read()
            prompt_input = (basic_prompt_fr + contents + "\n Poster en français: ")
            generated_response = model_inference.generate_text(prompt=prompt_input, guardrails=True)
    elif language_dropdown == "English" and content_type_dropdown == "LinkedIn":
        with open("linkedin_en.txt", "r") as file:
            contents = file.read()
            prompt_input = (basic_prompt_en + contents + "\n Post in English: ")
            generated_response = model_inference.generate_text(prompt=prompt_input, guardrails=True)
    elif language_dropdown == "German" and content_type_dropdown == "LinkedIn":
        with open("linkedin_de.txt", "r") as file:
            contents = file.read()
            prompt_input = (basic_prompt_de + contents + "\n Post auf Deutsch: ")
            generated_response = model_inference.generate_text(prompt=prompt_input, guardrails=True)
    elif language_dropdown == "French" and content_type_dropdown == "Events":
        with open("events_fr.txt", "r") as file:
            contents = file.read()
            prompt_input = (basic_prompt_fr + contents + "\n Poster en français: ")
            generated_response = model_inference.generate_text(prompt=prompt_input, guardrails=True)
    elif language_dropdown == "English" and content_type_dropdown == "Events":
        with open("events_en.txt", "r") as file:
            contents = file.read()
            prompt_input = (basic_prompt_en + contents + "\n Post in English: ")
            generated_response = model_inference.generate_text(prompt=prompt_input, guardrails=True)
    elif language_dropdown == "German" and content_type_dropdown == "Events":
        with open("events_de.txt", "r") as file:
            contents = file.read()
            prompt_input = (basic_prompt_de + contents + "\n Post auf Deutsch: ")
            generated_response = model_inference.generate_text(prompt=prompt_input, guardrails=True)
    elif language_dropdown == "German" and content_type_dropdown == "BeeKeeper":
        with open("beekeeper_de.txt", "r") as file:
            contents = file.read()
            prompt_input = (basic_prompt_de + contents + "\n Post auf Deutsch: ")
            generated_response = model_inference.generate_text(prompt=prompt_input, guardrails=True)

    return generated_response


def copy_output(output):
    pyperclip.copy(output)


def update_input(content_type):
    if content_type == "Events":
        return """
        Allgemeine Informationen:
        Veranstaltungsart:
        Veranstaltungsort:
        Veranstaltungsdatum:
        Email:
        Link:
        """
    else:
        return ""


logo_url = "https://upload.wikimedia.org/wikipedia/de/thumb/5/5f/Privatklinikgruppe_Hirslanden_logo.svg/2560px-Privatklinikgruppe_Hirslanden_logo.svg.png"
languages = ["German", "English", "French"]
content_type = ["LinkedIn", "BeeKeeper", "Events"]

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    title_html = f"""
    <div style="display: flex; align-items: center;">
        <img src="{logo_url}" alt="Logo" style="width: 320px; height: 50px; margin-right: 10px;">
        <h1>AI-Powered Content Generator</h1>
    </div>
    """
    title = gr.HTML(value=title_html)
    language_dropdown = gr.Dropdown(choices=languages, label="Choose Target Language", value=languages[0])
    content_type_dropdown = gr.Dropdown(choices=content_type, label="Choose Content Type", value=content_type[0])

    words = gr.Slider(label="Number of Words", value=200, minimum=0, maximum=500, step=1,
                      info="Set the desired number of words for your post")

    temperature = gr.Slider(label="Level of Creativity", value=0.9, minimum=0, maximum=2, step=0.1,
                            info="A higher value promotes greater output creativity. Setting value to 0 will always get the same result given the same input.")

    audio_input = gr.Audio(type="filepath", label="Record your message")

    input_text = gr.Textbox(label="Input", placeholder="Please provide basic information", lines=3)

    output = gr.Textbox(label="Output", lines=4)

    with gr.Row():
        generate_button = gr.Button("Generate Content")
        copy_button = gr.Button("Copy to Clipboard")

    content_type_dropdown.change(fn=update_input, inputs=content_type_dropdown, outputs=input_text)
    generate_button.click(fn=generate, inputs=[input_text, words, temperature, language_dropdown, content_type_dropdown],
                       outputs=output)
    copy_button.click(fn=copy_output, inputs=output)
    audio_input.change(fn=transcribe, inputs=[audio_input, language_dropdown], outputs=input_text)

demo.launch()
