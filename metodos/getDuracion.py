# te regresa la duracion en milisegundos de un archivo wav o mp3
from mutagen.mp3 import MP3
from mutagen.wave import WAVE


def getlen(filename):
    print(filename[-3:])
    if filename[-3:] == 'mp3':
        audio = MP3(filename)
    elif filename[-3:] == 'wav':
        audio = WAVE(filename)
    return int(audio.info.length * 1000)
