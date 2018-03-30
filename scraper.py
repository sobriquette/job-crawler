from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException

import os
import csv

JOBS_OF_INTEREST = {'Engineer', 'Software', 'Security', 'Developer'}
JOB_TITLES = []
JOB_LINKS = []

def update_job_titles_and_links(web_element):
	job_title = web_element.text
	job_link = web_element.get_attribute("href")
	words_in_title = set(job_title.split())
	if len(JOBS_OF_INTEREST & words_in_title) > 0:
		JOB_TITLES.append(job_title)
		JOB_LINKS.append(job_link)

def scrape():
	driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))
	url = "https://careers.google.com/jobs#t=sq&q=j&li=20&l=false&jlo=en-US&jl=37.7749295%3A-122.41941550000001%3ASan+Francisco%2C+CA%2C+USA%3AUS%3A%3A7.6750685520230215%3ALOCALITY%3A%3A%3A%3A%3A%3A&jld=20&"
	driver.get(url)

	while True:
		try:
			wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/div[2]/div/div[1]')))
			web_elements_by_job_title = driver.find_elements_by_class_name("sr-title")
			for we in web_elements_by_job_title:
				update_job_titles_and_links(we)

			try:
				next_btn = driver.find_element_by_xpath('//*[@aria-label="Next page"]')
				next_btn.click()
			except ElementNotVisibleException:
				print("No more pages to check")
				break
		except TimeoutError:
			print("Loading took too long")
			break
	driver.quit()

def create_csv():
	jobs = zip(JOB_TITLES, JOB_LINKS)
	file = open('jobs.csv', 'w')
	with file:
		writer = csv.writer(file)
		writer.writerow(['Job Title', 'URL'])
		writer.writerows(jobs)

def main():
	scrape()
	create_csv()