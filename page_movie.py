import time
import re
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from opinion import Opinion
from bs4 import BeautifulSoup

class Page_movie():
    def __init__(self, key_movie, driver, root):
        self.key_movie = key_movie
        self.driver = driver
        self.root = root

    def save_reviews(self, link):
        self.driver.implicitly_wait(5)
        self.driver.get(link)
        # gerar a página completa
        list_reviews = self.generate_full_page()
        list_opinions = []
        for review in list_reviews:
            list_opinions.append(self.handle_comment(review))
        
        for opinion in list_opinions:
            output = open(self.root + self.key_movie +'/'+opinion.id+'.json','w')
            output.write(opinion.to_json())
            output.close()
        
    def generate_full_page(self):
        comments_old = 0
        comments_new = 0
        retry = 10
        list_comments = []
        #generate all list
        while True:
            try:
                button_load_more = self.driver.find_element_by_class_name("btn-load-comments")
                if button_load_more.text == "Fim!":
                    return self.driver.find_elements_by_class_name("comments-list-item")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                ActionChains(self.driver).move_to_element(button_load_more).perform()
                button_load_more.click()
                time.sleep(1)
                comments_old = comments_new
                comments_new = len(self.driver.find_elements_by_class_name("comments-list-item"))
                if comments_new == comments_old:
                    retry -= 1
                    print('trying ...[%s] (%d)'%(self.key_movie, retry))
                    if retry < 0:
                        print('Refreshing ... ')
                        self.driver.refresh()
                        retry = 10
                        comments_new = 0
                        comments_old = 0
            except WebDriverException as web_driver_exception:
                #Try again...
                if comments_new != comments_old:
                    comments_old = comments_new
                    print('trying ...[%s]'%(self.key_movie))
                elif comments_new == comments_old:
                    retry -= 1
                    print('trying ...[%s] (%d)'%(self.key_movie, retry))
                    if retry < 0:
                        print('Refreshing ... ')
                        self.driver.refresh()
                        retry = 10
                        comments_new = 0
                        comments_old = 0
                #print(web_driver_exception)
        
    def handle_comment(self, review):
        self.driver.implicitly_wait(0)
        html_doc = review.get_attribute('innerHTML')
        soup = BeautifulSoup(html_doc, 'html.parser')

        link_perfil_user = soup.select_one(".user-name")['href']
        autor = link_perfil_user.split('/')[2]
        link_review = soup.select_one(".age")['href']
        id = link_review.split('/')[2]
        data_review = soup.select_one(".age").text.strip()
        now = datetime.now()
        collect_date = now.strftime("%d-%m-%Y %H:%M")
        # remoção de tags spoiler desnecessárias
        msg_spoiler = soup.select_one(".comment-text").select(".message")
        for msg_tag in msg_spoiler:
            msg_tag.decompose()
        # fim remoção
        review_text = soup.select_one(".comment-text").text

        star_tag = soup.select_one(".star-rating")
        star_rating = re.search('\d(\.\d)?',star_tag['title']).group(0) if star_tag else 0

        tag_see = soup.select_one('.icon-ok-sign')
        see = 1 if tag_see else 0

        tag_wsee = soup.select_one('.icon-plus-sign')
        wsee = 1 if tag_wsee else 0
        
        tag_fav = soup.select_one('.favorite')
        favorito = 1 if tag_fav else 0

        likes = int(soup.select_one('.count').text)
        tag_replies = soup.select_one('.comment-show-replies')
        replies = int(tag_replies.text.strip().split(' ')[0] if tag_replies else 0)
        
        opinion = Opinion(id, autor , self.key_movie, data_review, star_rating, review_text, likes, 0, '', link_review, 
        link_perfil_user, collect_date, see, wsee, favorito, replies)

        self.driver.implicitly_wait(5)

        return opinion