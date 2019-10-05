from google.cloud import texttospeech

class TextToSpeech:

    GOOGLE_MAX_SECTION_LENGTH=5000

    def SpeakSection(self, section_text):
        if len(section_text) > self.GOOGLE_MAX_SECTION_LENGTH:
            raise Exception("Section too big, text must be broken into units of ${self.GOOGLE_MAX_SECTION_LENGTH}")

        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=section_text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-GB',
            name='en-GB-Wavenet-A')

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3,
            pitch=-2,
            speaking_rate=1.3,
            effects_profile_id=['headphone-class-device'])

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        return response.audio_content