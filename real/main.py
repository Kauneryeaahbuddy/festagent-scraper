from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import time
from openpyxl import load_workbook

ua = UserAgent

def get_festival():

    wb = load_workbook("table.xlsx")
    ws = wb["data"]

    response = requests.get(
        url=f'https://festagent.com/ru/festivals?',
        headers={'user-agent': f'{ua.random}'}
    )


    soup = BeautifulSoup(response.text, 'lxml')

    pagination = soup.find('div', class_='pagination')
    last_page = pagination.find('a', class_='last_page').get('href').split('page=')
    last_page = int(last_page[-1])


    for page in range(1, last_page + 1):
        response = requests.get(
            url=f'https://festagent.com/ru/festivals?page-{page}',
            headers={'user-agent': f'{ua.random}'}
        )

        soup = BeautifulSoup(response.text, 'lxml')

        all_festivals_list = soup.find_all('div', class_='title-link')
        festival_links = []

        for festival in all_festivals_list:
            link_festival = 'https://festagent.com/' + festival.find('a').get('href')
            festival_links.append(link_festival)

        count = 0

        for link in festival_links:
            response = requests.get(
                url=f'{link}',
                headers={'user-agent': f'{ua.random}'}
            )

            soup = BeautifulSoup(response.text, 'lxml')

            title_of_festival = soup.find('h1', class_='festival-name').text.strip()
            venue = soup.find('span', class_='country-icon').next_element.text.strip() + ': ' + soup.find('span', class_='festival-city').text.strip()
            site_of_festival = soup.find('a', class_='website').get('href')
            contacts = soup.find('div', class_='contacts').find_all('p')
            
            if contacts[-1]:
                if contacts[-1].find('a'):
                    email = contacts[-1].find('a').string

            ws.append([title_of_festival, venue, site_of_festival, email, link])

            count+=1
            print(f'link #{count} done')

            time.sleep(1)

        print(f'page #{page} done')
        time.sleep(5)

    wb.save('table.xlsx')
    wb.close()



def main():
    get_festival()

if __name__ == '__main__':
    main()