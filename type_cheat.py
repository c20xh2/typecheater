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
from selenium.webdriver.common.action_chains import ActionChains


class Racer():

	def __init__(self):

		self.player_username = ''
		self.player_password = ''

		self.skill_level = 0
		self.points = 0
		self.avg_speed = 0
		self.races_total = 0

		self.racer_wpm_goal = 0

		self.minimum_games = 0
		self.maximum_games = 0
		self.accuracy = 0
		self.games_count = 0
		self.number_of_games = 0

		self.headless_browser = False


		self.last_game_speed = 'NA'
		self.last_game_time = 'NA'
		self.last_game_accuracy = 'NA'
		self.last_game_points = 'NA'
		self.last_game_placement = 'NA'

		self.get_configs()
		self.get_number_of_games()
		self.get_driver()

	def get_configs(self):

		with open('configs', 'r') as file:

			for line in file:

				if 'username=' in line:
					self.player_username = line.split('=', 1)[1].strip()
				if 'password=' in line:
					self.player_password = line.split('=', 1)[1].strip()
				if 'wpm=' in line:
					self.racer_wpm_goal = int(line.split('=', 1)[1].strip())
				if 'minimum_games=' in line:
					self.minimum_games = int(line.split('=', 1)[1].strip())
				if 'maximum_games=' in line:
					self.maximum_games = int(line.split('=', 1)[1].strip())
				if 'headless=' in line:
					self.headless_browser = line.split('=', 1)[1].strip()
				if 'accuracy=' in line:
					self.accuracy = int(line.split('=', 1)[1].strip())

	def get_keystroke_delay(self):

		modifier = 18

		try:
			self.minutes = int(self.race_time.split(':')[0])
			self.keystroke_delay = 60 / (self.racer_wpm_goal * modifier)

		except:
			self.seconds = int(self.race_time.split(':')[1])
			self.keystroke_delay = self.seconds / (self.racer_wpm_goal * modifier)

	def get_number_of_games(self):

		self.number_of_games = random.randint(self.minimum_games, self.maximum_games)

	def get_driver(self):

		chrome_options = Options() 
		
		if self.headless_browser == 'True':
			chrome_options.add_argument("--headless") 

		chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
		
		self.driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
		self.driver.set_window_size(1024, 768)


	def login(self):

		print('\n' * 100)
		print('[|] Login in {}'.format(self.player_username))

		self.driver.get('https://play.typeracer.com/')

		time.sleep(5)

		sign_in = self.driver.find_elements_by_tag_name('a')

		for elem in sign_in:
			if 'Sign In' in elem.text:
				elem.click()
	      
		user_box = self.driver.find_element_by_name('username')
		password_box = self.driver.find_element_by_name('password')
		submit = self.driver.find_element_by_class_name('gwt-Button')
		
		user_box.send_keys(self.player_username)
		password_box.send_keys(self.player_password)

		submit.click()

	def get_racer_infos(self):

		self.skill_level = self.driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[2]/a').text
		self.points = self.driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[5]').text
		self.avg_speed = self.driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[3]/table/tbody/tr/td[1]/div').text
		self.races_total = self.driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr/td[3]/div/table/tbody/tr[2]/td[4]').text

	def enter_first_race(self):
		enter_race = self.driver.find_element_by_xpath('//*[@id="dUI"]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a')
		enter_race.click()

	def wait_for_countdown(self):
		try:
			self.driver.find_element_by_class_name('countdownPopup')
		except KeyboardInterrupt:
			sys.quit()
		except Exception as e:
			self.ready = True

	def print_stats(self):

		print('\n'*100)
		print('[{}/{}] {} \n\n\t\tSkill Level: {} | Avg Speed: {} | races_total: {} | Points: {}'.format(
			self.games_count, 
			self.number_of_games, 
			self.player_username, 
			self.skill_level, 
			self.avg_speed, 
			self.races_total, 
			self.points))
		print('\n\t\tLast game placement: {}'.format(self.last_game_placement))
		print('\n\t\tLast game speed: {}\n\t\tLast game time : {}\n\t\tLast game accuracy: {}\n\t\tLast game points: {}'.format(self.last_game_speed, self.last_game_time, self.last_game_accuracy, self.last_game_points))

	def check_typo(self):

		roll = random.randint(0, self.accuracy)
		
		if roll <= 1:
			return True
		else:
			return False

	def race_init(self):

		self.games_count +=1
		self.print_stats()
		time.sleep(4)

		self.ready = False

		while not self.ready:
			self.wait_for_countdown()

		self.race_time = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/div/span').text
		self.race_text = self.driver.find_element_by_class_name('inputPanel').text.replace('change display format','').strip()
		self.race_input_box = self.driver.find_element_by_class_name('txtInput')
		self.race_words_count = len(self.race_text)
		
		self.get_keystroke_delay()

		print('\n #########')
		print('\n Current Race: {} characters | Delay: {:.3f} sec'.format(self.race_words_count, self.keystroke_delay))
		print('\n {}'.format(self.race_text))
		print('\n #########\n')
		
		self.active_game = True

	def race(self):

		try:
			
			hover = ActionChains(self.driver).move_to_element(self.race_input_box)
			hover.perform()
			typo = False
			i = 0
			
			while self.active_game:

				if i >= self.race_words_count:
					self.race_input_box.click()
					self.active_game = False

				typo = self.check_typo()
				
				if typo:

					letter = random.choice(string.ascii_letters)
					self.race_input_box.send_keys(letter)	
					time.sleep(self.keystroke_delay)
					self.race_input_box.send_keys('\b')
				
				else:
					self.race_input_box.send_keys(self.race_text[i])
					i += 1
				
				time.sleep(self.keystroke_delay)

		except Exception as e:
			pass

	def check_challenged(self):

		self.challenged = False
		
		time.sleep(3)

		try:
			self.challenged = self.driver.find_element_by_class_name('challengePrompt')
		except Exception as e:
			pass
		
		if challenged:
			self.driver.close()
			sys.exit()

	def get_results(self):
		time.sleep(3)
		try:		
			self.last_game_speed = self.driver.find_element_by_xpath('//*/table/tbody/tr[4]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/div/div').text
			self.last_game_time = self.driver.find_element_by_xpath('//*/table/tbody/tr[4]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr[2]/td[2]/div/span').text
			self.last_game_accuracy = self.driver.find_element_by_xpath('//*/table/tbody/tr[4]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/div').text
			self.last_game_points = self.driver.find_element_by_xpath('//*/table/tbody/tr[4]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr[4]/td[2]/div/div').text
			self.last_game_points = self.driver.find_element_by_xpath('//*/table/tbody/tr[4]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr[4]/td[2]/div/div').text
			self.last_game_placement = self.driver.find_element_by_xpath('//*/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div/div[1]').text

		except Exception as e:
			print(e)
			time.sleep(60)
	def play_again(self):

		new_game = False

		while not new_game:
			
			try:
				play_again = self.driver.find_elements_by_tag_name('a')
				for elem in play_again:
					if 'Race Again' in elem.text:
						elem.click()
						new_game = True
			except Exception as e:
				pass

racer = Racer()

racer.login()
time.sleep(3)

racer.get_racer_infos()
racer.enter_first_race()

while racer.games_count < racer.number_of_games:

	racer.race_init()
	racer.race()
	racer.get_racer_infos()
	racer.get_results()
	racer.play_again()

racer.driver.quit()