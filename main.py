import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# Type in course name for professor webscraping
course_name = input('Please input course name in format XXXX000 (four digits and 3 numbers): ')

# Set up selenium endpoints, constants, ETC
s = Service('/Users/ianveilleux/development/chromedriver')
driver = webdriver.Chrome(service=s)
driver.get(f"https://contacts.ucalgary.ca/info/ha/courses/w21/{course_name}?destination=courses/w21")

PROF_NAME_ENDPOINT = '//*[@id="root"]/div/div/div[1]/div/header/div[2]/div[3]/div[1]/div[2]/div/div[1]/div[2]/input'
SCHOOL_INPUT_ENDPOINT = '//*[@id="root"]/div/div/div[1]/div/header/div[2]/div[3]/div[1]/div[2]/div/div[' \
                        '2]/div/div/div[2]/input '
BUTTON_ENDPOINT = '/html/body/div[5]/div/div/button'
CHECK_SCHOOL_ENDPOINT = '//*[@id="root"]/div/div/div[4]/div[1]/div[3]/a/div/div[2]/div[2]/div[2]'

# Find all elements in course information table
name = driver.find_elements(By.XPATH, '//*[@id="uofc-table-1"]/tbody/tr')
names_list = []

# Loop through each row in table, isolate the first and last names of professors from list of all text
for table_row in name:
    lists = table_row.text.split()

    # try to grab first and last name and append tuple to list.
    try:
        # checks if the last element in the list is not 'web based' (skips unneeded text)
        if lists[::-1][0] != 'BASED':
            if (lists[::-1][1] + ' ' + lists[::-1][0]) not in names_list:
                names_list.append((lists[::-1][1] + ' ' + lists[::-1][0]))
    except IndexError:
        # continue program if there are no more elements in the table
        continue

name_score_list = []
test_dict = {}
# set up initial RMF webpage and click on the cookies button (out of loop so not repeated)
driver.get('https://www.ratemyprofessors.com/search/teachers?query=')
cookies_button = driver.find_element(By.XPATH, BUTTON_ENDPOINT)
cookies_button.click()
for name in names_list:
    # grab first and last name as separate variables, and query RMF
    first_name = name.split()[0]
    last_name = name.split()[1]
    driver.get(f"https://www.ratemyprofessors.com/search/teachers?query={first_name}%20{last_name}")

    # create list of web items
    check_school = driver.find_elements(By.XPATH, CHECK_SCHOOL_ENDPOINT)
    # loop through all profs, and check if prof is from U of C
    for professor in check_school:
        if professor.text == 'University of Calgary':
            # grab score, and number of ratings
            get_score_path = '//*[@id="root"]/div/div/div[4]/div[1]/div[3]/a/div/div[1]/div/div[2]'
            get_score = driver.find_element(By.CLASS_NAME, "CardNumRating__CardNumRatingNumber-sc-17t4b9u-2")
            num_of_ratings_path = 'CardNumRating__CardNumRatingCount-sc-17t4b9u-3'
            get_num_of_ratings = driver.find_element(By.CLASS_NAME, num_of_ratings_path)

            # name_score_list.append((name, float(get_score.text)))
            # create new dictionary entries with prof name, score, and number of ratings
            dict_entry = {
                name: {
                    'score': float(get_score.text),
                    'number of ratings': int(get_num_of_ratings.text.split()[0])
                }
            }
            test_dict.update(dict_entry)

        else:
            continue

# TO-DOs: Weigh the # of ratings so profs with a small number of ratings aren't unfairly weighted
    # Tell you the prof with the highest score vs number of ratings, and recommend them.
    # Inform you which lecture section they teach, and what time
    # Maybe look into sentiment analysis on the rate my prof ratings
print(test_dict)


