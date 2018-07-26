import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_driver():
	driver = webdriver.Chrome('./chromedriver')
	driver.set_window_size(1024, 768)
	return driver


def login(driver):
	user = ''
	password =''

	print('[|] Login in')

driver.get('https://play.typeracer.com/');
	time.sleep(5)

	sign_in = driver.find_elements_by_tag_name('a')

	for elem in sign_in:
		if 'Sign In' in elem.text:
			elem.click()
      
	user_box = driver.find_element_by_name('username')
	password_box = driver.find_element_by_name('password')
	submit = driver.find_element_by_class_name('gwt-Button')
	user_box.send_keys(user)
	password_box.send_keys(password)

	submit.click()

def start_first_race(driver):
	enter_race = driver.find_element_by_xpath('//*[@id="dUI"]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a')
	enter_race.click()

def racing(driver):

	while True:
		print('\n'*100)
		print('[|] Waiting for green light...')

		time.sleep(4)
		ready = False

		while not ready:
			try:
				driver.find_element_by_class_name('countdownPopup')
			except KeyboardInterrupt:
				sys.quit()
			except Exception as e:
				ready = True
				print("\n[!] Let's go !!!")
				pass

		type_this = driver.find_element_by_class_name('inputPanel')

		type_this = type_this.text.replace('change display format','').strip()
		
		print('\n## Race text:\n\n{}'.format(type_this))
		input_box = driver.find_element_by_class_name('txtInput')


		if len(type_this) >= 400:
			delay = 0.55

		elif len(type_this) >= 300: ### 119 wpm
			delay = 0.44

		elif len(type_this) >= 200:
			delay = 0.3 ### 119

		else:
			delay = 0.45

		print('\n[!!!] Typing !!! ({}) characters | Delay: {} sec'.format(len(type_this), delay))

		try:
			for letter in type_this:
				input_box.send_keys(letter)
				time.sleep(0.065)
		except Exception as e:
			pass


		print('Getting ready for next race...')

		challenged = False
		time.sleep(3)

		try:
			challenged = driver.find_element_by_class_name('challengePrompt')
		except Exception as e:
			pass
		
		if challenged:
			whatsup = input('\n[*]You are challenged, what would you like to do ?: [q:quit|c:continue]')

			if whatsup == 'q':
				sys.exit()
			elif whatsup == 'c':
				pass
		ready = False
		while not ready:
			try:
				play_again = driver.find_elements_by_tag_name('a')
				for elem in play_again:
					if 'Race Again' in elem.text:
						elem.click()
						ready = True
						print('\n!!! AGAIN !!!\n')
			except Exception as e:
				pass

driver = get_driver()
print('\n'* 100)
print('[+] Starting script...\n')
login(driver)
start_first_race(driver)
racing(driver)
driver.quit()
