"""Scrape LinkedIn's Job Postings"""

import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
import copy


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
        Load environment variables and default job title
        search terms.

        Args:
            None.

        Returns:
            None.

        If you want to add or delete job title search terms,
        consider building methods to ADD and DELETE
        search terms. Once those methods are built and
        functional, consider adjusting this docstring.
        """

        # Load LinkedIn username and password from .env file
        load_dotenv()

        # List the default "job search terms" in HTML format
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

    def login_to_linkedin(self):
        """
        Login to LinkedIn.com.

        Args:
            None.

        Returns:
            None.
        """

        # Save LinkedIn username and password to variables
        linkedin_user = os.environ['LINKEDIN_USER']
        linkedin_pass = os.environ['LINKEDIN_PASS']

        # Open browser to LinkedIn.com
        browser = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()))
        browser.get("https://www.linkedin.com")

        # Auto-input username and password on login page
        username = browser.find_element(By.ID, "session_key")
        username.send_keys(linkedin_user)
        password = browser.find_element(By.ID, "session_password")
        password.send_keys(linkedin_pass)

        # Click login button
        login_button = browser.find_element(By.CLASS_NAME,
                                            "sign-in-form__submit-button")
        login_button.click()

        # Save browser to class
        self.browser = browser

    def load_full_page(self):
        """
        We need to load all 25 jobs displayed on the jobs page
        in order to scrape their details. LinkedIn needs a user
        to scroll through the jobs page to load all 25 jobs.
        This function accomplishes the loading automatically.

        Args:
            None.
                However, you must have a valid LinkedIn
                username and password stored in a .env file in
                the follwoing format:
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

        # Recall the browser variable
        browser = self.browser

        # Set counter for our loop
        i = 1

        # Define loop
        while i < 25:
            # Navigate to the bottom of the page to load more results
            try:
                element = browser.find_element(
                    By.CLASS_NAME, "global-footer-compact")
            except NoSuchElementException:
                element = browser.find_element(
                    By.CLASS_NAME, "jobs-search-two-pane__pagination")
            browser.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(0.1)

            # Navigate through the loaded results in order to
            # load neighboring results (this function is best
            # understood by actually seeing it work on LinkedIn)
            job_lists = browser.find_element(
                By.CLASS_NAME, "jobs-search-results__list")
            jobs = job_lists.find_elements(
                By.CLASS_NAME, 'job-card-list__title')
            every_other_5_list = jobs[::i]
            for element in every_other_5_list:
                browser.execute_script(
                    "arguments[0].scrollIntoView();", element)
                time.sleep(0.3)

            # Add to the counter
            i += 3

        return

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
        # Recall the browser variable
        browser = self.browser

        # Save the <ul> HTML tag holding the job openings by
        # searching for its specific class name
        company_lists = browser.find_element(
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
        # so you will want to keep print results on to
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
            that has been appended with new job titles.
        """
        # Recall the browser variable
        browser = self.browser

        # Save the <ul> HTML tag holding the job openings by
        # searching for its specific class name
        job_lists = browser.find_element(
            By.CLASS_NAME, "jobs-search-results__list")

        # Get an iterable list of all <li> tags holding
        # each individual job opening
        jobs = job_lists.find_elements(
            By.CLASS_NAME, 'job-card-list__title')

        # Iterate through each job opening
        for i in jobs:
            # Append each job title to a list
            job_title.append(i.text)

        # Print results
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
        # Recall the browser variable
        browser = self.browser

        # Save the <ul> HTML tag holding the job openings by
        # searching for its specific class name
        location_lists = browser.find_element(
            By.CLASS_NAME, "jobs-search-results__list")

        # Get an iterable list of all <li> tags holding
        # each individual job opening
        each_item = location_lists.find_elements(
            By.CLASS_NAME, 'jobs-search-results__list-item')

        # Iterate through each job opening
        for number, item in enumerate(each_item):
            # For each job posting, grab the first element containing
            # the class name below, which will give us location
            try:
                i = item.find_element(
                    By.CLASS_NAME, 'job-card-container__metadata-wrapper')
            except NoSuchElementException:
                try:
                    i = item.find_element(
                        By.CLASS_NAME, 'job-card-container__metadata-item')
                except NoSuchElementException:
                    time.sleep(2)
            try:
                i = item.find_element(
                    By.CLASS_NAME, 'job-card-container__metadata-wrapper')
            except NoSuchElementException:
                try:
                    i = item.find_element(
                        By.CLASS_NAME, 'job-card-container__metadata-item')
                except NoSuchElementException:
                    print(f"""Couldn't find location class name for
                    job number {number} on the page""")
                    raise(NoSuchElementException)

            # Append each location to a list
            location.append(i.text)

        # Print results
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
            that has been appended with new job descriptions.
        """
        # Recall the browser variable
        browser = self.browser

        # Save the <ul> HTML tag holding the job openings by
        # searching for its specific class name
        description_lists = browser.find_element(
            By.CLASS_NAME, "jobs-search-results__list")

        # Get an iterable list of all <li> tags holding
        # each individual job opening
        job_descriptions = description_lists.find_elements(
            By.CLASS_NAME, 'jobs-search-results__list-item')

        # Iterate through each job opening
        for i in job_descriptions:
            # Click on an individual job opening to
            # display its job description
            ac = ActionChains(browser)
            ac.move_to_element_with_offset(i, 2, 2).click().perform()
            time.sleep(0.2)

            # Scrape the job description
            element = browser.find_element(
                By.CLASS_NAME, 'jobs-description__content')

            # Append job description to list
            description.append(element.get_attribute("innerText"))

        # Print results
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
        # Recall the browser variable
        browser = self.browser

        # Define our lists
        company_names = []
        job_title = []
        location = []
        description = []

        # Navigate to /jobs/ page
        browser.get(f"""https://www.linkedin.com/jobs/search/
            ?keywords={position}&location=united%20states""")

        page = 1

        # Loop through first n pages
        for i in range(1, n+1):

            # Rest between page loads so the server
            # doesn't shut us out
            time.sleep(i)
            if i != 1:
                page = (i-1)*25
                browser.get(f"""https://www.linkedin.com/jobs/search/
                ?keywords={position}&location=united%20states&start={page}""")

            # Give page 2 seconds to load
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
        linkedin_jobs = pd.DataFrame(
            self.scraped_list, index=[
                "company", "job_title", "location", "description"
                ]
            ).T

        return linkedin_jobs

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

        return

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
        # Create new folder with today's date so the data
        # stored is not overwritten the next time the
        # function runs.
        try:
            today = datetime.today().strftime('%Y-%m-%d')
            os.mkdir(f"data_generators/job_descriptions/scraped_{today}")
        except FileExistsError:
            print(f"""Folder data_generators/job_descriptions/scraped_{today}
            already exists!""")

        # Save the path to our folder
        self.folder_path = Path(
            f"data_generators/job_descriptions/scraped_{today}"
        )

        # Loop through all search terms
        for position in self.search_terms:

            # Find and scrape positions
            self.scraped_list = self.repeat_scrape_until_nth_page(
                position, n)

            # Save to dataframe
            linkedin_jobs = self.create_linkedin_dataframe()

            # Duplicate dataframe
            saving_jobs = copy.deepcopy(linkedin_jobs)

            # Drop duplicate job openings on new dataframe
            saving_jobs = saving_jobs.drop_duplicates(
                ['description']).reset_index(drop=True)

            # Remove jobs scraped without descriptions
            saving_jobs = saving_jobs[
                saving_jobs['description'].notna()
                ]

            # Rename position variable
            position = position.replace("%20", "_")

            # Get current working directory
            self.curpath = os.getcwd()

            # Save unique jobs
            saving_jobs.to_csv(
                f"{self.curpath}/{self.folder_path}/{position}_jobs.csv",
                encoding='utf-8',
                index=False
                )

            print(f'Successfully saved {position} jobs!')

        return

    def combine_individual_datasets(self, folder_date):
        """
        Loop through a specific folder in the "job-descriptions"
        folder and combine all csvs into one big csv containing
        all job details from each individual csv.

        Args:
            folder_date (str): the date of a previous scrape
            performed, in this format: "%Y-%m-%d".
                ex: "2022-03-19"
            You can find the dates of all previous scrapes
            by looking in the folder "job_descriptions".
            In that folder, you will find sub-folders titled
            like "scraped_2022-03-19".

        Returns:
            None.
        """
        # Get filepath and encode job_descriptions/scraped_{folder_date}/
        jobs_path = f'data_generators/job_descriptions/scraped_{folder_date}/'
        encoded_filepath = os.fsencode(jobs_path)

        # Create empty list to add dataframes to
        dataframe_list = []

        # Iterate through folder
        for file in os.listdir(encoded_filepath):

            # Get actual filename of csv
            filename = os.fsdecode(file)

            # Do not include combined csv if it already exists
            if filename != f'all_scraped_jobs_{folder_date}.csv':

                # Get actual path of csv
                dataset_path = os.path.join(jobs_path, filename)

                # Read csv into a dataframe
                data_df = pd.read_csv(dataset_path, encoding='utf-8')

                # Append dataframe to a list to be concatenated
                dataframe_list.append(data_df)

        # Concat all dataframes into one big dataframe
        # with all job titles
        all_jobs_df = pd.concat(dataframe_list).reset_index(drop=True)

        # Save our dataset
        all_jobs_df.to_csv(
            f"{jobs_path}/all_scraped_jobs_{folder_date}.csv",
            encoding='utf-8',
            index=False
            )

        print('Successfully saved combined dataset!')


if __name__ == '__main__':
    # Instantiate object
    scraper = JobScraper()

    # Log into LinkedIn
    scraper.login_to_linkedin()

    # Scrape the first n pages of job openings
    scraper.scrape_and_save_to_csv(n=1)

    # Combine all datasets scraped today
    today = datetime.today().strftime('%Y-%m-%d')
    scraper.combine_individual_datasets(today)
