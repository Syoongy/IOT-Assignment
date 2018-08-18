import speech_recognition as speechRecognition
import os,json,pygame
from google.cloud import texttospeech

config = open("google_credentials.json").read()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/labs/test/google_credentials.json"

def asr():
    asr = speechRecognition.Recognizer()
    speechInput = None #what the user has said
    while speechInput==None:
	with speechRecognition.Microphone() as source:
	    audio = asr.listen(source)
	
	# Speech recognition using Google Cloud Speech Recognition
	try:
	    speechInput = asr.recognize_google_cloud(audio, credentials_json=config)
	    print("You said: " + speechInput)
	except speechRecognition.UnknownValueError:
	    print("Google Speech Recognition could not understand audio\nWaiting for user to say again")
	except speechRecognition.RequestError as e:
	    print("Could not request results from Google Speech Recognition service; {0}".format(e))
	    tts("Please check that you have the microphone working, and you are connected to the internet.")
    return speechInput

def sr():
    sr = speechRecognition.Recognizer()
    speechInput = "none" #what the user has said
    with speechRecognition.Microphone() as source:
	audio = sr.listen(source)
    try:
	speechInput = sr.recognize_google_cloud(audio, credentials_json=config)
	print("You said: "+speechInput)
    except speechRecognition.UnknownValueError:
	print("Google Speech Recognition could not understand audio")
    except speechRecognition.RequestError as e:
	print("Could not request results from Google Speech Recognition service; {0}".format(e))
	tts("Please check that you have the microphone working, and you are connected to the internet.")
    return speechInput
	

def tts(text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(
	language_code='en-US',
	ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
	audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
	out.write(response.audio_content)
	pygame.mixer.init()
	pygame.mixer.music.load("output.mp3")
	print("TTS is playing: "+text)
	pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
	continue