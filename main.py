#!/usr/bin/env python3
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_url(search_term):
    template = 'https://www.amazon.ca/s?k={}&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')
    # add term query to url
    u = template.format(search_term)
    u += '&page={}'
    return u


def extract_record(item):
    """ extract and return  data from a single record"""
    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    urls = 'https://www.amazon.ca/' + atag.get('href')

    # price
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return
    # rank and rating
    try:
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''
    result = (description, price, rating, review_count, urls)
    return result


if __name__ == '__main__':
    print('add an Article to search:\n')
    search = input()
    driver = webdriver.Chrome(ChromeDriverManager().install())
    records = []
    url = get_url(search)
    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'dat-component-type': 's-search-result'})
        for i in results:
            record = extract_record(i)
            if record:
                records.append(record)
    driver.close()
    # save data to csv file
    with open('data.csv', 'w+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
        writer.writerows(records)
