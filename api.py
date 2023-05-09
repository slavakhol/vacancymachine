import os
import requests
from abc import ABC, abstractmethod
import json
class API(ABC):
    '''Создаем абстрактный класс и метод для определения шаблона дочерних классов'''
    @abstractmethod
    def get_vacancies(self):
        pass

class HeadHunterAPI(API):
    '''Определяем метод класс для обращению к серверу площадки по API'''
    def get_vacancies(self, keyword):
        response = requests.get(
        "https://api.hh.ru/vacancies?",
        headers={"HH-User-Agent": 'VacancyMachine/1.0 (slava.kholopov@gmail.com)'},
        params={"text": keyword}
        )
        my_list = []
        # Приводим формат выдачи по  API от HH к единому (за основу взят SuperJob), осуществляется проверка отсутствия необязательных полей
        for item in response.json()['items']:
            if item['snippet']['requirement'] is None:
                item['snippet']['requirement'] = ""

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
    '''Определяем метод класс для обращению к серверу площадки по API'''
    def get_vacancies(self, keyword):
        response = requests.get(
        "https://api.superjob.ru/2.0/vacancies/",
        headers={"X-Api-App-Id": os.getenv('SUPERJOB_SECRET')},
        params={"keyword": keyword}
    )
        my_list = []
        # Приводим формат выдачи по  API к единому, осуществляется проверка отсутствия необязательных полей
        for object in response.json()['objects']:
            if object['candidat'] is None:
                object['candidat'] = ""
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

