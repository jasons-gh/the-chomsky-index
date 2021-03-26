import itertools
import pandas as pd
import re
from bs4 import BeautifulSoup
from pathlib import Path
from unidecode import unidecode


def search_results(entry, base_df, base_path, settings):

    # Validate
    if (entry.strip() == '' or (';' in entry and '+' in entry)
            or any(x in entry for x in '.^$*?{}[]\\|()')
            or entry.replace(' ', '').replace('\t', '').isdigit()):
        return []

    # Filter
    if ';' in entry:
        search_type = 'separate'
    elif '+' in entry:
        search_type = 'nearby'
    else:
        search_type = 'normal'

    if ';' in entry.lower():
        phrases = [x.strip() for x in entry.lower().split(';')]
    elif '+' in entry.lower():
        phrases = [x.strip() for x in entry.lower().split('+')]
    else:
        phrases = [entry.lower().strip()]

    if any([phrase == '' for phrase in phrases]):
        return []

    phrase_info = []
    for phrase in phrases:
        phrase_info.append((phrase,
                            f"match_{phrase.replace(' ', '_')}",
                            f"start_{phrase.replace(' ', '_')}"))

    cnt_df = base_df.copy()
    if settings['Video']:
        cnt_df = cnt_df[cnt_df['ext'] == 'cnt']
        cnt_df = all_filter(cnt_df, phrase_info)
        if search_type == 'nearby':
            cnt_df = nearby_filter(cnt_df, phrase_info)
        cnt_df = count_filter(cnt_df, phrase_info)
    else:
        cnt_df = cnt_df[0:0]

    html_df = base_df.copy()
    if settings['Print']:
        html_df = html_df[html_df['ext'] == 'html']
        html_df = all_filter(html_df, phrase_info)
        if search_type == 'nearby':
            html_df = nearby_filter(html_df, phrase_info)
        html_df = count_filter(html_df, phrase_info)
    else:
        html_df = html_df[0:0]

    # Search
    cnt_df['occurrences'] = [[] for _ in range(len(cnt_df))]
    if settings['Video']:
        cnt_re_strings = re_strings(search_type, phrases)
    
        if search_type == 'normal':
            cnt_df['occurrences'] = cnt_df.apply(cnt_search, args=[cnt_re_strings[0], search_type], axis=1)
        elif search_type == 'separate':
            for cnt_re_string in cnt_re_strings:
                cnt_df['occurrences'] = cnt_df.apply(cnt_search, args=[cnt_re_string, search_type], axis=1)
        else:
            cnt_df['occurrences'] = cnt_df.apply(cnt_nearby, args=[cnt_re_strings[0], search_type], axis=1)
    else:
        cnt_df = cnt_df[0:0]


    # cnt_df['occurrences'] = ''
    # cnt_df['occurrences'] = cnt_df.apply(cnt_search, args=[entry], axis=1)

    for x in Path(base_path / 'html').glob('**/*.html'):
        x.unlink()

    html_df['occurrences'] = [[] for _ in range(len(html_df))]
    if settings['Print']:
        if search_type == 'normal':
            html_df['occurrences'] = html_df.apply(html_search, args=[*phrases, base_path], axis=1)
        elif search_type == 'separate':
            for phrase in phrases:
                html_df['occurrences'] = html_df.apply(html_search, args=[phrase, base_path], axis=1)
        else:
            html_df['occurrences'] = html_df.apply(html_nearby, args=[phrases, base_path], axis=1)
    else:
        html_df = html_df[0:0]


    # Sort
    
    results_df = pd.concat([cnt_df, html_df])
    
    results_df['occurrences_len'] = ''
    results_df['occurrences_len'] = results_df['occurrences'].apply(len)
    
    results_df['name_lower'] = ''
    results_df['name_lower'] = results_df['name'].apply(lambda x: x.lower())
    
    results_df.sort_values(by=['occurrences_len', 'name_lower'], ascending=[False, True], inplace=True)

    return [i for j in results_df['occurrences'].tolist() for i in j]


def all_filter(df, phrase_info):
    """Filter used for all search types"""
    for phrase, match_col, start_col in phrase_info:
        df[match_col] = df['content'].apply(match, args=[phrase])

    df['all_phrases'] = df[[x[1] for x in phrase_info]].all(1)

    return df.loc[df['all_phrases']]


def match(content, phrase):
    """Returns True if all phrases found"""
    return bool(re.search(phrase.replace(' ', '\s'), content, re.I | re.M | re.S))


def nearby_filter(df, phrase_info):
    """Filter used for nearby search type"""
    for phrase, match_col, start_col in phrase_info:
        df[start_col] = df['content'].apply(starts, args=[phrase])

    df['product'] = ''
    df['product'] = df.apply(product, args=[phrase_info], axis=1)

    df['is_nearby'] = df['product'].apply(is_nearby, args=[phrase_info])

    return df.loc[df['is_nearby']]


def count_filter(df, phrase_info):
    df['count_col'] = df['content'].apply(count, args=[phrase_info])
    df.sort_values(by=['count_col'], ascending=[False], inplace=True)

    df['cumsum_col'] = df['count_col'].cumsum()
    df = df[df['cumsum_col'] < 500]

    return df


def count(content, phrase_info):
    return sum([len([match.start() for match in re.finditer(phrase.replace(' ', '\s'), content, re.I | re.M | re.S)]) for phrase, match_col, start_col in phrase_info])


def starts(content, phrase):
    """Returns list of phrase start positions"""
    return [match.start() for match in re.finditer(phrase.replace(' ', '\s'), content, re.I | re.M | re.S)]


def product(row, phrase_info):
    """Returns list of combinations of phrase start positions"""
    return list(itertools.product(*[row[start_col] for phrase, match_col, start_col in phrase_info]))


def is_nearby(product, phrase_info):
    """Returns True if any combination has all phrase start positions within 1500 characters"""
    return any([max(element) - min(element) <= 1500 * (len(phrase_info) - 1) for element in product])

def re_strings(search_type, phrases):
    re_strings = []
    
    if search_type == 'normal':
        re_strings.append((r'^[^\n]*' +
                         str(phrases[0].replace(' ', '\s')) +
                         r'[^\n]*\n' * 10 + r'[^\n]*'))

    elif search_type == 'separate':
        for phrase in phrases:
            re_strings.append((r'^[^\n]*' +
                             str(phrase.replace(' ', '\s')) +
                             r'[^\n]*\n' * 10 + r'[^\n]*'))

    else:
        re_string = ''
        for phrase in phrases:
            re_string += (r'(?=(.{0,1500}' +
                         str(phrase).replace(' ', '\s') +
                         r'[^\n]*\n[^\n]*\n[^\n]*))')
        re_strings.append(re_string)
        
    return re_strings


def cnt_search(row, re_string, search_type):
    occurrences = []
    data = row['content']
    seconds = -30

    matches = re.finditer(re_string, data, re.I | re.M | re.S)

    for match in matches:
        if int(data.split('\n')[int(data[0:match.start()].count('\n') + data.count('\n')/2)]) - seconds >= 30:

            # Subtitle
            cut = 0
            while data[:match.end()].count('\n') - cut >= int(data.count('\n')/2):
                cut += 1
            subtitle = ' '.join(match.group().splitlines()[:len(match.group().splitlines())-cut])

            # Other information
            seconds = int(data.split('\n')[int(data[0:match.start()].count('\n') + data.count('\n')/2)])
            video_id = row['base_url'][-11:]
            name = row['name']
            url = r'https://www.youtube.com/watch?v=' + video_id + '&t=' + str(seconds)

            occurrences.append((video_id, name, subtitle, url))

    return row['occurrences'] + occurrences


def cnt_nearby(row, re_string, search_type):
    occurrences = []
    data = row['content']
    seconds = -30

    matches = re.finditer(re_string, data, re.I | re.M | re.S)

    for match in matches:
        if int(data.split('\n')[int(data[0:match.start()].count('\n') + data.count('\n')/2)]) - seconds >= 30:

            # Subtitle
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
            video_id = row['base_url'][-11:]
            name = row['name']
            url = r'https://www.youtube.com/watch?v=' + video_id + '&t=' + str(seconds)

            occurrences.append((video_id, name, subtitle, url))

    return row['occurrences'] + occurrences


def html_search(row, phrase, base_path):
    occurrences = []
    soup_page = BeautifulSoup(row['content'], "html.parser")
    re_string = phrase.replace(' ', '\s')
    name = str(row.name) + ' ' + str(row['name'])[:150]
    for char in '\\/:*?"<>|\n':
        name = name.replace(char, ' ')

    for tag_index, content in enumerate(soup_page.find_all(lambda tag, re_string=re_string: tags(tag, re_string))):

        text = ' '.join(str(content.get_text()).split())
        content_parent = content

        try:
            content_parent.clear()
        except:
            continue

        matches = re.finditer(re_string, text, re.I | re.M | re.S)

        starts = [0]
        for match in matches:
            starts.append(match.start())

        parts = [text[i:j] for i, j in zip(starts, starts[1:]+[None])]

        content_parent.append(parts[0])

        for start, part in zip(starts[1:], parts[1:]):
            a = soup_page.new_tag('a')
            a['id'] = str(phrase.replace(' ', '-')) + '-' + str(tag_index) + '-' + str(starts[1:].index(start))
            content_parent.append(a)
            content_parent.append(part)

            context = text.strip().replace('\n', ' ').replace('\t', ' ')
            context = (context[:start - len(text) - 30].split(' ')[-1] +
                       context[start - len(text) - 30:start + 400] +
                       context[start + 400:].split(' ')[0])

            occurrences.append([row['base_url'],
                                row['name'],
                                context,
                                str(Path(base_path) / 'html' / f"{name}-{str(phrase.replace(' ', '-'))}.html") + '#' + str(phrase.replace(' ', '-')) + '-' + str(tag_index) + '-' + str(starts[1:].index(start))])

    with open(Path(Path(base_path) / 'html' / f"{name}-{str(phrase.replace(' ', '-'))}.html"), 'w') as f:
        html = unidecode(str(soup_page.prettify()))
        f.write(html)

    return row['occurrences'] + occurrences


def tags(tag, re_string):
    return tag.name == 'p' and re.compile(re_string, re.I | re.M | re.S).search(tag.get_text())


def html_nearby(row, phrases, base_path):
    """
    This function creates the following lists.
       
    soup_page.find_all(string=True) - every piece of text in the article,
                                      attached to the BeautifulSoup parse tree
                                      
    texts                           - texts taken from the above list,
                                      separated from the BeautifulSoup parse tree
                                      
    soup_matches                    - search through texts list and append a tuple
                                      called a match each time a phrase in phrases is found
                                      eg ('chomsky', (6, 130), 2530) means that
                                      'chomsky' occurs 6 pieces of text in,
                                      130 characters in, which is 2530 characters
                                      into the article text.
                                      
    groups                          - nearby matches from soup_matches are
                                      grouped together into a tuple called a group.
                                      groups is the list of every group. each
                                      group contains the information needed
                                      to create a result occurrence box.
                                      
    contexts                        - a list of strings, one for each
                                      group/result occurrences box
    
    soup_starts                     - for every text in the page: zero, and the
                                      positions of the first match of each group
                                      in groups eg
                                      [[0], [0, 42 , 12], ..., [0, 130], [0], ... , [0]]
                                      
    soup_parts                      - for every text in the page, the text split
                                      into parts using the above list.
    """
    occurrences, texts, soup_matches = [], [], []
    soup_page = BeautifulSoup(row['content'], "html.parser")
    name = str(row.name) + ' ' + str(row['name'])[:150]
    for char in '\\/:*?"<>|\n':
        name = name.replace(char, ' ')

    
    cumulative_length = 0
    for text_index, text in enumerate(soup_page.find_all(string=True)):
        cumulative_length += len(text)
        texts.append((text_index, cumulative_length, text))
    
    for phrase in phrases:
        for text_index, cumulative_length, text in texts:
            matches = re.finditer(phrase.replace(' ', '\s'),
                                  text,
                                  re.I | re.M | re.S)

            # for example, ('chomsky', (7, 130), 2530) means that
            # 'chomsky' occurs in the 7th piece of text, 130 characters in,
            # which is 2530 characters into the article text
            for match in matches:
                soup_matches.append((phrase,
                                     (text_index, match.start()),
                                     cumulative_length - len(text) + match.start()))

    soup_matches.sort(key=lambda x: x[2])
    
    groups = []
    while soup_matches:
        first = soup_matches[0]
        rest = soup_matches[1:]
        
        nearby = []
        nearby.append(first)
        
        for match in rest:
            if match[2] - first[2] <= 1500 * (len(phrases) - 1):
                nearby.append(match)
            else:
                break

        # if every phrase occurs at least once
        if set(phrases) == set([match[0] for match in nearby]):
            
            # collect them
            group = []
            group.append(nearby[0])
            for x in nearby[1:]:
                if x[0] in [y[0] for y in group]:
                    continue
                else:
                    group.append(x)

            groups.append(tuple(group))
            
            for x in group:
                soup_matches.remove(x)

        else:
            del soup_matches[0]

    # get contexts
    contexts = []
    for group in groups:
        context = ''
        for detail in group:
            text_index = detail[1][0]
            text = texts[text_index][2]
            text = text.strip().replace('\n', ' ').replace('\t', ' ')
            char_index = detail[1][1]
            context += (text[:char_index - len(text) - 30].split(' ')[-1] +
                       text[char_index - len(text) - 30:char_index + 200] +
                       text[char_index + 200:].split(' ')[0] +
                       ' ... ')
        context = context[:-5]
        contexts.append(context)
            
    # get page text starts
    soup_starts = [[0] for _ in texts]
    for group in groups:
        text_index = group[0][1][0]
        char_index = group[0][1][1]
        soup_starts[text_index] += [char_index]
        
    # get page text parts
    soup_parts = [[] for _ in texts]
    for text_index, starts in enumerate(soup_starts):
        text = texts[text_index][2]
        soup_parts[text_index] = [text[i:j] for i, j in zip(starts, starts[1:]+[None])]
        
    group_index = 0
    for content, starts, parts in zip(soup_page.find_all(string=True), soup_starts, soup_parts):
        if starts != [0]:
            
            text = str(content)
            content_parent = content.parent
    
            try:
                content_parent.clear()
            except:
                continue
            
            content_parent.append(parts[0])
            
            for start, part in zip(starts[1:], parts[1:]):
                a = soup_page.new_tag('a')
                a['id'] = str(phrase.replace(' ', '-')) + '-' + str(group_index)
                content_parent.append(a)
                content_parent.append(part)
                
            occurrences.append([row['base_url'],
                                row['name'],
                                contexts[group_index],
                                str(Path(base_path) / 'html' / f"{name}.html") + '#' + str(phrase.replace(' ', '-')) + '-' + str(group_index)])
                
            group_index += 1

    with open(Path(Path(base_path) / 'html' / f"{name}.html"), 'w') as f:
        html = unidecode(str(soup_page.prettify()))
        f.write(html)


    return row['occurrences'] + occurrences