from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import chevron
import getpass
import csv

REPOSITORY = "ibmcom"
TIMEOUT = 10

class ReadmeAutomation:
	def __init__(self, browser) -> None:
		options = None
		if browser:
			options = webdriver.ChromeOptions()
			options.binary_location = browser
		self.browser = webdriver.Chrome(options=options)

	def login_to_dockerhub(self, user, pswd) -> None:
		self.browser.get("https://login.docker.com/u/login")
		username = self.browser.find_element(By.NAME, "username")
		username.clear()
		username.send_keys(user)
		username.send_keys(Keys.RETURN)
		password = self.browser.find_element(By.NAME, "password")
		password.clear()
		password.send_keys(pswd)
		password.send_keys(Keys.RETURN)
		WebDriverWait(self.browser, TIMEOUT).until(
			EC.presence_of_element_located((By.XPATH, "//span[@data-testid='navBarUsernameDropdown']"))
		)

	def get_repositories_urls(self) -> list:
		self.browser.get(f"https://hub.docker.com/repositories/{REPOSITORY}")
		try:
			repos = WebDriverWait(self.browser, TIMEOUT).until(
				EC.presence_of_all_elements_located((By.XPATH, "//a[@data-testid='repositoryRowLink']"))
			)
			return [ {
					'url': repo.get_attribute("href"),
					'image': f'icr.io/ppc64le-oss/{repo.get_attribute("href").split("/")[-1]}'
				} for repo in repos
			]
		except TimeoutException:
			print("Failed to get repositories")

	def accept_cookie_consent(self) -> None:
		try:
			cookies = WebDriverWait(self.browser, TIMEOUT).until(
				EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
			)
			cookies.click()
		except TimeoutException:
			print("Cookie consent dialogue not found, skipping consent")
	
	def update_readme(self, input_file) -> None:
		self.accept_cookie_consent()				# Required to avoid obstruction of button visibility
		with open('README.mustache', 'r') as template:
			if input_file:
				with open(input_file) as csv_file:
					repos = []
					for row in csv.DictReader(csv_file):
						repos.append({
							'url': f'https://hub.docker.com/repository/docker/{REPOSITORY}/{row["name"]}',
							'image': row["image"]
						})
			else:
				repos = self.get_repositories_urls()
			for repo in repos:
				self.browser.get(repo["url"])
				try:
					edit = WebDriverWait(self.browser, TIMEOUT).until(
						EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='editRepoReadme']"))
					)
					edit.click()
					textarea = self.browser.find_element(By.TAG_NAME, "textarea")
					textarea.clear()
					readme = chevron.render(template, {
						# Add any variables defined inside template here in key:value pairs
						# key = variable name in template
						# value = data to be replaced in generated README
						'image': repo["image"]
					})
					textarea.send_keys(readme)
					update = self.browser.find_element(By.XPATH, "//button[text()='Update']")
					update.click()
				except TimeoutException:
					print(f'Failed to update README for {repo["url"]}')

if __name__ == "__main__":
	user = input("Enter Docker Hub Username: ")
	pswd = getpass.getpass("Enter Docker Hub Password: ")
	browser = input("Chromium-based browser binary path (Empty if browser is Chrome): ")
	input_file = input("Input CSV file (Empty if running on whole repository): ")
	ra = ReadmeAutomation(browser=browser)
	ra.login_to_dockerhub(user=user, pswd=pswd)
	ra.update_readme(input_file=input_file)
