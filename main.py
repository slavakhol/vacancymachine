from classes import HeadHunterAPI, SuperJobAPI, Vacancy
import json

# Функция для взаимодействия с пользователем
def user_interaction():
    # Собираем вводные данные для осуществления запроса
    # choice = int(input('На каком сайте поищем? 1 - HeadHunter, 2 - SuperJob, 3 - оба'))
    choice = 3
    # keyword = input('По какому ключевому слову будем искать?')
    keyword = "Python"
    # filter = input('А по какому слову будем их дополнительно фильтровать (оставить пустым, если не нужно фильтровать)?')
    filter = "офис"
    # n_max = int(input("Сколько (максимум) вакансий вывести: "))
    n_max = 10
    # В зависимости от выбора пользователя осуществляем запросы по API к площадкам вакансий
    if choice == 1:
        HeadHunterAPI().get_vacancies(keyword)
    elif choice == 2:
        SuperJobAPI().get_vacancies(keyword)
    elif choice == 3:
        HeadHunterAPI().get_vacancies(keyword)
        SuperJobAPI().get_vacancies(keyword)
    else:
        print("Некорректный ввод")
    #Объединяем полученные ответы от системы в единый список
    with open('hh.json', 'r', encoding="utf-8") as f:
        datahh = json.load(f)
    with open('superjob.json', 'r', encoding="utf-8") as f2:
        datasj = json.load(f2)
    if choice == 1:
        merged_data = datahh
    elif choice == 2:
        merged_data = datasj
    elif choice == 3:
        merged_data = datahh + datasj

    # Фильруем список вакансий по дополнительному фильтру, указанному пользователю
    filtered_data = [x for x in merged_data if filter in x['title'] or filter in x['requirement']]

    # Создаем список из экземпляров класса Vacancy из отфильтрованного списка
    vacancies = [Vacancy(x['title'], x['url'], x['salary_from'], x['salary_to'], x['salary_currency'], x['requirement']) for x in filtered_data]

    n = 1
    for vacancy in vacancies:
        print(f"{n}. {vacancy}")

        # Проверяем достигло ли число выведенных вакансий максимального (указанного пользователем)
        if n ==n_max:
            break
        else:
            n+=1

if __name__ == "__main__":
    user_interaction()