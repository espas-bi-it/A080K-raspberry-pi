from pydub import AudioSegment
from pydub.playback import play

def playSound(soundPath):
    sound = AudioSegment.from_wav(soundPath)
    play(sound)