from bs4 import BeautifulSoup
import requests
import re
import csv

HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}  # pretending to be user and not a webscraper

try:
    source = requests.get('https://www.imdb.com/chart/top/', headers=HEADERS)
    source.raise_for_status()  # to throw an error in case of faulty URL
    soup = BeautifulSoup(source.text, 'lxml')

    movies = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-9d2f6de0-0 iMNUXk compact-list-view ipc-metadata-list--base").find_all('li')

    with open('movie_list.csv', 'w', newline='', encoding='utf-8') as csvfile:  # Output will be written to csv
        writerObj = csv.writer(csvfile)
        writerObj.writerow(['rank', 'name', 'year', 'duration', 'classification', 'rating'])

        for movie in movies:  # loop to iterate through each tag/s associated with each movie in the list
            rank = movie.find('div', class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-479faa3c-9 dkLVoC cli-title").h3.text.split('.')[0]
            name = movie.find('div', class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-479faa3c-9 dkLVoC cli-title").h3.text.split('.')[1]
            metadata = movie.find('div', class_="sc-479faa3c-7 jXgjdT cli-title-metadata").text
            year = metadata[:4]
            duration = re.split('m|,|M,|R', metadata[4:])[0]
            classification = (re.split('m|, |h', metadata[4:]))[-1]
            rating = movie.find('div', class_="sc-e3e7b191-0 jlKVfJ sc-479faa3c-2 eUIqbq cli-ratings-container").span.text[:3]
            # print(rank, name, year, duration, classification, rating, '\n')
            data = [rank, name, year, duration, classification, rating]
            writerObj.writerow(data)

except Exception as e:
    print(e)
