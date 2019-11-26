import os
from shutil import copyfile
import services.text_to_speech as TextToSpeech
import services.novel_sites.uploaded_epub as UploadedEpub

def CopyChapter(chapter, total_chaps):
        print("Proccessed chapter {} of {}".format(chapter['chapter_number'], total_chaps))
        temp_mp3 = TextToSpeech.SpeakChapter(chapter)
        copyfile(temp_mp3.name, os.path.join('/home/tim/audiobook/Worm/Chapter_{}.mp3'.format(chapter['chapter_number'])))

def NovelToAudiobook():
    
    #Fetch an actual story
    story_rip = UploadedEpub.GetStoryByLocalPath('/home/tim/Documents/code/ReadMeStories/tests/test_assets/Worm.epub')
    print('Printing chapter')

    selected_chapters = story_rip [19:]
    for chapter in selected_chapters:
        CopyChapter(chapter, len(selected_chapters))
    #for chapter in story_rip:


NovelToAudiobook()