from fastapi import FastAPI, UploadFile
import fasttext
import requests
import urllib.parse
import assemblyai as aai
from bs4 import BeautifulSoup
from huggingface_hub import hf_hub_download
from fastapi.middleware.cors import CORSMiddleware
# from speechbrain.pretrained import EncoderASR

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate/fr-fon")
async def translate_fr_fon(sentence: str):
  """
    Traduction d'une phrase du français en fon. \n
    En paramètre, la phrase à traduire. \n
    En retour, la phrase traduite.
  """
  sentence = urllib.parse.quote_plus(sentence)
  sentence = sentence.replace("+", "%20")

  url = f"https://translate.glosbe.com/fr-fon/{sentence}"

  page = requests.get(url)

  soup = BeautifulSoup(page.content, "html.parser")

  div = soup.find("div", class_="w-full h-full bg-gray-100 h-full border p-2 min-h-25vh sm:min-h-50vh whitespace-pre-wrap break-words")
  
  return div.text

@app.post("/translate/fon-fr")
async def translate_fon_fr(sentence: str):
  """
    Traduction d'une phrase du fon en français. \n
    En paramètre, la phrase à traduire. \n
    En retour, la phrase traduite.
  """
  sentence = urllib.parse.quote_plus(sentence)
  sentence = sentence.replace("+", "%20")

  url = f"https://translate.glosbe.com/fon-fr/{sentence}"

  page = requests.get(url)

  soup = BeautifulSoup(page.content, "html.parser")

  div = soup.find("div", class_="w-full h-full bg-gray-100 h-full border p-2 min-h-25vh sm:min-h-50vh whitespace-pre-wrap break-words")
  
  return div.text

@app.post("/audio-fon")
async def audio_fon(audio: UploadFile):
  """
   Transcrire un audio fon en texte.
  """
  API_URL = "https://api-inference.huggingface.co/models/speechbrain/asr-wav2vec2-dvoice-fongbe"
 
  headers = {"Authorization": "Bearer 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"}
  
  data = await audio.read()

  response = requests.post(API_URL, headers=headers, data=data)

  return response.json()
 

# @app.post("/translate/en-fon")
# async def translate_en_fon(sentence: str):
#   """
#     Traduction d'une phrase du anglais en fon. \n
#     En paramètre, la phrase à traduire. \n
#     En retour, la phrase traduite.
#   """
#   sentence = urllib.parse.quote_plus(sentence)
#   sentence = sentence.replace("+", "%20")

#   url = f"https://translate.glosbe.com/en-fon/{sentence}"

#   page = requests.get(url)

#   soup = BeautifulSoup(page.content, "html.parser")

#   div = soup.find("div", class_="w-full h-full bg-gray-100 h-full border p-2 min-h-25vh sm:min-h-50vh whitespace-pre-wrap break-words")
  
#   return div.text

# @app.post("/translate/fon-en")
# async def translate_fon_en(sentence: str):
#   """
#     Traduction d'une phrase du fon en anglais. \n
#     En paramètre, la phrase à traduire. \n
#     En retour, la phrase traduite.
#   """
#   sentence = urllib.parse.quote_plus(sentence)
#   sentence = sentence.replace("+", "%20")

#   url = f"https://translate.glosbe.com/fon-en/{sentence}"

#   page = requests.get(url)

#   soup = BeautifulSoup(page.content, "html.parser")

#   div = soup.find("div", class_="w-full h-full bg-gray-100 h-full border p-2 min-h-25vh sm:min-h-50vh whitespace-pre-wrap break-words")
  
#   return div.text

@app.get("/")
async def welcome():
  return {"message":"Welcome to the Saawara API. You can translate from French to Fon, Fon to French. You can also transcribe audio to text."}

