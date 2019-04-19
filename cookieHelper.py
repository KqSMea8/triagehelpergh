from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import os

class CookieClass():
	def __init__(self, username, password):
		self.userName = username
		self.passWord = password

	def update_cookie(self):

		driver = webdriver.Chrome()
		driver.get('http://voyager.intra.xiaojukeji.com/static/management/#/trip/list')
		# wait 20s until successfully login
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))) 
		user_name = driver.find_element_by_xpath('//*[@id="username"]')
		user_name.send_keys(self.userName)
		pass_word = driver.find_element_by_xpath('//*[@id="password"]')
		pass_word.send_keys(self.passWord)
		submit = driver.find_element_by_xpath('//*[@id="submit"]')
		submit.click()
		# wait 20s
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@class="username"]')))

		# get cookies
		cookie_list = driver.get_cookies()
		expiry_time = int(cookie_list[0]['expiry'])
		driver.close()
		driver.quit()
		cookies_pre = ";".join([item["name"] + "=" + item["value"] + "" for item in cookie_list])
		cookies = {}
		for line in cookies_pre.split(';'):
		    name,value=line.strip().split('=',1)  
		    cookies[name]=value
		cookies['expiry'] = expiry_time
		#save to file()
		js = json.dumps(cookies)   
		file = open('cookies.txt', 'w')  
		file.write(js)  
		file.close()   
		return cookies

	def get_cookie(self):
		current_time = int(time.time())
		if not os.path.exists('cookies.txt'):
			cookies = self.update_cookie()
		else:
			f = open('cookies.txt', 'r')
			content = f.readline()
			cookies = json.loads(content)
			expiry_time = cookies['expiry']
			if current_time > expiry_time:
				cookies = self.update_cookie()

		cookies.pop('expiry')
		return cookies




	

if __name__ == "__main__":
	pass

