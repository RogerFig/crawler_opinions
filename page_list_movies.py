from bs4 import BeautifulSoup
from urllib import request

class Page_list_movies():
    def __init__(self, limit=None):
        self.limit = limit

    def get_list(self, link):
        html_doc = request.urlopen(link)
        self.soup = BeautifulSoup(html_doc, 'html.parser')
        movie_list = self.soup.find_all("li", class_="span2 movie_list_item")
        list_keys_links = []
        for movie in movie_list:
            key_movie = movie.select_one("span a")["href"].strip('/')
            link_movie = link_movie = 'https://filmow.com' + movie.select_one("span a")["href"]
            list_keys_links.append((key_movie, link_movie))
        return list_keys_links

    def next(self):
        next_page = self.soup.select_one('a#next-page')
        if next_page:
            num_page = int(next_page['href'].split('=')[1])
            if self.limit and num_page > self.limit:
                return None
            else:
                return 'https://filmow.com'+next_page['href']
        else:
            return None

if __name__ == '__main__':
    page_list_movies = Page_list_movies(limit=5)

    next = 'https://filmow.com/filmes-todos/'
    print("Page 1")
    while next:
        list_movies = page_list_movies.get_list(next)
        for movie in list_movies:
            print('Key: ' + movie[0] + ' Link: ' + movie[1])
        next = page_list_movies.next()
        if next:
            print("Page " + next.split("=")[1])
    