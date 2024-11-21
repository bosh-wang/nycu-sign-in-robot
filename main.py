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
	
def get_schedules():
    schedules = []
    print("Enter multiple login/logout schedules in the format 'MM/DD HH:MM to HH:MM'. ex: 10/15 13:00 to 18:00.  Type 'done' to finish.")
    while True:
        schedule = input("Enter schedule: ")
        if schedule.lower() == "done":
            break
        try:
            # Parse input (e.g., "11/5 12:00 to 16:00")
            date, times = schedule.split()
            start_time_str, end_time_str = times.split("to")
            start_time = datetime.strptime(f"{date} {start_time_str.strip()}", "%m/%d %H:%M")
            end_time = datetime.strptime(f"{date} {end_time_str.strip()}", "%m/%d %H:%M")
            schedules.append((start_time, end_time))
        except ValueError:
            print("Invalid format. Please use 'MM/DD HH:MM to HH:MM'.")
    return schedules
	

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
url = "https://portal.nycu.edu.tw" 

#schedules = get_schedules()


start_time = datetime.strptime("2024/11/25 13:00", "%Y/%m/%d %H:%M")
end_time = datetime.strptime("2024/11/25 17:00", "%Y/%m/%d %H:%M")

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


