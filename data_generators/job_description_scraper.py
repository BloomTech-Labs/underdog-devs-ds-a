"""Scrape LinkedIn's Job Postings"""

import os
from dotenv import load_dotenv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import copy


class JobScraper:
    """
    This class opens Google Chrome and logs into the user's
    LinkedIn account.

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

    # Load LinkedIn username and password from .env file
    load_dotenv()

    def __init__(self):
        """Login to LinkedIn.com"""

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
        """
        # Recall the browser variable
        browser = self.browser

        # Save the <ul> HTML tag holding the job openings by
        # searching for its specific class name
        location_lists = browser.find_element(By.CLASS_NAME, "jobs-search-results__list")

        # Get an iterable list of all <li> tags holding
        # each individual job opening
        each_item = location_lists.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')
        
        # Iterate through each job opening
        for item in each_item:
            # For each job posting, grab the first element containing
            # the class name below, which will give us location
            i = item.find_element(By.CLASS_NAME, 'job-card-container__metadata-wrapper')
            
            # Append each location to a list
            location.append(i.text)
        
        # Print results
        print("Location:")
        print(location, "\n")
        print("Length of list:", len(location))
        print()
        
        return location



# # Get job descriptions
# def get_descriptions(browser, description):
#     """
#     Get the 25 job descriptions listed on 
#     the LinkedIn jobs page.
#     """
#     # Save the <ul> HTML tag holding the job openings by
#     # searching for its specific class name
#     description_lists = browser.find_element(By.CLASS_NAME, "jobs-search-results__list")
    
#     # Get an iterable list of all <li> tags holding
#     # each individual job opening
#     job_descriptions = description_lists.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')
    
#     # Iterate through each job opening
#     for i in job_descriptions:
#         # Click on an individual job opening to 
#         # display its job description
#         ac = ActionChains(browser)
#         ac.move_to_element_with_offset(i, 2, 2).click().perform()
#         time.sleep(0.2)
        
#         # Scrape the job description
#         element = browser.find_element(By.CLASS_NAME, 'jobs-description__content')
        
#         # Append job description to list
#         description.append(element.get_attribute("innerText"))
        
#     # Print results
#     print("Description list length:")
#     print(len(description))
#     print()
    
#     return description


# # ### Now define our looping scraper function to scrape the first 10 pages of a position

# # Scrape first 10 pages
# def repeat_scrape_until_10th_page(browser, position):
#     """
#     Scrape first 10 pages of a position's job openings.
#     """
#     # Define our lists
#     company_names=[]
#     job_title=[]
#     location=[]
#     description=[]
    
#     # Navigate to /jobs/ page
#     browser.get(f"https://www.linkedin.com/jobs/search/?keywords={position}&location=united%20states")
    
#     page = 1
    
#     # Loop through first 10 pages
#     for i in range(1, 11):
        
#         # Rest between page loads so the server 
#         # doesn't shut us out
#         time.sleep(i)
#         if i != 1:
#             page = (i-1)*25
#             browser.get(f'https://www.linkedin.com/jobs/search/?keywords={position}&location=united%20states&start={page}')
        
#         # Give page 2 seconds to load
#         time.sleep(2)
#         load_full_page()
#         company_names = get_company_name(browser, company_names)
#         job_title = get_job_titles(browser, job_title)
#         location = get_location(browser, location)
#         description = get_descriptions(browser, description)
        
#     scraped_list = [company_names, job_title, location, description]
    
#     return scraped_list




# # ### Begin looking for jobs

# # List the "job search terms" in HTML format 
# # to iterate through
# search_terms = [
#     "data%20scientist",
#     "machine%20learning%20engineer",
#     "data%20engineer",
#     "web%20developer",
#     "frontend%20developer",
#     "backend%20developer", 
#     "devops",
#     "software%20engineer"
# ]

# # ### Collect jobs and store in dataframes

# # Loop through all search terms
# for position in search_terms:
    
#     # Find and scrape positions
#     scraped_list = repeat_scrape_until_10th_page(browser, position)

#     # Define dataframe-creating function
#     def create_linkedin_dataframe(scraped_list):
#         """
#         Create a dataframe from the scraped text.
#         """
#         linkedin_jobs = pd.DataFrame(scraped_list, 
#             index=["company","job_title","location","description"]).T
        
#         return linkedin_jobs

#     # Create dataframe from results
#     linkedin_jobs = create_linkedin_dataframe(scraped_list)

#     # Look at number of unique jobs to account for duplicate postings
#     print(f"Number of unique jobs found for {position}:", 
#           linkedin_jobs['description'].nunique())

#     # Begin filtering and saving work
#     saving_jobs = copy.deepcopy(linkedin_jobs)
    
#     # Drop duplicates
#     saving_jobs = saving_jobs.drop_duplicates(['description']).reset_index(drop=True)
    
#     # Remove jobs scraped without descriptions
#     saving_jobs = saving_jobs[saving_jobs['description'].notna()]
#     display(saving_jobs)

#     # Rename position variable
#     position = position.replace("%20","_")

#     # Save unique jobs
#     saving_jobs.to_csv(f'individual_jobs/{position}_jobs.csv', encoding='utf-8', index=False)
#     print(f'Successfully saved {position} jobs!')

# # ### Merge our saved datasets into one super dataset with all job titles

# # +
# # Get filepath and encode individual_jobs/ folder
# individual_jobs_filepath = os.fsencode('individual_jobs/')

# # Create empty list to add dataframes to
# dataframe_list = []

# # Iterate through folder
# for file in os.listdir(individual_jobs_filepath):
    
#     # Get actual filename of csv
#     filename = os.fsdecode(file)
    
#     # Get actual path of csv
#     dataset_path = os.path.join('individual_jobs/', filename)
    
#     # Read csv into a dataframe
#     data_df = pd.read_csv(dataset_path, encoding='utf-8')
    
#     # Append dataframe to a list to be concatenated
#     dataframe_list.append(data_df)

# # Concat all dataframes into one big dataframe
# # with all job titles
# all_jobs_df = pd.concat(dataframe_list).reset_index(drop=True)

# # Display new dataframe
# all_jobs_df
# # -

# # Save our dataset
# all_jobs_df.to_csv(f'scraped_linkedin_jobs.csv', encoding='utf-8', index=False)
# print(f'Successfully saved jobs!')

if __name__ == '__main__':
    scraper = JobScraper()
    scraper.load_full_page()
