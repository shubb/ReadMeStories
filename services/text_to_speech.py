from google.cloud import texttospeech

GOOGLE_MAX_SECTION_LENGTH=5000

def SpeakSection(section_text):
    if len(section_text) > GOOGLE_MAX_SECTION_LENGTH:
        raise Exception("Section too big, text must be broken into units of ${GOOGLE_MAX_SECTION_LENGTH}")

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

def _is_blank(text):
    return text is None or text.strip() == ''

def SplitTextToSections(full_text, max_section_length):

    # Split the text into paragraphs
    text_as_paragraphs = full_text.splitlines()

    # Post proccess paragraphs
    final_list = []
    for paragraph in text_as_paragraphs:
        
        # If the 'paragraph' is blank
        if _is_blank(paragraph):
            continue # Blank, leave out

        #If the paragraph is too big, split it into sentences
        if len(paragraph) > max_section_length:
            sentences = paragraph.split('.')
            for sentence in sentences:
                if _is_blank(sentence):
                    continue # Blank, leave out
                # If the sentence is too big, just truncate it. 
                if len(sentence) > max_section_length:
                    final_list.append(sentence[0:max_section_length - 10])
                else:
                    final_list.append(sentence)
        else:
            # Paragraph is small enough to append as a section
            final_list.append(paragraph)  

    return final_list

def CleanUpTextForTTS(full_text):
    pass