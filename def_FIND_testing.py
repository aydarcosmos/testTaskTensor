import urllib.request

url = 'https://lenta.ru/news/2019/10/16/shar_smerti/'
raw_page = urllib.request.urlopen(url).read().decode('utf8')

def find(html_text, tag='div', filter=None):
    #some algoritm which will return all text in needed TAG with FILTER. If FILTER = None, return text in all tag blocks
    def find_tag_places(tag):
        start = 0
        tags = []
        while start != -1:
            tag_place = html_text.find(str(tag), start+1)
            tags.append(tag_place)
            start = tag_place
        return tags

    open_tag = '<' + tag
    close_tag = '</' + tag

    all_open_tag_places = find_tag_places(open_tag)
    all_close_tag_places = find_tag_places(close_tag)

    def combine_open_and_close_tags(open_tags, close_tags):
        tag_nums = len(open_tags)
        list_of_tag_pairs = []
        for close_tag in close_tags:
            if len(open_tags) == 2:
                list_of_tag_pairs.append([open_tags[0], close_tag])
                break
            for i in range(tag_nums):
                if close_tag > open_tags[i] and close_tag < open_tags[i+1]:
                    list_of_tag_pairs.append([open_tags[i], close_tag])
                    open_tags.remove(open_tags[i])
                    break
        return list_of_tag_pairs

    list_of_tag_pairs = combine_open_and_close_tags(all_open_tag_places, all_close_tag_places)      #get all pairs like <div> ... </div> 
    
    if filter==None:
        text = ''
        for tag_pair in list_of_tag_pairs:
            text = text + r'\n' + html_text[tag_pair[0]:tag_pair[1]]
    else:
        filter_element_place = html_text.find(filter)
        for tag_pair in list_of_tag_pairs:
            if tag_pair[0] < filter_element_place and tag_pair[1] > filter_element_place:
                filtered_tag_pair = tag_pair
                break
        text = html_text[filtered_tag_pair[0]:filtered_tag_pair[1]]
    
    return text

text = find(raw_page, 'div', 'itemprop="articleBody"')
print(find(text, 'p'))

