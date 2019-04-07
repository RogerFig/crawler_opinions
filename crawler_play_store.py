from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.options import Options
from opinion import Opinion

'''
	#https://play.google.com/store/apps/collection/topselling_free
	#https://play.google.com/store/apps/details?id=com.whatsapp
	#https://play.google.com/store/apps/details?id=com.wb.goog.injustice&showAllReviews=true
	#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	U26fgb O0WRkf oG5Srb C0oVfc n9lfJ M9Bg4d
'''
class Crawler_play_store():

	def __init__(self):
		#options = Options()
		#options.headless = True
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument("--lang=pt-BR")
		options.add_argument('window-size=1200x800')
		#options.binary_location = "/home/rogerio/Applications/chrome-linux/chrome"
		self.driver = webdriver.Chrome(options=options)
		#self.driver = webdriver.Firefox(options=options)

	def main(self, id_app):
		#id_app = "com.whatsapp"
		link_play = "https://play.google.com/store/apps/details?id={}&showAllReviews=true"
		self.driver.get(link_play.format(id_app))
		self.driver.implicitly_wait(5)
		hc = Handle_Comments()
		cont = 0
		inicial = 0
		validos = 0
		while validos <= 5001:
			divs_comments = self.driver.find_elements_by_xpath("//div[@jsmodel = 'y8Aajc']")
			total = len(divs_comments)
			if total == inicial:
				break
			for i in range(inicial, total):
				valido, opiniao = hc.handle(i, id_app, divs_comments[i], self.driver)
				if valido:
					validos+=1
					output = open('reviews/'+id_app+'/'+str(validos)+'.json','w')
					output.write(opiniao.to_json())
					output.close()
				cont+=1
			print("Válidos: " + str(validos) + "; Total: " + str(cont))
			inicial = total
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1)
			try:
				ActionChains(self.driver).move_to_element(divs_comments[-1]).perform()
				self.driver.find_element_by_class_name("PFAhAf").click()
			except NoSuchElementException:
				continue

	def close(self):
		self.driver.close()

'''
	Classe para tratar os comentários
'''
class Handle_Comments():
	def __init__(self):
		pass

	'''
		Executar as operações de extração para os comentários e retornar o objeto
	'''
	def handle(self, id, app ,div_comment, driver):
		self.driver = driver
		autor = div_comment.find_element_by_class_name("X43Kjb").text
		data = div_comment.find_element_by_class_name("p2TkOb").text
		likes = div_comment.find_element_by_class_name("jUL89d").text
		if likes.strip() == '':
			likes = 0
		else:
			likes = int(likes)
		estrelas = len(div_comment.find_elements_by_class_name("vQHuPe"))
		texto = self.extract_text(div_comment)
		if texto.strip() == '':
			return (False, None)
		#link_comment = self.extract_link(div_comment)
		opiniao = Opinion(id, autor , app, data, estrelas, texto, likes, 0)
		return (True, opiniao)

	'''
		Executar as operações para extrair o link do comentário da play store
	'''
	def extract_link(self, elemento):
		# Clicar em Mais opções
		ActionChains(self.driver).move_to_element(elemento).perform()
		botao = elemento.find_element_by_xpath(".//div[@aria-label='Mais opções']")
		botao.click()
		# Clicar em Link para esta análise
		menu = self.driver.find_element_by_xpath("//*[@id='yDmH0d']/div[@class='JPdR6b CblTmf qjTEB']/div/div/content[@aria-label='Link para esta análise']/div[2]/div")
		time.sleep(1)
		menu.click()
		time.sleep(1)
		link = self.driver.current_url
		self.driver.back()
		return link

	'''
		Extrair texto dos comentários
	'''
	def extract_text(self, elemento):
		if self.ler_mais_click(elemento):
			texto = elemento.find_element_by_xpath(".//span[@jsname = 'fbQN7e']").text
		else:
			texto = elemento.find_element_by_xpath(".//span[@jsname = 'bN97Pc']").text
		return texto

	'''
		Verificar se o botão ler mais existe.
	'''
	def ler_mais_exists(self, elemento):
		try:
			elemento.find_element_by_class_name("LkLjZd")
		except NoSuchElementException:
			return False
		return True

	'''
		Executar a operação para clicar em ler mais
	'''
	def ler_mais_click(self, div_comment):
		if self.ler_mais_exists(div_comment):
			ler_mais = div_comment.find_element_by_class_name("LkLjZd")
			ActionChains(self.driver).move_to_element(div_comment).perform()
			time.sleep(0.5)
			ler_mais.click()
			return True
		else:
			return False

if __name__ == '__main__':
	#lista = ['com.b2w.americanas']
	lista = ['com.twitter.android']
	for app in lista:
		print(app)
		crawler = Crawler_play_store()
		crawler.main(app)
		crawler.driver.close()
