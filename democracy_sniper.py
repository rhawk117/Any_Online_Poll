from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
from datetime import datetime 
from threading import Thread
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import requests as req
from pprint import pprint
from queue import Queue
import traceback
import random
from bs4 import BeautifulSoup
import threading
from queue import Queue


# random name and email generator (lol)
names = [
    "Olivia", "Emma", "Amelia", "Sophia", "Charlo", "Lu", "Isabel", "Le", "Luna", "Evelyn", 
    "Gianna", "Lily", "Aria", "Aurora", "Ellie", "Harper", "Mila", "Sofia", "Camila", "Layla", 
    "Nova", "Eliana", "Ella", "Violet", "Hazel", "Willow", "Chloe", "Ma", "Scarle", "Penelo", 
    "Eleano", "Elena", "Avery", "Nora", "Abigai", "Emily", "Maya", "Isla", "Delila", "Naomi", 
    "Elizab", "Grace", "Zoey", "Emilia", "Riley", "Mi", "Paisle", "Athena", "Leilan", "Madiso", 
    "Victor", "Ayla", "Stella", "Lucy", "Kinsle", "Iris", "Gabrie", "Lainey", "Aaliya", "Sereni", 
    "Addiso", "Alice", "Bella", "Sadie", "Sophie", "Amara", "Autumn", "Summer", "Emery", "Everly", 
    "Valent", "Hannah", "Brookl", "Madely", "Natali", "Leah", "Maria", "Savann", "Amira", "Aubrey", 
    "Jade", "Jasmin", "Eden", "Skylar", "Josie", "Clara", "Adelin", "Ellian", "Millie", "Lillia", 
    "Melody", "Sarah", "Aa", "Ruby", "Freya", "Lyla", "Adalyn", "Lilian", "Daisy", "Nevaeh"
]
emails_ext = ['@gmail.com','@yahoo.com','@outlook.com', '@hotmail.com','@comast.net']
last_names = [
  'King',
 'Thompson',
 'Lopez',
 'Brown',
 'Baker',
 'Campbell',
 'King',
 'Lee',
 'Jones',
 'Wright',
 'Robinson',
 'Campbell',
 'Roberts',
 'Mitchell',
 'Lewis',
 'Lopez',
 'Rivera',
 'Wright',
 'Young',
 'King',
 'Clark',
 'Nelson',
 'Wright',
 'Ramirez',
 'Thomas',
 'Baker',
 'Rivera',
 'Walker',
 'Harris',
 'Thompson',
 'Nelson',
 'Smith',
 'Brown',
 'Brown',
 'Baker',
 'Ramirez',
 'Roberts',
 'Hill',
 'Martinez',
 'Ramirez',
 'Gonzalez',
 'Martin',
 'Scott',
 'Moore',
 'Martinez',
 'Mitchell',
 'Miller',
 'Flores',
 'Anderson',
 'Young'
]

def generate_email(first: str, last: str, emails_ext: list):
  sep = '_' if random.randint(1,2) == 1  else '-'
  return f"{first}{last}{sep}{random.choice(emails_ext)}"
  
def get_random(first: list, last: list):
  return (random.choice(first),random.choice(last))

# API URLS
post_url = '[REDACTED]'
form_url = '[REDACTED]'
auth_token_url = '[REDACTED]'


# def get_authenticity_token(url):
#     auth_tag = req.get(auth_token_url).content
#     soup = BeautifulSoup(auth_tag, 'html.parser')
#     input_element = soup.find('input', {'name': 'authenticity_token'})
#     return input_element.get('value') if input_element else None


# ----------------------------------------------------------------------------------------------------------------------------
# CSS SELECTORS

first_slctor = '#field_310_25636'
lst_slctor = '#field_311_25636'
email_slctor = '#field_312_25636'

check_box_slctor = '#field_316_25636 > div:nth-child(2) > div:nth-child(3) > label:nth-child(2)'
submit_slctor = '.fsFormSubmitButton'
#----------------------------------------------------------------------------------------------------------------------------
class Subimission:
  def __init__(self):
    self.first, self.last = get_random(names, last_names)
    self.email = generate_email(self.first, self.last, emails_ext) 
    
  def __str__(self) -> str:
    return f"SUBMISSION INFO\nFirst: {self.first}\nLast: {self.last}\nEmail: {self.email}\n\n\n"
#----------------------------------------------------------------------------------------------------------------------------
def log_error(e:Exception, slctor) -> None:
    with open('error.log', 'a') as f:
        f.write(f'[SELECTOR { slctor }]:  failed to proces...\n\n\n')
        f.write(f'[EXCEPTION]: { e }\n')
        f.write(traceback.format_exc())
        f.write('\n\n' + "*"*50)
        
def init_driver():
  # hide the automation (xd)
  options = webdriver.ChromeOptions()
  options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
  options.page_load_strategy = 'none'
  options.add_argument("--window-size=1920,1080")
  options.add_argument("--start-maximized")  # start maximized
  options.add_argument("--disable-extensions")  
  options.add_argument("--disable-popup-blocking")  
  options.add_argument("--disable-gpu")  
  options.add_argument("--no-sandbox")  
  options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
  options.add_experimental_option("useAutomationExtension", False)
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("--disable-blink-features=AutomationControlled")

    # Enable verbose logging for troubleshooting (Optional)
  options.add_argument("--verbose")
  options.add_argument("--log-level=0")
  
  print("[i] Driver initialized [i]")
  return webdriver.Chrome(options=options)


def input_action(driver, slctor, form_input, Actions):
  target_elm = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(By.CSS_SELECTOR, slctor)
  )
  Actions.move_to_element(target_elm).click().send_keys(form_input).perform() 


def driver_logic(first, last, email):
    driver = init_driver()
    Actions = ActionChains(driver)
    try:
      with driver:
        driver.get(form_url)
        
        input_action(driver, first_slctor, first, Actions)
        print(f'[i] Sent { first } input to First Name field')

        input_action(driver, lst_slctor, last, Actions)
        print(f'[i] Sent {last} input to Last Name field')
        
        input_action(driver, email_slctor, email, Actions)
        print(f'[i] Sent {email} input to Email field')
        
        
        check_box = WebDriverWait(driver, 10).until(
          lambda x: x.find_element(By.CSS_SELECTOR, check_box_slctor)
        )
        
        Actions.move_to_element(check_box).click().perform()
        
        submit_btn = WebDriverWait(driver, 10).until(
          lambda x: x.find_element(By.CSS_SELECTOR, submit_slctor)
        )
        Actions.move_to_element(submit_btn).click().perform()
        
    except Exception as e:
      print(f"Exception occured with the driver...")
      log_error(e, "unknown")  
      driver.quit()
      return 
    finally:        
      driver.quit()

# old send_input function (didn't work consistently due to AJAX)
# def send_input(driver, slctor, val):
#   try:
#     delay = random.randint(10,15)
#     tag = WebDriverWait(driver, delay).until(
#       lambda x: x.find_element(By.CSS_SELECTOR, slctor)
#     )
#     tag.send_keys(val)
#     return True

#   except Exception as e:
#     print(f"Exception occured with the CSS selector of {slctor}")
#     log_error(e, slctor)  
#     driver.quit()
#     return False

#   finally:
#     driver.quit()
  
def convert_list_q(alist: list):
  rtrnList = Queue()
  for i in alist:
    rtrnList.put(i)
  return rtrnList

def get_submissions(total: int) -> Queue:
  submissions = convert_list_q([Subimission() for i in range(total)])
  return submissions
  
def a_vote(voter: Subimission) -> None:
    driver_logic(voter.first, voter.last, voter.email)
  
def thread_task(task_queue: Queue) -> None:
  while not task_queue.empty():
    vote_info = task_queue.get()
    try:
        a_vote(vote_info)
    except Exception as e:
        print(f'Error: { e }')
        log_error(e, vote_info)
    finally:  
        task_queue.task_done()
        
  
def start_threads(task_queue: Queue, thread_count: int) -> None:
  threads = []
  for _ in range(thread_count):
    try:
      thread = Thread(target=thread_task, args=(task_queue,))
      threads.append(thread)
      thread.start()
      
    except Exception as e:
      print(f'Error: { e }')
      log_error(e, task_queue)
      
  for thread in threads:
    thread.join()
    
  print("[i] All Threads have completed their tasks [i]")
  
  
def main() -> None:
  task_queue = get_submissions(50) # specify num of votes
  start_threads(task_queue, 5)
  

if __name__ == "__main__":
  main()