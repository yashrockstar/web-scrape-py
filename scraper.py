import requests
from bs4 import BeautifulSoup
import csv


def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/107.0.0.0'
                      'Safari/537.36'
    }

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def scrapeData(quotes, base_url):
    print(f'{base_url}')
    soup = scrape_page(base_url)
    quote_elements = soup.find_all('div', class_='quote')

    for quote_element in quote_elements:
        text = quote_element.find('span', class_='text').text
        author = quote_element.find('small', class_='author').text
        tag_elements = quote_element.find('div', class_='tags').find_all('a', class_='tag')
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ', '.join(tags)
            }
        )

    nextPage = soup.find('li', class_='next')
    if nextPage is not None:
        next_page_relative_url = nextPage.find('a', href=True)['href']
        base_url = 'https://quotes.toscrape.com'
        scrapeData(quotes, base_url + next_page_relative_url)


def createCSV(quotes):
    csv_file = open('quotes.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(['Text', 'Author', 'Tags'])

    for quote in quotes:
        writer.writerow(quote.values())

    print(f'{csv_file}')
    csv_file.close()


quoteList = []
baseUrl = 'https://quotes.toscrape.com'

soupData = scrape_page(baseUrl)
scrapeData(quoteList, baseUrl)
createCSV(quoteList)
print(f'{quoteList}')
