import os

import services.text_to_speech as TextToSpeech

def test_SpeakSelection():

    # Create an MP3 speech saying section_text
    section_text = "Some text to say"

    tempfile_mp3_output = TextToSpeech.SpeakSection(section_text)

    # Sniff test the MP3 by checking it is about the right size
    assert os.stat(tempfile_mp3_output.name).st_size > 3000
    assert os.stat(tempfile_mp3_output.name).st_size < 10000
    os.unlink(tempfile_mp3_output.name)


def test_SpeakChapter():

    sample_chapter_dict = {
        "title": "My Title",
        "text": ''.join([ 'cats and dogs.' * 10 + os.linesep * 2 for i in range(5) ])
    }

    tempfile_mp3_output = TextToSpeech.SpeakChapter(sample_chapter_dict)

    # Sniff test the MP3 by checking it is about the right size
    assert os.stat(tempfile_mp3_output.name).st_size > 204919
    assert os.stat(tempfile_mp3_output.name).st_size < 404919    
    os.unlink(tempfile_mp3_output.name)

def test_SpeakLongText():
    
    # Should be split into 5 paragraphs before synthesis
    sample_text = ''.join([ 'cats and dogs.' * 10 + os.linesep * 2 for i in range(5) ])

    tempfile_mp3_output = TextToSpeech.SpeakLongText(sample_text)

    # Sniff test the MP3 by checking it is about the right size
    assert os.stat(tempfile_mp3_output.name).st_size > 204919
    assert os.stat(tempfile_mp3_output.name).st_size < 404919    
    os.unlink(tempfile_mp3_output.name)

def test_SplitTextToSections():

    # Test: Split by paragraph
    # Test input: 1000 paragraphs each containing the word cats 50 times
    num_paragraphs = 1000
    max_section_size = 500
    text_with_paragraphs = ''.join([ 'cats ' * 50 + os.linesep * 2 for i in range(num_paragraphs) ])
    text_seperated_into_sections = TextToSpeech.SplitTextToSections(text_with_paragraphs, max_section_size)
    assert len(text_seperated_into_sections) == num_paragraphs
    for section in text_seperated_into_sections:
        assert len(section) < max_section_size

    # Test: Split long text without paragraphs into nearest sentence
    # Test input: Several paragraphs then one triple sized paragraph of short sentences
    num_sentences = 90
    text_with_long_paragraph = ''.join([ 'cats ' * 50 + os.linesep * 2 for i in range(num_paragraphs)]) + ''.join([ 'Cats and dogs. ' * num_sentences ])
    text_seperated_into_sections = TextToSpeech.SplitTextToSections(text_with_long_paragraph, max_section_size)
    assert len(text_seperated_into_sections) == num_paragraphs + num_sentences
    for section in text_seperated_into_sections:
        assert len(section) < max_section_size

    # Test split long text with no sentences by word
    # Test Input: Several paragraphs then one long paragraph with no sentences
    text_with_long_paragraph_no_sentences = ''.join( [ 'cats ' * 50 + os.linesep * 2 for i in range(num_paragraphs) ] ) + ''.join( [ 'cats ' * 90 ] )
    text_seperated_into_sections = TextToSpeech.SplitTextToSections(text_with_long_paragraph_no_sentences, max_section_size)
    # Check none of the sections is too big
    for section in text_seperated_into_sections:
        assert len(section) < max_section_size

    # Test: split long text with no words, truncate the big words
    # Test Input: Several paragraphs then one long paragraph with no sentences
    text_with_long_paragraph_just_one_word = ''.join( [ 'cats ' * 50 + os.linesep * 2 for i in range(num_paragraphs) ] ) + ''.join( [ 'cats' * 90 ] )
    text_seperated_into_sections = TextToSpeech.SplitTextToSections(text_with_long_paragraph_just_one_word, 500)
    for section in text_seperated_into_sections:
        assert len(section) < max_section_size


def test_CleanUpTextForTTS():
    assert False

    # Test find long runs of non-alpha and remove
    
    # Test find URLs and remove

    # Test find very long words and truncate or split