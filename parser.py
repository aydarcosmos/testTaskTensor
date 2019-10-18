import sys
import urllib.request 
from urllib.parse import urlparse
import re

class MiniReadability:

    def __init__(self, url = 'https://www.ufa.kp.ru/daily/27043/4108254/'): 
        self.url = url
        self.site_name = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
        self.page = urllib.request.urlopen(self.url).read().decode('utf8')

    def _get_tag_pairs(self, html_text, tag_for_search):
        #some algoritm which will return all text in needed TAG with FILTER. If FILTER = None, return text in all tag blocks 
        
        def __find_tag_places(tag):
            start = 0
            tags = []
            while start != -1:
                tag_place = html_text.find(str(tag), start + 1)
                tags.append(tag_place)
                start = tag_place
            return tags

        def __combine_open_and_close_tags(open_tags, close_tags):

            tag_nums = len(open_tags)
            list_of_tag_pairs = []
            for close_tag in close_tags:
                if len(open_tags) == 2:
                    list_of_tag_pairs.append([open_tags[0], close_tag])
                    break
                try:    
                    for i in range(tag_nums):
                        if close_tag > open_tags[i] and close_tag < open_tags[i+1]:
                            list_of_tag_pairs.append([open_tags[i], close_tag])
                            open_tags.remove(open_tags[i])
                            break
                except IndexError:
                    pass
            return list_of_tag_pairs
        
        open_tag = '<' + tag_for_search
        close_tag = '</' + tag_for_search + '>'  

        all_open_tag_places = __find_tag_places(open_tag)
        all_close_tag_places = __find_tag_places(close_tag)

        list_of_tag_pairs = __combine_open_and_close_tags(all_open_tag_places, all_close_tag_places)    #get all pairs like <div> ... </div> 
        return list_of_tag_pairs
        
    def _find_useful_text(self, html_text, tag, filter = None):
        list_of_tag_pairs = self._get_tag_pairs(html_text, tag)
        list_of_text_blocks = []
        if filter==None:
            for tag_pair in list_of_tag_pairs:
                list_of_text_blocks.append(html_text[tag_pair[0]:tag_pair[1]])
        else:
            filter_element_place = html_text.find(filter)
            for tag_pair in list_of_tag_pairs:
                if tag_pair[0] < filter_element_place and tag_pair[1] > filter_element_place:
                    filtered_tag_pair = tag_pair
                    break
            list_of_text_blocks.append(html_text[filtered_tag_pair[0]:filtered_tag_pair[1]])
        
        return list_of_text_blocks
            
    def format_text(self, text):
        #change <a href='url'>url_name<>  to  url_name[url] and put \n beetween blocks
        def format_links(input_text):
            number_of_a_tag_in_text = len(self._get_tag_pairs(text, 'a'))               
            for _ in range(number_of_a_tag_in_text):    
                start = input_text.find('<a') 
                end = input_text.find('</a>')

                link = input_text[start:end].split('href="')[1].split('"')[0]
                if link.find('http') == -1:
                    link = self.site_name + link
                link_name = input_text[start:end].split('>')[1]
                text_to_past = link_name + ' [' + link + ']'
                input_text = input_text[:start] + text_to_past + input_text[end+len('</a>'):]
            return input_text

        text = format_links(text)

        def put_separators_instead_tag(text, tag):
            re_exp = '<' + tag + '>'
            cleanr = re.compile(re_exp)
            text_with_separators = re.sub(cleanr, '\n\n   ', text)
            return text_with_separators
        text = put_separators_instead_tag(text, 'p')

        def delete_tags(text):
            cleanr = re.compile('<.*?>')
            clean_text = re.sub(cleanr, '', text)
            return clean_text
        
        text = delete_tags(text)        
        
        return text

    def _get_article_name(self):
        title = self._find_useful_text(self.page, 'title')
        return title


    def get_significant_and_formated_text(self):
        title = self._get_article_name()
        if self.site_name == 'https://www.ufa.kp.ru':
            self.page  = self._find_useful_text(self.page, 'div', filter = 'class="textContent"') # return needed div block
        else:
            self.page  = self._find_useful_text(self.page, 'div', filter = 'itemprop="articleBody"') # return needed div block
        self.page = self._find_useful_text(''.join(self.page), 'p') #return all news, but with <a> tags
        self.page = self.format_text(title[0] + ''.join(self.page))
        return self.page

    def save_to_file(self, text):
        #check directories, if need create new one and save text.
        pass
        
        
def main():
    #url = sys.argv[1]
    web_page = MiniReadability()
    text = web_page.get_significant_and_formated_text()
    print(text)
    
    #lenta_page.save_to_txt()

if __name__ == '__main__':
    main()