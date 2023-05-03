import os
import requests
from abc import ABC
import json
class API(ABC):
    pass

class HeadHunterAPI(API):
    def get_vacancies(self, keyword):
        response = requests.get(
        "https://api.hh.ru/vacancies?",
        headers={"HH-User-Agent": 'VacancyMachine/1.0 (slava.kholopov@gmail.com)'},
        params={"text": keyword}
        )
        my_list = []

        for jp in response.json()['items']:
            #Приводим формат выдачи по  API от HH к единому(за основу взят SuperJob)
            if jp['salary'] is None:
                salary_from = '0'
                salary_to = '0'
                salary_currency = ""
            else:
                salary_from = jp['salary']['from']
                salary_to = jp['salary']['to']
                salary_currency = jp['salary']['currency']
            if salary_from == None:
                salary_from = "0"
            if salary_to == None:
                salary_to = "0"
            #Формируем данные списка для сохранения в локальный файл
            data = {
                "title": jp['name'],
                "url": "https://hh.ru/vacancy/" + jp['id'],
                "salary_from":  salary_from,
                "salary_to": salary_to,
                "salary_currency": salary_currency,
                "requirement": jp['snippet']['requirement']
            }
            my_list.append(data)
        #Сохраняем локальный файл
        with open("hh.json", "w", encoding="utf-8") as f:
            json.dump(my_list, f, ensure_ascii=False)



class SuperJobAPI(API):
    def get_vacancies(self, keyword):
        response = requests.get(
        "https://api.superjob.ru/2.0/vacancies/",
        headers={"X-Api-App-Id": os.getenv('SUPERJOB_SECRET')},
        params={"keyword": keyword}
    )
        my_list = []
        for jp in response.json()['objects']:

            data = {
                "title": jp['profession'],
                "url": jp['link'],
                "salary_from":  str(jp['payment_from']),
                "salary_to": str(jp['payment_to']),
                "salary_currency":  "RUB",
                "requirement": jp['candidat']
            }
            my_list.append(data)
        with open("superjob.json", "w", encoding="utf-8") as f:
            json.dump(my_list, f, ensure_ascii=False)

