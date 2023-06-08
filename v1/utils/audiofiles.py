import os

from pydantic import FilePath
from pydub import AudioSegment


def convert_audio(audiopath: FilePath) -> str:
    audio = AudioSegment.from_wav(audiopath)
    audioname = audiopath.split('/')[-1]
    audioname = audioname[:-4] + '.mp3'
    new_path = os.path.join('music_converter_service', 'audiofiles_mp3', audioname)
    audio.export(new_path, format='mp3')
    return new_path
