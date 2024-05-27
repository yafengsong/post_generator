import gradio as gr
import pyperclip
from ibm_watsonx_ai.foundation_models import ModelInference



def generate(input, temperature, language_dropdown, output_dropdown):
    # Load the LLM from IBM watsonx
    model_inference = ModelInference(
        model_id="ibm/granite-20b-multilingual",
        params={
            "decoding_method": "sample",
            "max_new_tokens": 500,
            "temperature": float(temperature),
            "repetition_penalty": 1.13
        },
        credentials={
            "apikey": "OPWfU-YTtgcz3n66AyY3UtzlanrQnKzmV1AdSns1KFKQ",
            "url": "https://us-south.ml.cloud.ibm.com"
        },
        project_id="fd7e73b4-4dfe-452e-99c9-26d8bb98ae77"
    )
    generated_response = "No content generated. Please ensure the language is set to French and try again."

    if language_dropdown == "French":
        with open("test.txt", "r") as file:
            # Read the entire contents of the file
            contents = file.read()
            prompt_input = (f"write a linkedIn post in French to {input}. Use an approachable tone, ensure the language is clear and concise, "
                            f"and avoid using jargon.Use relevant hashtags and emojis to enhance engagement but ensure they are relevant and not overused."
                            f"Aim for an active tone. Please also refer to the example: {contents}")
            print(prompt_input)
            generated_response = model_inference.generate_text(prompt=prompt_input, guardrails=True)

    return generated_response

def copy_output(output):
    pyperclip.copy(output)

logo_url = "https://upload.wikimedia.org/wikipedia/de/thumb/5/5f/Privatklinikgruppe_Hirslanden_logo.svg/2560px-Privatklinikgruppe_Hirslanden_logo.svg.png"
languages = ["German", "French", "English"]
output_types = ["LinkedIn", "BeepK", "Events", "video"]

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    title_html = f"""
    <div style="display: flex; align-items: center;">
        <img src="{logo_url}" alt="Logo" style="width: 350px; height: 50px; margin-right: 10px;">
        <h1>AI-Powered Content Generator</h1>
    </div>
    """
    title = gr.HTML(value=title_html)
    language_dropdown = gr.Dropdown(choices=languages, label="Choose Target Language", value=languages[0])
    output_dropdown = gr.Dropdown(choices=output_types, label="Choose Output Type", value=output_types[0])

    temperature = gr.Slider(label="Level of Creativity", value=1, minimum=0, maximum=2, step=0.1,
                            info="A higher value promotes greater output creativity. Setting value to 0 will always get the same result given the same input.")

    input = gr.Textbox(label="Input", placeholder="Enter your name", lines=3)

    output = gr.Textbox(label="Output", lines=4)

    with gr.Row():
        greet_button = gr.Button("Generate Content")
        copy_button = gr.Button("Copy to Clipboard")

    greet_button.click(fn=generate, inputs=[input, temperature, language_dropdown, output_dropdown], outputs=output)
    copy_button.click(fn=copy_output, inputs=output)

demo.launch()
