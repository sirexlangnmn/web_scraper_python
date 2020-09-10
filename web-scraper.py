# Import libraries
import requests
from bs4 import BeautifulSoup

import csv

# Create a file to write to, add headers row
f = csv.writer(open('indeed_job_list.csv', 'w'))
f.writerow(['Job Name', 'Job Preview Link', 'Company', 'Location', 'Salary', 'Easily Apply', 'Urgently Hiring', 'Responsive Employer', 'New', 'Job Description'])


# Collect first page of artists list
# iterating over the pages
pages = []
for i in range(1, 2):
    url = 'https://ph.indeed.com/jobs?q=IT&start=' + str(i)
    # https://ph.indeed.com/jobs?q=IT&start=2

    # url = 'https://www.jobstreet.com.ph/en/job-search/job-vacancy/' + str(i) + '/'
    # https://www.jobstreet.com.ph/en/job-search/job-vacancy/99/

    pages.append(url)

    if pages:
        # scraping data from each of those pages
        for item in pages:
            page = requests.get(item)
            # Create a BeautifulSoup object
            soup = BeautifulSoup(page.text, 'html.parser')


            # Pull all data from the table with class serpContainerMinHeight (Parent html tags)
            job_list = soup.find("table", attrs={"class": "serpContainerMinHeight"})

            # Pull data from all html tags inside of parent html tags
            jobs = job_list.find_all("div", attrs={"class": "jobsearch-SerpJobCard"})

            for job in jobs:
                # to get all job in the list
                job_name = job.find("a", attrs={"class": "jobtitle"}).text if job.find("a", attrs={"class": "jobtitle"}) else ""
                links = job.find("a", attrs={"class": "jobtitle"}).get('href') if job.find("a", attrs={"class": "jobtitle"}) else ""
                job_preview_link = 'https://ph.indeed.com' + links
                company = job.find('span', class_='company').text if job.find('span', class_='company') else ""
                location = job.find('span', class_='location').text if job.find('span', class_='location') else ""
                salary = job.find('div', class_='salarySnippet').text if job.find('div', class_='salarySnippet') else ""
                easily_apply = job.find('span', class_='iaLabel').text if job.find('span', class_='iaLabel') else ""
                urgently_hiring = job.find('span', class_='jobCardShelfIcon').text if job.find('span', class_='jobCardShelfIcon') else ""
                responsive_employer = job.find('span', class_='jobCardShelfIcon').text if job.find('span', class_='jobCardShelfIcon') else ""
                new = job.find('span', class_='new').text if job.find('span', class_='new') else ""

                # to get the other job details of specific job
                url2 = job_preview_link
                page2 = requests.get(url2)
                soup2 = BeautifulSoup(page2.text, 'html.parser')
                job_data = soup2.find("div", attrs={"class": "jobsearch-jobDescriptionText"})
                job_description = job_data.ul

                f.writerow([job_name, job_preview_link, company, location, salary, easily_apply, urgently_hiring, responsive_employer, new, job_description])
