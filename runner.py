import os
from shutil import copyfile
import services.text_to_speech as TextToSpeech
import services.novel_sites.royal_road as RoyalRoad


def NovelToAudiobook():
    
    #Fetch an actual story
    story_rip = RoyalRoad.GetStoryByID('26675')

    for chapter in story_rip:
        temp_mp3 = TextToSpeech.SpeakChapter(chapter)
        copyfile(temp_mp3.name, os.path.join('/home/tim/audiobook/Chapter_{}.mp3'.format(chapter['chapter_number'])))
        os.unlink(temp_mp3.name)

NovelToAudiobook()