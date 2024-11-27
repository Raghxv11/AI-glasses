import gtts
import playsound

text = input("Enter something: ")
sound = gtts.gTTS(text, lang="en")

sound.save("test.mp3")
playsound.playsound("test.mp3")