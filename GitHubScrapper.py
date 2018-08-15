from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import urllib2
import time
import pymongo
from pymongo import MongoClient
import sys

# Get the host ip, from the arguemnt
# if user didn't pass ant ip, will use localhost
host_ip = "127.0.0.1"
if len(sys.argv) > 1:
    host_ip = sys.argv[1]

print "Start DB"
# Connect to the mongo server
client = MongoClient(host_ip, 27017)
RepoDB = ""
Repos_Collection = ""
try:
    client.server_info()
    RepoDB = client.RepoDB
    #check if 'Repos' collection exists in the db
    # if not, create on
    # and then clear it from values (drop)
    if "Repos" not in RepoDB.list_collection_names():
        RepoDB.create_collection("Repos")
    Repos_Collection =  RepoDB["Repos"]
    Repos_Collection.drop()
except pymongo.errors.ServerSelectionTimeoutError as e:
    print "No mongo Server is up"


print "start Scrapping"
#database is a local list of repos for own use
database = []
#setting up the chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--start-maximized')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.set_window_size(1080, 800)

#connect to github
browser.get("http://github.com/")

search = browser.find_element_by_name("q")
search.send_keys("selenium")
#mesurre time from serach until page load
start_time = time.time()
search.send_keys(Keys.RETURN)
for i in xrange(5):
    #wait until page loads, and then finding the time for page to load
    # by subtracting the time when we searchq hit next from the time now
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "repo-list")))
    print "It took ", time.time() - start_time, " seconds for page to load"
    #sleep for 1 second in order the avoid bug when not all repositories are updated
    time.sleep(1)
    #findind list of elemnts
    repo_list_element = browser.find_element_by_class_name("repo-list")
    all_repos = repo_list_element.find_elements_by_xpath("div")
    for rep in all_repos:
        repo_data = {}
        try:
            #- find title element for the name and the link
            Title = rep.find_element_by_tag_name("a") 
            link = Title.get_attribute("href")
            print link
            #check if not broken link
            #if so, an exception will be raised
            urllib2.urlopen(link)
            
            repo_data["Title"] = Title.text
            #- description
            dec = rep.find_element_by_tag_name("p").text 
            repo_data["Description"] = dec
                
            datetime_element = rep.find_element_by_tag_name("relative-time")
            repo_data["Date_Time"] = datetime_element.get_attribute("datetime") #- For time it self

            #- get the right div which contains the stars and the language    
            right = rep.find_element_by_xpath("div[2]") 
            # - Language
            repo_data["Language"] = right.find_element_by_class_name("text-gray").text 
            #- Stars
            repo_data["Stars"] = right.find_element_by_class_name("pl-2").text

            #- find list of tags
            tags = rep.find_elements_by_class_name("topic-tag") 
            repo_data["Tags"] = [tag.text for tag in tags]

            # add the repo to the collection in the db as dictionary
            database.append(repo_data)
            Repos_Collection.insert(repo_data)
        # In case of broken link  
        except urllib2.HTTPError as e:
            print "Broken link, repos not stored"
        except Exception as e:
            print e
    #finding the 'next'' button, click and mesure time
    next = browser.find_element_by_class_name("next_page")
    # cupturing the time before the action
    start_time = time.time()
    next.click()

#close browser in the end
browser.quit()

for repo in database:
    print repo



