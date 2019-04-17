from selenium import webdriver
from page_list_movies import Page_list_movies
from page_movie import Page_movie
import os
import sys, getopt

'''
    Até página 1305 são: aprox 3042354 comentários
    1305 - 2559: 999294
'''
class Crawler_filmow():

    def __init__(self, link, limit=None):
        self.link = link
        self.limit = limit
        #options = Options()
        #options.headless = True
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--lang=pt-BR")
        options.add_argument('window-size=1200x800')
        options.add_argument("--disable-infobars")
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        #options.binary_location = "/home/rogerio/Applications/chrome-linux/chrome"
        self.driver = webdriver.Chrome(options=options)
        #self.driver = webdriver.Firefox(options=options)

    def main(self):
        page_list_movies = Page_list_movies(self.limit)
        # get página inicial
        next = self.link
        while next:
            list_movies = page_list_movies.get_list(next)
            for movie in list_movies:
                # criar pasta do filme
                if not os.path.isdir('reviews_filmow/'+movie[0]):
                    os.mkdir('reviews_filmow/'+movie[0])
                # instancia um page movie para tratar os comentários
                page_movie = Page_movie(movie[0], self.driver)
                # get lista de comentários
                # Salvar todos os comentários
                page_movie.save_reviews(movie[1])
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
    inicial = ''
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
