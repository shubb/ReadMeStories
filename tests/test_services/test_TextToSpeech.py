import services.TextToSpeech as TextToSpeech

def test_SpeakSelection():

    # Create an MP3 speech saying section_text
    section_text = "Some text to say"
    mp3_output = TextToSpeech.SpeakSection(section_text)

    # Sniff test the MP3 by checking it is about the right size
    assert len(mp3_output) > 3000
    assert len(mp3_output) < 10000