import services.text_to_speech as TextToSpeech

output = TextToSpeech.SpeakSection("Some text to say")

print(len(output))