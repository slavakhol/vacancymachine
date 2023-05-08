import os
import requests
from abc import ABC, abstractmethod
import json
class API(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass

class HeadHunterAPI(API):
    def get_vacancies(self, keyword):
        response = requests.get(
        "https://api.hh.ru/vacancies?",
        headers={"HH-User-Agent": 'VacancyMachine/1.0 (slava.kholopov@gmail.com)'},
        params={"text": keyword}
        )
        my_list = []

        for item in response.json()['items']:
            #Приводим формат выдачи по  API от HH к единому(за основу взят SuperJob)
            if item['salary'] is None:
                salary_from = '0'
                salary_to = '0'
                salary_currency = ""
            else:
                salary_from = item['salary']['from']
                salary_to = item['salary']['to']
                salary_currency = item['salary']['currency']
            if salary_from == None:
                salary_from = "0"
            if salary_to == None:
                salary_to = "0"
            #Формируем данные списка для сохранения в локальный файл
            data = {
                "title": item['name'],
                "url": "https://hh.ru/vacancy/" + item['id'],
                "salary_from":  salary_from,
                "salary_to": salary_to,
                "salary_currency": salary_currency,
                "requirement": item['snippet']['requirement']
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
        for object in response.json()['objects']:

            data = {
                "title": object['profession'],
                "url": object['link'],
                "salary_from":  str(object['payment_from']),
                "salary_to": str(object['payment_to']),
                "salary_currency":  "RUB",
                "requirement": object['candidat']
            }
            my_list.append(data)
        with open("superjob.json", "w", encoding="utf-8") as f:
            json.dump(my_list, f, ensure_ascii=False)

class Vacancy():
    def __init__(self, title, url, salary_from, salary_to, salary_currency, requirement):
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.requirement = requirement

    # Метод для вывода экземляра класса на печать
    def __str__(self):
        # Делаем дополнительные проверки на случай того, если работодатель не указал данные (или указал частично) о зарплате
        if self.salary_to == "0" and self.salary_from == "0":
            salary_currency = "Зарплата не указана"
        else:
            salary_currency = self.salary_currency
        if self.salary_from == "0":
            salary_from = ""
        else:
            salary_from = "от " + str(self.salary_from)
        if self.salary_to == "0":
            salary_to = ""
        else:
            salary_to = " до " + str(self.salary_to)

        return f'{self.title} ({self.url}) {salary_from}{salary_to} {salary_currency}'