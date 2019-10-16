import urllib.request

class ParserFromWeb:
    def __init__(self, url = 'https://lenta.ru/news/2019/10/16/shar_smerti/'): #https://lenta.ru/news/2019/10/16/shar_smerti/
        self.url = url
        self.raw_page = urllib.request.urlopen(self.url).read().decode('utf8')
        
        
    def get_raw_page(self):
        articleBody = self.raw_page.find(r'itemprop="articleBody"')
        #end = start + 10000
        start = 0
        divs = []
        while start != -1:
            div_num = self.raw_page.find(r'<div', start+1)
            divs.append(div_num)
            start = div_num
        #print(self.raw_page.find(r'<div'))
        #print(self.raw_page.count(r'</div>'))
        print(div)

        
        

lenta_page = ParserFromWeb()
lenta_page.get_raw_page()

        
        