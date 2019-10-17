import urllib.request

def get_page(url='https://lenta.ru/news/2019/10/16/shar_smerti/'):
    page = urllib.request.urlopen(url).read().decode('utf8') 
    return page


def find(html_text, tag, filter=None):
    #some algoritm which will return all text in needed TAG with FILTER. If FILTER = None, return text in all tag blocks
    return text

def format(text):
    #change <a href='url'>url_name<>  to  url_name[url] and put \n beetween blocks
    pass

def save_to_txt(formated_text):
    #create new directories and save text.
    pass

def main():
    page = get_page()
    text_from_articleBody  = find(page, 'div', filter = 'itemprop="articleBody"') # return needed div block
    text_from_p = find(text_from_articleBody, 'p') #return all news, but with <a> tags
    formated_text = format(text_from_p)
    save_to_txt(formated_text)

if __name__ == '__main__':
    main()
