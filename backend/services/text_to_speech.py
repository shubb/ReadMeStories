import os
import uuid
import asyncio
import tempfile
from google.cloud import texttospeech
from pydub.generators import Sine
from pydub import AudioSegment
from project_root import ROOT_DIR
from google.oauth2 import service_account
import concurrent.futures

GOOGLE_MAX_TEXT_LENGTH=5000
GOOGLE_CREDENTIALS_PATH=os.path.join(ROOT_DIR, 'secrets/readnovel-a7ed7aaa0145.json')
MAX_CONCURRENT_GOOGLE_API_REQUESTS = 10
# TODO: Should this path be in config file?

# Load google credentials
credentials = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH)

def SpeakChapter(chapter_dict):

    # We will return the resulting mp3 in this temporary file
    mp3_tempfile_to_return = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)

    # Generate the chapter name
    mp3_tempfile_chapter_title = SpeakLongText("Chapter titled: {}".format(chapter_dict['title']))    
    
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

    mp3_tempfile_to_return.close()

    # Return the tempfile which is now an MP3 of our chapter
    return mp3_tempfile_to_return

def SpeakLongText(long_text, max_text_length=GOOGLE_MAX_TEXT_LENGTH):
    "Converts a full length long_text text into an mp3"

    # Split the long_text into short_texts small enough to TTS
    long_text_as_short_texts = SplitTextToShortTexts(long_text, max_text_length)

    
    # Allocate a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        
        # Get the event loop
        loop = asyncio.get_event_loop()
        concurrency_limit = asyncio.Semaphore(MAX_CONCURRENT_GOOGLE_API_REQUESTS)

        # NOTE: Google's text to speech library creates a TCP connection for each request but does not close it. 
        #       These even stay open in the background after the Client is de-referenced (?!). 
        #       These each use a File Descriptor, so for a large book, we hit the max file descriptors limit and crash. 
        #       Running each TTS in its own proccess guarantees that at least at the end of the chapter, all will be de-allocated. 

        # Manually create an executor so we can force it to clean up after
        with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_CONCURRENT_GOOGLE_API_REQUESTS) as executor:

            # Call to spawn a thread to generate each short text
            async def GenerateShortTextInThread(loop, short_text, temp_dir):
                async with concurrency_limit:
                    return await loop.run_in_executor(executor, SpeakShortText, short_text, temp_dir)

            # Call to generate MP3s for all the short texts (concurrently)
            async def SimultaneouslyGenerateSeveralShortTexts(loop, all_short_texts, temp_dir):
                mp3_generation_tasks = [ GenerateShortTextInThread(loop, short_text, temp_dir) for short_text in all_short_texts ]
                return await asyncio.gather(*mp3_generation_tasks)
            
            # Generate an MP3 for each short_text
            mp3s_of_short_texts = loop.run_until_complete(SimultaneouslyGenerateSeveralShortTexts(loop, long_text_as_short_texts, temp_dir))

            # Attempt to clean up all resources
            executor.shutdown(wait = True)

        # Combine the short_texts into a single mp3
        mp3_long_text = Sine(300).to_audio_segment(duration=500)
        for mp3_short_text in mp3s_of_short_texts:
            mp3_long_text = mp3_long_text.append(AudioSegment.from_mp3(mp3_short_text))

        # Return the full Mp3 (as a temporary file)
        temporary_mp3 = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        mp3_long_text.export(temporary_mp3.name, format="mp3")
        
        return temporary_mp3

    

def SpeakShortText(short_text, segment_dir):
    "Converts a short short_text text into an mp3"
    if len(short_text) > GOOGLE_MAX_TEXT_LENGTH:
        raise Exception("Text too big, text must be broken into units of ${GOOGLE_MAX_TEXT_LENGTH}")

    # Note: It would be nice to extract client initialisation from the inner loops
    #       but I don't know how that would play with async. Risk of races. 

    # Instantiates a client
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=short_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name='en-AU-Wavenet-C') #Use indian english wavenet voice for a unique sound

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        pitch=0,
        speaking_rate=1.0,
        #effects_profile_id=['headphone-class-device']
        )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    destination_filename = os.path.join(segment_dir, uuid.uuid4().hex + '.mp3')
    with open(destination_filename, 'wb+') as temporary_mp3:
        temporary_mp3.write(response.audio_content)

    # Needs to be deleted later
    # TODO: What is better way to do this? Does it work without delete=False
    # Return the short_text mp3 (as a temporary file)
    return destination_filename

def _is_blank(text):
    return text is None or text.strip() == ''

def SplitTextToShortTexts(full_text, max_text_length):

    # Split the text into paragraphs
    text_as_paragraphs = full_text.splitlines()

    # Post proccess paragraphs
    final_list = []
    for paragraph in text_as_paragraphs:
        
        # If the 'paragraph' is blank
        if _is_blank(paragraph):
            continue # Blank, leave out

        #If the paragraph is too big, split it into sentences
        if len(paragraph) > max_text_length:
            sentences = paragraph.split('.')
            for sentence in sentences:
                if _is_blank(sentence):
                    continue # Blank, leave out
                # If the sentence is too big, just truncate it. 
                if len(sentence) > max_text_length:
                    final_list.append(sentence[0:max_text_length - 10])
                else:
                    final_list.append(sentence)
        else:
            # Paragraph is small enough to append as a short_text
            final_list.append(paragraph)  

    return final_list

def CleanUpTextForTTS(full_text):
    # TODO: remove things that typically cause bad tts
    # short_text breaks
    # URLs
    # Long non-words
    # detect and handle acronyms nicely?

    pass