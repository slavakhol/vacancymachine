from api import HeadHunterAPI, SuperJobAPI
import json


# Функция для взаимодействия с пользователем
def user_interaction():
    # Собираем вводные данные для осуществления запроса
    choice = int(input('На каком сайте поищем? 1 - HeadHunter, 2 - SuperJob, 3 - оба'))
    keyword = input('По какому ключевому слову будем искать?')
    filter = input('А по какому слову будем их дополнительно фильтровать (оставить пустым, если не нужно фильтровать)?')
    n_max = int(input("Сколько (максимум) вакансий вывести: "))

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
    with open('hh.json', 'r') as f:
        datahh = json.load(f)
    with open('superjob.json', 'r') as f2:
        datasj = json.load(f2)
    if choice == 1:
        merged_data = datahh
    elif choice == 2:
        merged_data = datasj
    elif choice == 3:
        merged_data = datahh + datasj

    # Фильруем список вакансий по дополнительному филтру, указанному пользователю
    filtered_data = [e for e in merged_data if filter in e['title'] or filter in e['requirement']]


    n=1
    for position in filtered_data:
            #Делаем дополнительные проверки на случай того, если работодатель не указал данные (или указал частично) о зарплате
            if position['salary_to'] == "0" and position['salary_from'] == "0":
                position['salary_currency'] = ""
            if position['salary_from'] == "0":
                salary_from = ""
            else:
                salary_from = "от " + str(position['salary_from'])
            if position['salary_to'] == "0":
                salary_to = ''
            else:
                salary_to = " до " + str(position['salary_to'])
            # Выводим результат на экран в виде списка
            print(f"{n}. {position['title']} ({position['url']}) {salary_from}{salary_to} {position['salary_currency']}")
            #Проверяем достигло ли число выведенных вакансий максимального (указанного пользователем)
            if n == n_max:
                break
            else:
                n += 1

if __name__ == "__main__":
    user_interaction()