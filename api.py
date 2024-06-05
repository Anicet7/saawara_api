from fastapi import FastAPI, UploadFile
import requests
import urllib.parse
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

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
 

@app.get("/")
async def welcome():
  return {"message":"Welcome to the Saawara API. You can translate from French to Fon, Fon to French. You can also transcribe audio to text."}

