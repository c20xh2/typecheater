import time
import sys
import random
import string
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_configs():
	configs = {}

	with open('configs', 'r') as file:
		for line in file:
			if 'username=' in line:
				configs['username'] = line.split('=', 1)[1].strip()
			if 'password=' in line:
				configs['password'] = line.split('=', 1)[1].strip()
			if 'wpm=' in line:
				configs['wpm'] = int(line.split('=', 1)[1].strip())
			if 'minimum_games=' in line:
				configs['minimum_games'] = int(line.split('=', 1)[1].strip())
			if 'maximum_games=' in line:
				configs['maximum_games'] = int(line.split('=', 1)[1].strip())
			if 'headless=' in line:
				configs['headless'] = line.split('=', 1)[1].strip()


	return configs
 
def should_i_run():
	return True


def get_number_of_games(configs):

	number_of_games = random.randint(configs['minimum_games'], configs['maximum_games'])
	return number_of_games

def get_driver(configs):

	chrome_options = Options() 
	
	if configs['headless'] == 'True':
		chrome_options.add_argument("--headless") 
	
	driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

	driver.set_window_size(1024, 768)
	return driver

def login(driver, configs):

	print('[|] Login in')

	driver.get('https://play.typeracer.com/')
	time.sleep(5)

	sign_in = driver.find_elements_by_tag_name('a')

	for elem in sign_in:
		if 'Sign In' in elem.text:
			elem.click()
      
	user_box = driver.find_element_by_name('username')
	password_box = driver.find_element_by_name('password')
	submit = driver.find_element_by_class_name('gwt-Button')
	user_box.send_keys(configs['username'])
	password_box.send_keys(configs['password'])

	submit.click()

def print_stats(games_count, number_of_games):
	print('\n'*100)

	skill_level = driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[2]/a').text
	points = driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[5]').text
	avg_speed = driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[3]/table/tbody/tr/td[1]/div').text
	races = driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[4]').text

	print('[{}/{}] Skill Level: {} | Avg Speed: {} | Races: {} | Points: {}'.format(games_count, number_of_games, skill_level, avg_speed, races, points))

def start_first_race(driver):
	enter_race = driver.find_element_by_xpath('//*[@id="dUI"]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a')
	enter_race.click()


def get_delay(race_text, race_time, configs):

	wpm = configs['wpm']

	modifier = 18

	try:
		minutes = int(race_time.split(':')[0])
		delay = 60 / (wpm * modifier)
	except:
		seconds = int(race_time.split(':')[1])
		delay = seconds / (wpm * modifier)



	return delay

def check_typo():

	roll = random.randint(0, 15)
	
	if roll <= 1:
		return True
	else:
		return False



def racing(driver, configs):

	games_count = 0
	number_of_games = get_number_of_games(configs)

	while games_count < number_of_games:
		
		games_count +=1

		print_stats(games_count, number_of_games)

		time.sleep(4)
		
		ready = False

		while not ready:

			try:
				driver.find_element_by_class_name('countdownPopup')
			except KeyboardInterrupt:
				sys.quit()
			except Exception as e:
				ready = True
				pass

		race_time = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/div/span').text
		race_text = driver.find_element_by_class_name('inputPanel').text.replace('change display format','').strip()

		input_box = driver.find_element_by_class_name('txtInput')
		
		delay = get_delay(race_text, race_time, configs)
		
		race_words = len(race_text)
		print('\n Current Race: {} characters | Delay: {:.3f} sec'.format(race_words, delay))

		try:

			typo = False
			typing_game = True

			i = 0

			while typing_game:

				if i >= len(race_text):
					input_box.click()
					typing_game = False

				typo = check_typo()
				
				if typo:
					letter = random.choice(string.ascii_letters)
					input_box.send_keys(letter)
					time.sleep(delay)
					input_box.send_keys('\b')
				
				else:
					input_box.send_keys(race_text[i])
					i += 1
				time.sleep(delay)

		except Exception as e:
			pass

		challenged = False
		time.sleep(3)

		try:
			challenged = driver.find_element_by_class_name('challengePrompt')
		except Exception as e:
			pass
		
		if challenged:
			sys.exit()

		ready = False
		
		while not ready:
			
			try:
				play_again = driver.find_elements_by_tag_name('a')
			
				for elem in play_again:
					if 'Race Again' in elem.text:
						elem.click()
						ready = True

			except Exception as e:
				pass


run = should_i_run()
configs = get_configs()
if run:
	driver = get_driver(configs)
	print('\n'* 100)
	print('[+] Starting script...\n')
	login(driver,configs)
	start_first_race(driver)
	racing(driver,configs)
	driver.quit()
