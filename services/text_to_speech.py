import os
import tempfile
from google.cloud import texttospeech
from pydub.generators import Sine
from pydub import AudioSegment
from project_root import ROOT_DIR
from google.oauth2 import service_account

GOOGLE_MAX_SECTION_LENGTH=5000
GOOGLE_CREDENTIALS_PATH=os.path.join(ROOT_DIR, 'secrets/readnovel-a7ed7aaa0145.json')
# TODO: Should this path be in config file?

def SpeakChapter(chapter_dict):

    # We will return the resulting mp3 in this temporary file
    mp3_tempfile_to_return = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)

    # Generate the chapter name
    mp3_tempfile_chapter_title = SpeakSection("Chapter titled: {}".format(chapter_dict['title']))    
    
    # Produce a chapter:
    (
        # Start with the Chapter Title
        AudioSegment.from_mp3(mp3_tempfile_chapter_title.name)
        # Append a moments silence
        .append(AudioSegment.silent(duration=500))
        # Append the actual chapter text
        .append(AudioSegment.from_mp3(SpeakLongText(chapter_dict['text']).name))
        # Append another moments silence
        .append(AudioSegment.silent(duration=500))     
        # Export the result into the tempfile as an mp3
        .export(mp3_tempfile_to_return.name, format="mp3")
    )

    # Return the tempfile which is now an MP3 of our chapter
    return mp3_tempfile_to_return

def SpeakLongText(long_text, max_section_length=GOOGLE_MAX_SECTION_LENGTH):
    "Converts a full length long_text text into an mp3"

    # Split the long_text into sections small enough to TTS
    long_text_sections = SplitTextToSections(long_text, max_section_length)

    # Generate an MP3 for each section
    mp3_sections = []
    for section in long_text_sections:
        mp3_sections.append(SpeakSection(section))

    # Combine the sections into a single mp3
    mp3_long_text = Sine(300).to_audio_segment(duration=500)
    for mp3_section in mp3_sections:
        mp3_long_text = mp3_long_text.append(AudioSegment.from_mp3(mp3_section.name))

    # Clean up the section temp files
    for mp3_section in mp3_sections:
        os.unlink(mp3_section.name)

    # Return the full Mp3 (as a temporary file)
    temporary_mp3 = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
    mp3_long_text.export(temporary_mp3.name, format="mp3")

    return temporary_mp3

def SpeakSection(section_text):
    "Converts a short section text into an mp3"
    if len(section_text) > GOOGLE_MAX_SECTION_LENGTH:
        raise Exception("Section too big, text must be broken into units of ${GOOGLE_MAX_SECTION_LENGTH}")

    # Load google credentials
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH)

    # Instantiates a client
    client = texttospeech.TextToSpeechClient(credentials=credentials)

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

    temporary_mp3 = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
    temporary_mp3.write(response.audio_content)
    temporary_mp3.close()

    # Needs to be deleted later
    # TODO: What is better way to do this? Does it work without delete=False
    # Return the section mp3 (as a temporary file)
    return temporary_mp3

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
    # TODO: remove things that typically cause bad tts
    # section breaks
    # URLs
    # Long non-words
    # detect and handle acronyms nicely?

    pass