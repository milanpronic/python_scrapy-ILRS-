# Scrape a Website(ILRS)

## Project Details

I need you to scrape data from a website (as detailed in the attachment)
Then provide filtered output for each segment.

I can accept solutions in python, Jupiter notebook, excel or mobile apps.
Skills Required
PHP
Python
Web Scraping
Django
Software Architecture
-----------------
https://www.adamchoi.co.uk
    Both Teams To Score
        BTTS
    Total Match Goal
        Over 1.5 Match Goals
        Over 2.5 Match Goals
    Total Match Corners
        Over 9.5 Total Corners
        Over 10.5 Total Corners
    Total Cards
        Over 6.5 cards
https://www.adamchoi.co.uk/results/quick
    Playing today
    All matches
    Home Matches
    Away Matches
https://www.adamchoi.co.uk
    Popular
    Unbeated
    Corners
    example
------------------------
## Distribution
This site is established by iframe on Angular JS.
So Beautiful Soup don't work exactly and I used Selenium Python Framework.
Main file is 'main.py'
Selenium required package for this program
    webdriver  //  command line   "pip install webdriver-manage"
    csv        //  command line   "pip install csv"
    xlsxwriter //  command line   "pip install xlswriter"
After webdriver installed, you have to customize 5 line in main.py 
    driver = webdriver.Chrome(r"C:\Users\116\.wdm\drivers\chromedriver\win32\90.0.4430.24\chromedriver.exe") -> driver = webdriver.Chrome('the webdriver.exe file's location in your OS')

Run Command
    python main.py

`python ./main.py 20`
