import os
import gradio as gr
import whisper
import time
from keybert import KeyBERT
from sendToSheets import sendToSheets

kw_model = KeyBERT()
model = whisper.load_model('base')

def transcribe(audio, state={}, lang=None):
    time.sleep(1)
    
    state['transcription'] = ""
    transcription = model.transcribe(audio, language=lang)
    state['transcription'] += transcription['text'] + " "
    
    text = state['transcription']
    keyword = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=None, top_n=1)

    if len(keyword) > 0 and len(text) > 0:
        sendToSheets(keyword[0][0], text)


    return state['transcription'], state, f"Detected language: {transcription['language']}", f"Detected Keyword: {keyword[0][0]}"


title = "RememberThis by Whisper4Lokal - OpenAI's Whisper hackathon"
transcription_tb = gr.Textbox(label="Transcription", lines=10, max_lines=20)
detected_lang = gr.outputs.HTML(label="Detected Language")
detected_keyword= gr.outputs.HTML(label="Detected Keyword")

state = gr.State({"transcription": ""})

gr.Interface(fn=transcribe,
    inputs=[
        gr.Audio(source="microphone", type="filepath", streaming=False),
        state,
    ],
    outputs=[
        transcription_tb,
        state,
        detected_lang,
        detected_keyword
    ],
    #live=True,
    allow_flagging='never',
    title=title,
).launch(
    # enable_queue=True,
    #debug=True
)
