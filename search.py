import concurrent.futures
import re
from collections import Counter
from pathlib import Path

# A search function return a list of 5-tuples:
# (sorting info, result info, name, subtitle, url).
# search_results sorts and returns list of 4-tuples.


def select_files(entry, files):
    if ';' in entry.lower():
        phrases = [x.strip() for x in entry.lower().split(';')]
    elif '+' in entry.lower():
        phrases = [x.strip() for x in entry.lower().split('+')]
    else:
        phrases = [entry.lower().strip()]

    selected_files = []

    for file in files:
        with open(file, 'r', encoding='utf-8') as file_object:
            data = file_object.read()
            if all(phrase.lower() in data.lower().replace('\n', ' ') for phrase in phrases):
                selected_files.append(file)

    return selected_files


def search_cnt_normal_separate_nearby(entry, cnt_files):
    occurrences = []

    for j in range(entry.lower().count(';') + 1):

        if not '+' in entry:
            re_string = (r'^[^\n]*' +
                         str(entry.lower().split(';')[j].strip().replace(' ', '\s')) +
                         r'[^\n]*\n[^\n]*\n[^\n]*')
        else:
            re_string = r'^'
            for phrase in [x.strip() for x in entry.lower().split('+')]:
                re_string += (r'(?=(.{0,1500}' +
                              str(phrase).replace(' ', '\s') +
                              r'[^\n]*\n[^\n]*\n[^\n]*))')

        for file in cnt_files:
            seconds = -30
            with open(file, 'r', encoding='utf-8') as file_object:
                data = file_object.read()

                matches = re.finditer(re_string, data, re.I | re.M | re.S)

                if matches:
                    for match in matches:
                        if int(data.split('\n')[int(data[0:match.start()].count('\n') + data.count('\n')/2)]) - seconds >= 30:

                            # Subtitle
                            if not '+' in entry:

                                cut = 0
                                while data[:match.end()].count('\n') - cut >= int(data.count('\n')/2):
                                    cut += 1
                                subtitle = ' '.join(match.group().splitlines()[:len(match.group().splitlines())-cut])

                            else:

                                if any(match.group(_).count('\n') == 4 for _ in range(1, len(match.groups()) + 1)):

                                    # get a list of match groups, cuts and lengths
                                    # remove duplicates of these triples, which are the same subtitle
                                    # order by length, which orders chronologically
                                    # create subtitle
                                    
                                    groups_properties = []

                                    for _ in range(1, len(match.groups()) + 1):
                                        
                                        cut = 0
                                        while data[:match.end(_)].count('\n') - cut >= int(data.count('\n')/2):
                                            cut += 1
                            
                                        length = len(match.group(_))
                                                     
                                        groups_properties.append((match.group(_), cut, length))
                                    
                                    groups_properties = list(set(groups_properties))
                                    
                                    groups_properties = sorted(groups_properties, key=lambda t: t[2])

                                    subtitle = ''
                                    for group_properties in groups_properties:
                                       subtitle = subtitle + ' '.join(group_properties[0].splitlines()[-5:len(group_properties[0].splitlines())-group_properties[1]]) + ' ... '
                                    subtitle = subtitle[:-5]

                                else:
                                    continue

                            # Other information
                            seconds = int(data.split('\n')[int(data[0:match.start()].count('\n') + data.count('\n')/2)])
                            video_id = file.name[-18:-7]
                            name = file.name[:file.name.rfind(' ')]
                            url = r'https://youtu.be/' + video_id + '?t=' + str(seconds)

                            if not '+' in entry:
                                occurrences.append((video_id, video_id, name, subtitle, url))
                            else:
                                occurrences.append(((len(match.groups()), video_id), video_id, name, subtitle, url))

    return occurrences


def search_results(entry, base_path):

    # Validate
    if (entry.strip() == '' or (';' in entry and '+' in entry)
            or any(x in entry for x in '.^$*?{}[]\\|()')
            or entry.replace(' ', '').replace('\t', '').isdigit()):
        return []

    if ';' in entry:
        search_type = 'separate'
    elif '+' in entry:
        search_type = 'nearby'
    else:
        search_type = 'normal'

    # Files to search
    cnt_files = [x for x in Path(base_path / 'cnt').glob('**/*.cnt') if x.is_file()]
    selected_cnt_files = select_files(entry, cnt_files)

    # Search
    results = []

    if cnt_files:
        
        # results = results + search_cnt_normal_separate_nearby(entry, selected_cnt_files)

        # Multiprocessing - split selected_cnt_files into 8 parts
        processes = 8
        k, m = divmod(len(selected_cnt_files), processes)
        parts = (selected_cnt_files[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(processes))

        with concurrent.futures.ProcessPoolExecutor() as executor:
            outputs = [executor.submit(search_cnt_normal_separate_nearby, entry, part) for part in parts]
            
            for f in concurrent.futures.as_completed(outputs):
                results = results + f.result()

    # if txt_files:

    # Sort
    if search_type == 'normal' or search_type == 'separate':

        occurrences_counts = Counter(t[0] for t in results)
        occurrences_sorted = sorted(results, key=lambda t:occurrences_counts[t[0]], reverse=True)
        occurrences_sorted = [(x[1], x[2], x[3], x[4]) for x in occurrences_sorted]
        results_sorted = occurrences_sorted

    else:

        nearby_counts = Counter(t[0][1] for t in results)
        nearby_sorted = sorted(results, key=lambda t: (t[0][0], nearby_counts[t[0][1]]), reverse=True)
        nearby_sorted = [(x[1], x[2], x[3], x[4]) for x in nearby_sorted]
        results_sorted = nearby_sorted

    return results_sorted
