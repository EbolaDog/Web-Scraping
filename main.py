import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re
import json


HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers = Headers(browser='chrome', os='win').generate()
vacancy_list = []


def true_info(text):
    pattern = r"(.*django.*flask.*)|(.*flask.*django.*)"
    result = re.findall(pattern, text, flags=re.I)
    return result


vacancy = requests.get(HOST, headers=headers).text
soup = BeautifulSoup(vacancy, features='lxml')
vacancy_tag = soup.find(id='a11y-main-content')
vacancy_tags = vacancy_tag.find_all(class_='serp-item')

for vacancy in vacancy_tags:
    vacancy_href = vacancy.find('a', class_='serp-item__title')['href']
    vacancy_html = requests.get(vacancy_href, headers=headers).text
    soup = BeautifulSoup(vacancy_html, features="lxml")
    vacancy_body = soup.find('div', class_="vacancy-section").text
    if len(true_info(vacancy_body)) > 0:
        name_company = vacancy.find('a', class_='bloko-link').text
        city = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
        salary = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
        if salary:
            vacancy_salary = salary.text
        else:
            vacancy_salary = '-'
        vacancy_list.append({
            'link': vacancy_href,
            'salary': vacancy_salary,
            'name_company': name_company,
            'city': city
        })
        
with open(r"Vacancy.json", 'w', encoding='utf-8') as f:
       json.dump(vacancy_list, f, ensure_ascii=False,  indent=2)