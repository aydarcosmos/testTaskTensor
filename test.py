import urllib.request

url = 'https://lenta.ru/news/2019/10/16/shar_smerti/'
raw_page = urllib.request.urlopen(url).read().decode('utf8')

#f = open('index.html', 'r')
#raw_page = f.read()
#f.close()

def places(tag):
    start = 0
    tags = []
    while start != -1:
        tag_place = raw_page.find(str(tag), start+1)
        tags.append(tag_place)
        start = tag_place
    return tags

places_div_start = places('<div')
places_div_end = places('</div')
tag_nums = len(places_div_start)
print(places_div_start)
print(places_div_end)
list_of_div_pairs = []

for j in places_div_end:
    if len(places_div_start) == 2:
        list_of_div_pairs.append([places_div_start[0], j])
        break
    for i in range(tag_nums):
        if j > places_div_start[i] and j < places_div_start[i+1]:
            list_of_div_pairs.append([places_div_start[i], j])
            places_div_start.remove(places_div_start[i])
            break

print(tag_nums)

#print(list_of_div_pairs)
articleBody = raw_page.find(r'itemprop="articleBody"')
print()

for tag_pair in list_of_div_pairs:
    if tag_pair[0] < articleBody and tag_pair[1] > articleBody:
        needed_pair = tag_pair
        print(tag_pair)
        break

#print(raw_page[needed_pair[0]:needed_pair[1]])

place_p_start = places('<p')
place_p_end = places('</p')

print(place_p_start)
print(place_p_end)