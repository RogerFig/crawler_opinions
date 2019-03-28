from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from selenium.webdriver.firefox.options import Options

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
		options.add_argument('window-size=1200x600')
		self.driver = webdriver.Chrome(options=options)
		#self.driver = webdriver.Firefox(options=options)

	def main(self):
		id_app = "com.whatsapp"
		link_play = "https://play.google.com/store/apps/details?id={}&showAllReviews=true"
		self.driver.get(link_play.format(id_app))
		self.driver.implicitly_wait(10)
		cont = 0
		while True:
			quant_0 = len(self.driver.find_elements_by_class_name("zc7KVe"))
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			#time.sleep(1)
			print("Loops: %d" % cont)
			cont+=1
			try:
				quant_1 = len(self.driver.find_elements_by_class_name("zc7KVe"))
				print("antes: %d depois: %d " % (quant_0, quant_1))
				if quant_1 == quant_0 and quant_1 >= 10000:
					break
				self.driver.find_element_by_class_name("PFAhAf").click()
			except NoSuchElementException:
				continue

	def close(self):
		self.driver.close()

if __name__ == '__main__':
	crawler = Crawler_play_store()
	crawler.main()