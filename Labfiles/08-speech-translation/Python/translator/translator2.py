from dotenv import load_dotenv
import os
from datetime import datetime
from playsound import playsound
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        # Load environment variables
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')
        
        if not ai_key or not ai_region:
            raise ValueError("API key or region is not set. Check your .env file.")

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(ai_key, ai_region)
        translation_config.speech_recognition_language = 'en-US'
        translation_config.add_target_language('fr')
        translation_config.add_target_language('es')
        translation_config.add_target_language('hi')
        print('Ready to translate from', translation_config.speech_recognition_language)

        # Configure speech
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)

        # Run translation interaction
        run_translation_interaction(translation_config)

    except Exception as ex:
        print("An error occurred:", ex)

def run_translation_interaction(translation_config):
    target_language = ''
    while True:
        target_language = input('\nEnter a target language\n fr = French\n es = Spanish\n hi = Hindi\n Enter "quit" to stop\n').lower()
        if target_language == 'quit':
            break
        if target_language in translation_config.target_languages:
            translate(target_language, translation_config)
        else:
            print("Invalid language selection.")

def translate(target_language, translation_config):
    audio_file = 'station.wav'
    if not os.path.exists(audio_file):
        print(f"The audio file {audio_file} does not exist.")
        return
    
    try:
        playsound(audio_file)
        audio_config = speech_sdk.AudioConfig(filename=audio_file)
        translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)
        print("Getting speech from file...")
        result = translator.recognize_once_async().get()
        if result.reason == speech_sdk.ResultReason.TranslatedSpeech:
            print(f'Translating "{result.text}" to {target_language}')
            translation = result.translations[target_language]
            print(translation)
        else:
            print("Translation failed: No speech detected or an error occurred.")
    except Exception as ex:
        print("Failed to translate due to:", ex)

if __name__ == "__main__":
    main()
