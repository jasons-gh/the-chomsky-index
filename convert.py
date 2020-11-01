import pysubs2
from datetime import datetime
from pathlib import Path


# Files auto-generated by YT have each subtitle line repeating 3 times, once at
# the end of a pair, once by itself and once at the beginning of a pair.
# But sometimes only the first case (end of a pair) exists, which are lines
# 3 + 10i.

for srt_file in [x for x in Path(__file__).parent.glob('**/*.srt') if x.is_file()]:
    with open(srt_file, 'r', encoding='utf-8') as file_object:
        contents = file_object.readlines()

        # Check for repeating lines from auto-generated subtitles (use lines 3+10i)
        # or non-repeating subtitles from a manual upload (parse using srt library)

        if (
            len(contents) > 40 and
            ((contents[3].strip() != '' and contents[3] == contents[7] and contents[7] == contents[12]) or
            (contents[13].strip() != '' and contents[13] == contents[17] and contents[17] == contents[22]) or
            (contents[23].strip() != '' and contents[23] == contents[27] and contents[27] == contents[32]) or
            (contents[33].strip() != '' and contents[33] == contents[37] and contents[37] == contents[42]))
            ):
            print(srt_file.name + ' is a repeating file')

            # Make lists of lines and times

            lines = []
            i = 0
            while 3+10*i < len(contents):
                lines.append(contents[3+10*i])
                i += 1

            times = []
            i = 0
            while i < len(lines):
                t = datetime.strptime(contents[1+10*i][:8], '%H:%M:%S')
                times.append(str(t.hour*3600 + t.minute*60 + t.second) + '\n')
                i += 1

        else:
            print(srt_file.name + ' is a nonrepeating file')            
            subtitles = pysubs2.load(srt_file, encoding="utf-8")
            lines = []
            for i in subtitles:
                lines.append(str(i.text.replace('\n', ' ').replace(r'\N', ' ')) + '\n')
            times = []
            for i in subtitles:
                times.append(str(int(i.start // 1000)) + '\n')

        # Make .en.cnt with lines then times

        with open(str(Path(__file__).parent) + '\\' + srt_file.name[:-7] + '.en.cnt', 'a') as cnt_file:
            for i in lines:
                cnt_file.write(i)
    
        with open(str(Path(__file__).parent) + '\\' + srt_file.name[:-7] + '.en.cnt', 'a') as cnt_file:
            for i in times:
                cnt_file.write(str(i))
