from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime

from send_email import send_email


import os
from dotenv import load_dotenv
load_dotenv()



def login_portal(url, username, password):


	service = webdriver.FirefoxService(executable_path='/usr/local/bin/geckodriver')
	driver = webdriver.Firefox(service=service)

	driver.get(url)

	time.sleep(5)

	username_field = driver.find_element(By.ID, "account") 
	password_field = driver.find_element(By.ID, "password")

	username_field.send_keys(username)
	password_field.send_keys(password)

	# send enter key action
	password_field.send_keys(Keys.RETURN)

	time.sleep(5)
	
	return driver
	
	
def redirct_and_signin(driver):
	# open another tab
	driver.execute_script("window.open('');")  
	driver.switch_to.window(driver.window_handles[1])  

	target_url = "https://portal.nycu.edu.tw/#/redirect/timeclocksign"
	driver.get(target_url)
	
	# wait for timeout
	driver.implicitly_wait(2)
	
	# click on sign in button
	signin_button = driver.find_element(By.ID, "ContentPlaceHolder1_GridView_attend_LinkButton_signIn_0")
	signin_button.click()

	time.sleep(3)

	confirm_signin_button = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$Button_attend")
	confirm_signin_button.click()
	
		
	
	driver.quit()
	
	
def redirct_and_signout(driver):
	# open another tab
	driver.execute_script("window.open('');")  
	driver.switch_to.window(driver.window_handles[1])  

	target_url = "https://portal.nycu.edu.tw/#/redirect/timeclocksign"
	driver.get(target_url)
	
	# wait for timeout
	driver.implicitly_wait(2)
	
	# click on sign out button
	# signout_button = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_GridView_attend_LinkButton_signIn_0"]')  # temporary for weird web content
	signout_button = driver.find_element(By.ID, "ContentPlaceHolder1_GridView_attend_LinkButton_signOut_0")
	signout_button.click()

	time.sleep(3)

	confirm_signout_button = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$Button_attend")
	confirm_signout_button.click()
	
	driver.quit()
	


username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
url = "https://portal.nycu.edu.tw" 


start_time = datetime.strptime("2024/11/25 13:10", "%Y/%m/%d %H:%M")
end_time = datetime.strptime("2024/11/25 17:10", "%Y/%m/%d %H:%M")

schedules = []
schedules.append((start_time, end_time))


for start_time, end_time in schedules:
	print(f"Scheduled login at {start_time} and logout at {end_time}.")

    # Wait until the start time for login
	print(f"Waiting until {start_time} to log in...")
	while datetime.now() < start_time:
		time.sleep(1)
	
	try:
		driver = login_portal(url, username, password)
		redirct_and_signin(driver)
		send_email(f"sucessfully sign in at {datetime.now()}, congrats!!")
		print(f"sucessfully sign in at {datetime.now()}, congrats!!")
	except Exception as e:
		send_email(f"Faild to sign in at {datetime.now()}, {e}")
		driver.quit()
		print(e)
		
    
    # Wait until the end time for logout
	print(f"Waiting until {end_time} to log out...")
	while datetime.now() < end_time:
		time.sleep(1)
	
	time.sleep(60)

	try:
		driver = login_portal(url, username, password)
		redirct_and_signout(driver)
		print(f"sucessfully sign out at {datetime.now()}, congrats!!")
		send_email(f"sucessfully sign out at {datetime.now()}, congrats!!")
	except Exception as e:
		send_email(f"Faild to sign out at {datetime.now()}, {e}")
		print(e)
		

# driver = login_portal(url, username, password)
# redirct_and_signout(driver)



# print(datetime.now() < dt)

# driver.quit()


