import csv
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()

url = 'https://www.amazon.ca/'
driver.get(url)


def get_url(search_term):
    template = 'https://www.amazon.ca/s?k={}&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')
    return template.format(search_term)


url = get_url('phone')
print(url)
