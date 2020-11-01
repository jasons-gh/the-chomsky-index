import convert
import sources
import subprocess
from pathlib import Path
from unidecode import unidecode


# youtube-dl - download the subtitles as .vtt files
urls_yt = sources.urls_yt()
for url in urls_yt:
    subprocess.run(['youtube-dl', '-i', '--skip-download', '--write-auto-sub', '-o%(title)s %(id)s', url])


# ffmpeg - convert from .vtt to .srt
for file in [x for x in Path(__file__).parent.glob('**/*.vtt') if x.is_file()]:
    subprocess.run('ffmpeg.exe -i "' + str(file.name) + '" -- "' + str(file.name[:-4]) + '".srt')


# unidecode - replace some characters if present
unidecoded_files = set()

for file in [x for x in Path(__file__).parent.glob('**/*.srt') if x.is_file()]:
    with open(file, 'r', encoding='utf-8') as file_object:
        data = file_object.read()
        for line in data:
            if line != unidecode(line):
                data = data.replace(line, unidecode(line))
                unidecoded_files.add(str(file.name))

    with open(file, 'w', encoding='utf-8') as file_object:
        file_object.write(data)


# convert - convert from .srt to .cnt
convert.convert()


# delete .vtt files
for file in [x for x in Path(__file__).parent.glob('**/*.vtt') if x.is_file()]:
    file.unlink()


# delete .srt files
for file in [x for x in Path(__file__).parent.glob('**/*.srt') if x.is_file()]:
    file.unlink()


# information
print(str(len(urls_yt)) + ' subtitle files requested')
print(str(len([x for x in Path(__file__).parent.glob('**/*.vtt') if x.is_file()])) + ' .vtt subtitle files in this folder')
print(str(len([x for x in Path(__file__).parent.glob('**/*.srt') if x.is_file()])) + ' .srt subtitle files in this folder')
print(str(len(unidecoded_files)) + ' subtitle files unidecoded')
