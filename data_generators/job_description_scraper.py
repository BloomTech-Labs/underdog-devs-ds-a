"""Scrape LinkedIn's Job Postings"""

import copy
import os
import time
from datetime import datetime
from getpass import getpass
from pathlib import Path
from urllib import parse

import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def combine_individual_datasets(folder_date):
    """
    Loop through a specific folder in the "job-descriptions"
    folder and combine all csv's into one big csv containing
    all job details from each individual csv.

    Args:
        folder_date (str): the date of a previous scrape
        performed, in this format: "%Y-%m-%d". Example
        below.
            "2022-03-19"
        You can find the dates of all previous scrapes
        by looking in the folder "job_descriptions".
        In that folder, you will find sub-folders titled
        like "scraped_2022-03-19".

    Returns:
        None.
    """
    jobs_path = f'data_generators/job_descriptions/scraped_{folder_date}/'
    encoded_filepath = os.fsencode(jobs_path)
    dataframe_list = []
    for file in os.listdir(encoded_filepath):
        filename = os.fsdecode(file)
        if filename != f'all_scraped_jobs_{folder_date}.csv':
            # Get actual path of csv
            dataset_path = os.path.join(jobs_path, filename)
            data_df = pd.read_csv(dataset_path, encoding='utf-8')
            dataframe_list.append(data_df)
    all_jobs_df = pd.concat(dataframe_list).reset_index(drop=True)
    all_jobs_df.to_csv(
        f"{jobs_path}/all_scraped_jobs_{folder_date}.csv",
        encoding='utf-8',
        index=False)
    print('Successfully saved combined dataset!')


class JobScraper:
    """
    This class opens Google Chrome and logs into the user's
    LinkedIn account. It can be used to scrape a job opening's:
    company name, job title, location, and job description.

    Standard order of methods should be called after instantiating
    the object with a command like "scraper = JobScraper()":

    1. Log into LinkedIn:
        scraper.login_to_linkedin()

    2. Scrape LinkedIn and save results to a csv:
        scraper.scrape_and_save_to_csv()

    Please read the docstring of each method above to know
    more about their arguments.
    """

    def __init__(self):
        """
        Load environment variables, default job title
        search terms, and other instance variables.

        Args:
            None.

        Returns:
            None.
        """
        # Load LinkedIn username and password from .env file
        load_dotenv()
        self.search_terms = [
            "data%20scientist",
            "machine%20learning%20engineer",
            "data%20engineer",
            "web%20developer",
            "frontend%20developer",
            "backend%20developer",
            "devops",
            "software%20engineer"
        ]
        self.browser = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()))
        self.linkedin_jobs = None
        # Create new folder with today's date so the data
        # stored is not overwritten the next time the
        # function runs.
        self.today = datetime.today().strftime('%Y-%m-%d')
        if os.path.exists(
                f"data_generators/job_descriptions/scraped_{self.today}"):
            print(f"""Folder data_generators/job_descriptions/scraped_{self.today}
                    already exists!""")
        else:
            os.mkdir(f"data_generators/job_descriptions/scraped_{self.today}")
        self.folder_path = Path(
            f"data_generators/job_descriptions/scraped_{self.today}"
        )
        self.scraped_list = []
        self.curpath = os.getcwd()

    def login_to_linkedin(self):
        """
        Login to LinkedIn.com.

        Args:
            None.

        Returns:
            None.
        """
        if 'LINKEDIN_USER' in os.environ:
            linkedin_user = os.environ['LINKEDIN_USER']
        else:
            linkedin_user = input("Enter your LinkedIn email: ")
        if 'LINKEDIN_PASS' in os.environ:
            linkedin_pass = os.environ['LINKEDIN_PASS']
        else:
            linkedin_pass = getpass("Enter your password (hidden): ")
        self.browser.get("https://www.linkedin.com")
        # Auto-input username and password on login page
        username = self.browser.find_element(By.ID, "session_key")
        username.send_keys(linkedin_user)
        password = self.browser.find_element(By.ID, "session_password")
        password.send_keys(linkedin_pass)
        # Click login button
        login_button = self.browser.find_element(
            By.CLASS_NAME, "sign-in-form__submit-button")
        login_button.click()

    def load_full_page(self):
        """
        We need to load all 25 jobs displayed on the job's page
        in order to scrape their details. LinkedIn needs a user
        to scroll through the job's page to load all 25 jobs.
        This function accomplishes the loading automatically.

        Args:
            None.
                However, you must have a valid LinkedIn
                username and password stored in a .env file in
                the following format:
                    LINKEDIN_USER={yourvalidusername}
                    LINKEDIN_PASS={yourvalidpassword}
                Please make sure to remove the {} brackets when
                you add your username and password.

        Returns:
            None.
                However, your LinkedIn username and password
                stored in an .env file will be loaded as
                environment variables.
            """
        i = 1
        while i < 25:
            # Navigate to the bottom of the page to load more results
            if len(self.browser.find_elements(
                    By.CLASS_NAME, "global-footer-compact")) > 0:
                element = self.browser.find_element(
                    By.CLASS_NAME, "global-footer-compact")
            elif len(self.browser.find_elements(
                    By.CLASS_NAME, "jobs-search-two-pane__pagination")) > 0:
                element = self.browser.find_element(
                    By.CLASS_NAME, "jobs-search-two-pane__pagination")
            else:
                raise NoSuchElementException
            self.browser.execute_script(
                "arguments[0].scrollIntoView();", element)
            time.sleep(0.1)
            # Navigate through the loaded results in order to
            # load neighboring results (this function is best
            # understood by actually seeing it work on LinkedIn)
            job_lists = self.browser.find_element(
                By.CLASS_NAME, "jobs-search-results__list")
            jobs = job_lists.find_elements(
                By.CLASS_NAME, 'job-card-list__title')
            every_other_5_list = jobs[::i]
            for element in every_other_5_list:
                self.browser.execute_script(
                    "arguments[0].scrollIntoView();", element)
                time.sleep(0.3)
            i += 3

    def get_company_name(self, company_names):
        """
        Get the 25 company names listed on
        the LinkedIn jobs page.

        Args:
            company_names (list): a list of company names.

        Returns:
            company_names (list): a list of company names
            that has been appended with new company names.
        """
        # Save the <ul> HTML tag holding the job openings by
        # searching for its specific class name
        company_lists = self.browser.find_element(
            By.CLASS_NAME, "jobs-search-results__list")
        # Get an iterable list of all <li> tags holding
        # each individual job opening
        companies = company_lists.find_elements(
            By.CLASS_NAME, 'artdeco-entity-lockup__subtitle')
        # Iterate through each job opening
        for i in companies:
            # Append each company name to a list
            company_names.append(i.text)
        # Print results (LinkedIn may change its website
        # someday and that might break the script,
        # so you will want to print results to
        # verify everything is working properly)
        print("Company Names:")
        print(company_names, "\n")
        print("Length of list:", len(company_names))
        print()
        return company_names

    def get_job_titles(self, job_title):
        """
        Get the 25 job titles listed on
        the LinkedIn jobs page.

        Args:
            job_title (list): a list of job titles.

        Returns:
            job_title (list): a list of job titles
            that have been appended with new job titles.
        """
        # Save the <ul> HTML tag holding the job openings by
        # searching for its specific class name
        job_lists = self.browser.find_element(
            By.CLASS_NAME, "jobs-search-results__list")
        # Get an iterable list of all <li> tags holding
        # each individual job opening
        jobs = job_lists.find_elements(
            By.CLASS_NAME, 'job-card-list__title')
        # Iterate through each job opening
        for i in jobs:
            job_title.append(i.text)
        print("Job Titles:")
        print(job_title, "\n")
        print("Length of list:", len(job_title))
        print()
        return job_title

    def get_location(self, location):
        """
        Get the 25 job locations listed on
        the LinkedIn jobs page.

        Args:
            location (list): a list of locations.

        Returns:
            location (list): a list of locations
            that has been appended with new locations.
        """
        # Save the <ul> HTML tag holding the job openings by
        # searching for its specific class name
        location_lists = self.browser.find_element(
            By.CLASS_NAME, "jobs-search-results__list")
        # Get an iterable list of all <li> tags holding
        # each individual job opening
        each_item = location_lists.find_elements(
            By.CLASS_NAME, 'jobs-search-results__list-item')
        # Iterate through each job opening
        for number, item in enumerate(each_item):
            # For each job posting, grab the first element containing
            # the class name below, which will give us location
            if len(item.find_elements(
                    By.CLASS_NAME, 'job-card-container__metadata-wrapper'
                    )) > 0:
                i = item.find_element(
                    By.CLASS_NAME, 'job-card-container__metadata-wrapper')
                location.append(i.text)
            elif len(item.find_elements(
                    By.CLASS_NAME, 'job-card-container__metadata-item'
                    )) > 0:
                i = item.find_element(
                    By.CLASS_NAME, 'job-card-container__metadata-item')
                location.append(i.text)
            elif len(item.find_elements(
                    By.CLASS_NAME, 'artdeco-entity-lockup__caption'
                    )) > 0:
                i = item.find_element(
                    By.CLASS_NAME, 'artdeco-entity-lockup__caption')
                location.append(i.text)
            else:
                print(f"""Couldn't find location class name for
                        job number {number} on the page""")
        print("Location:")
        print(location, "\n")
        print("Length of list:", len(location))
        print()
        return location

    def get_descriptions(self, description):
        """
        Get the 25 job descriptions listed on
        the LinkedIn jobs page.

        Args:
            description (list): a list of job descriptions.

        Returns:
            description (list): a list of job descriptions
            that have been appended with new job descriptions.
        """
        # Save the <ul> HTML tag holding the job openings by
        # searching for its specific class name
        description_lists = self.browser.find_element(
            By.CLASS_NAME, "jobs-search-results__list")
        # Get an iterable list of all <li> tags holding
        # each individual job opening
        job_descriptions = description_lists.find_elements(
            By.CLASS_NAME, 'jobs-search-results__list-item')
        # Iterate through each job opening
        for i in job_descriptions:
            # Click on an individual job opening to
            # display its job description
            ac = ActionChains(self.browser)
            ac.move_to_element_with_offset(i, 2, 2).click().perform()
            time.sleep(0.2)
            # Scrape the job description
            element = self.browser.find_element(
                By.CLASS_NAME, 'jobs-description__content')
            # Append job description to list
            description.append(element.get_attribute("innerText"))
        print("Description list length:")
        print(len(description))
        print()
        return description

    def repeat_scrape_until_nth_page(self, position, n=5):
        """
        Scrape the first n pages of a position's job openings
        and return a list of a companies, job titles, locations,
        and job descriptions. We recommend setting the variable n
        to no more than 10 pages, as after the 5th page,
        duplicates become more present. For best results,
        leave n at 5.

        Args:
            position (str): a job title in HTML format.
                ex: "data%20scientist" (replace empty
                spaces with "%20")
            n (int): number of pages to scrape.

        Returns:
            scraped_list (list): a nested list of scraped data.
                ex: [company_names, job_title, location, description]
        """
        company_names = []
        job_title = []
        location = []
        description = []
        # Navigate to /jobs/ page
        self.browser.get(f"""https://www.linkedin.com/jobs/search/
            ?keywords={position}&location=united%20states""")
        # Loop through first n pages
        for i in range(1, n + 1):
            # Rest between page loads so the server
            # doesn't shut us out
            time.sleep(i)
            if i != 1:
                page = (i - 1) * 25
                self.browser.get(f"""https://www.linkedin.com/jobs/search/
                ?keywords={position}&location=united%20states&start={page}""")
            time.sleep(2)
            self.load_full_page()
            company_names = self.get_company_name(company_names)
            job_title = self.get_job_titles(job_title)
            location = self.get_location(location)
            description = self.get_descriptions(description)
        scraped_list = [company_names, job_title, location, description]
        return scraped_list

    def create_linkedin_dataframe(self):
        """
        Create a dataframe from the scraped text.

        Args:
            None.

        Returns:
            linkedin_jobs (DataFrame): a DataFrame containing
            the "company", "job_title", "location", and "description"
            for each job opening scraped for a given position
            and a given number of pages defined by the
            repeat_scrape_until_nth_page() method.
        """
        self.linkedin_jobs = pd.DataFrame(
            self.scraped_list, index=[
                "company", "job_title", "location", "description"
            ]).T
        return self.linkedin_jobs

    def print_unique_jobs(self):
        """
        Print the unique number of jobs scraped.

        Args:
            None.

        Returns:
            None.
        """
        for position in self.search_terms:
            print(f"Number of unique jobs found for {position}:",
                  self.linkedin_jobs['description'].nunique())

    def scrape_and_save_to_csv(self, n=5):
        """
        Loop through self.search_terms and scrape their
        job details. Then turn the scraped results into
        a dataframe, then save the dataframe to a csv.

        Args:
            n (int): number of pages to scrape.

        Returns:
            None.
        """
        for position in self.search_terms:
            self.scraped_list = self.repeat_scrape_until_nth_page(
                position, n)
            linkedin_jobs = self.create_linkedin_dataframe()
            saving_jobs = copy.deepcopy(linkedin_jobs)
            saving_jobs = saving_jobs.drop_duplicates(
                ['description']).reset_index(drop=True)
            saving_jobs = saving_jobs[
                saving_jobs['description'].notna()]
            position = position.replace("%20", "_")
            saving_jobs.to_csv(
                f"{self.curpath}/{self.folder_path}/{position}_jobs.csv",
                encoding='utf-8',
                index=False)
            print(f'Successfully saved {position} jobs!')

    def add_job_titles(self, job_list):
        """
        Add more job titles to search through.

        Args:
            job_list (str or list): A job title or list of
            job titles for the scraper to search through.
            Two examples below.
                ["web developer","backend engineer"]
                ["devops"]

        Returns:
            None.
        """
        if isinstance(job_list, list):
            for title in job_list:
                self.search_terms.append(parse.quote(title))
        elif isinstance(job_list, str):
            self.search_terms.append(parse.quote(job_list))
        else:
            print("No list or string was passed.")
        return f"Your search terms: {self.search_terms}"

    def redefine_job_titles(self, job_list):
        """
        This will wipe the old search term list
        and replace it with the list you provide.

        Args:
            job_list (str or list): A job title or list of
            job titles for the scraper to search through.
            Two examples below.
                ["web developer","backend engineer"]
                ["devops"]

        Returns:
            None.
        """
        if isinstance(job_list, list):
            self.search_terms = []
            for title in job_list:
                self.search_terms.append(parse.quote(title))
        elif isinstance(job_list, str):
            self.search_terms = parse.quote(job_list)
        else:
            print("No list or string was passed.")
        return f"Your search terms: {self.search_terms}"

    def remove_job_titles(self, job_list):
        """
        Remove job titles from the search list. This may
        produce an error if you provide a search term
        that does not already exist in the list.

        Args:
            job_list (str or list): A job title or list of
            job titles for the scraper to remove.
            Two examples below.
                ["web developer","backend engineer"]
                ["devops"]

        Returns:
            None.
        """
        if isinstance(job_list, list):
            for job in job_list:
                job_list.append(parse.quote(job))
            self.search_terms = [
                x for x in self.search_terms if x
                not in job_list
            ]
        elif isinstance(job_list, str):
            self.search_terms = [
                x for x in self.search_terms if
                x != job_list and x != parse.quote(job_list)
            ]
        else:
            print("No list or string was passed.")
        return f"Your search terms: {self.search_terms}"


if __name__ == '__main__':
    scraper = JobScraper()
    scraper.login_to_linkedin()
    scraper.scrape_and_save_to_csv(n=1)
    today = datetime.today().strftime('%Y-%m-%d')
    combine_individual_datasets(today)
