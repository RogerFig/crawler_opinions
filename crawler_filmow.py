from selenium import webdriver
from page_list_movies import Page_list_movies
from page_movie import Page_movie
import os
import sys, getopt
import simplejson as json

'''
    Ate página 1305 são: aprox 3042354 comentários
    1305 - 2559: 999294
'''
class Crawler_filmow():

    def __init__(self, link, limit=None):
        self.link = link
        self.limit = limit
        self.root = 'filmow/'
        arq_list_movies = open('list_movies.json','r')
        self.list_movies = json.load(arq_list_movies)
        arq_list_movies.close()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--lang=pt-BR")
        options.add_argument('window-size=1200x800')
        options.add_argument("--disable-infobars")
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        #options.binary_location = "/home/rogerio/Applications/chrome-linux/chrome"
        self.driver = webdriver.Chrome(options=options)

    def main(self):
        page_list_movies = Page_list_movies(self.limit)
        # get página inicial
        next = self.link
        while next:
            list_movies = page_list_movies.get_list(next)
            for movie_key, movie_link in list_movies:
                # criar pasta do filme
                if os.path.isdir(self.root+movie_key) or movie_key in self.list_movies:
                    continue
                else:
                    print(movie_key)
                    os.mkdir(self.root+movie_key)
                # instancia um page movie para tratar os comentários
                page_movie = Page_movie(movie_key, self.driver, self.root)
                # get lista de comentários
                # Salvar todos os comentários
                page_movie.save_reviews(movie_link)
                # Passar para a próxima página
            next = page_list_movies.next()
            if next:
                print("Page " + next.split("=")[1])


    # def sum_comments_count(self):
    #     total = 0
    #     while True:
    #         print("Visiting page: %s" % (self.driver.current_url))
    #         quant_comments_movies = self.driver.find_elements_by_class_name("badge-num-comments")
    #         for quant_comments in quant_comments_movies:
    #             total += int(quant_comments.text.strip().replace(',','').replace('K','00'))
    #         try:
    #             next_page_link = self.driver.find_element_by_id("next-page").get_attribute('href')
    #             #ActionChains(self.driver).move_to_element(next_page).perform()
    #             #next_page.click()
    #         except NoSuchElementException:
    #             break
    #         self.driver.get(next_page_link)
    #     print(total)

    # def has_next(self):
    #     pass
    
    def close(self):
        self.driver.close()

if __name__ == '__main__':
    argv = sys.argv[1:]
    #print(sys.argv[1:])
    inicial = 1
    final = ''
    try:
        opts, args = getopt.getopt(argv,"h")
    except getopt.GetoptError:
        print('Usage: crawler_filmow.py inicial final')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: crawler_filmow.py inicial final')
            sys.exit()
    if len(args) == 2:
        try:
            inicial = int(args[0])
            final = int(args[1])
        except:
            print('Usage: crawler_filmow.py inicial final')
    else:
            print('Usage: crawler_filmow.py inicial final')

    link = "https://filmow.com/filmes-todos/?pagina=" + str(inicial)
    crawler = Crawler_filmow(link, final)
    crawler.main()
    crawler.close() 
