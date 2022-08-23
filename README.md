## Web Scraper for Reddit
A Reddit data collection project.
I have designed this project to obtain mostly unstructured and some structured data from Reddit, an interesting American social news/ content rating platform that is an incredible source of information on countless fields of human knowledge and a website where it is possible to contribute to any discussion one can think of. The aim of this scraper is to analyse the data from some of the hottest topics in the world and find out the current most popular words in each different topic. This could be useful to make predictions about cryptocurrency and stock markets for investors. 
I used Selenium technology to scrape the desired data.

# Summary of the project structure.
Using object oriented programming approach, the scraper contains one module with a class that holds most of the code: class Scraper().
Scraper class allows for navigating, installing and scalably storing the scraped data. The class includes methods to:
- Slowly scroll down the page to enable navigating (__scroll_down_page)
- Click the ‘new’ button of each community to scrape the latest posts and not the most popular
- Determine the advertisements to avoid scraping promoted posts
- Scrape the texts of titles, number of comments, number of votes and image sources and print them out in text
- Store the data of each community in separate JSON files and upload these raw data files in AWS S3 bucket
- Convert the raw data to tabular and upload the tables to AWS RDS through sqlalchemy and psycop2

# Testing
Some of the methods were tested using the unittest module of Python, it is possible to test the methods through the file ‘testscraper.py’. 
- Testing directory has two modules: [testing.py](http://testing.py) and [testscraper.py](http://testscraper.py) (contains TestScraper() and TestIntegrationScraper() which are TestCase classes)
- The test will check that each data entry has only one string data
- It will check that the data has been placed in the JSON file

# Cloud Storage 
I used Amazon Web Services (AWS) software tools to store my objects in an S3 bucket through a web service interface and RDS (Relational Database Service) to set up, operate and scalably store my tabular data in the cloud. 
