from api import HeadHunterAPI, SuperJobAPI
from vacancy import Vacancy
from JSONopener import JSONopener

# Функция для взаимодействия с пользователем
def user_interaction():
    # Собираем вводные данные для осуществления запроса

    choice = int(input('На каком сайте поищем? 1 - HeadHunter, 2 - SuperJob, 3 - оба'))

    if choice != 1 and choice != 2 and choice != 3:
        print("Неверный выбор")
        exit()
    keyword = input('По какому ключевому слову будем искать?')

    filter = input('А по какому слову будем их дополнительно фильтровать (оставить пустым, если не нужно фильтровать)?')

    n_max = int(input("Сколько (максимум) вакансий вывести: "))

    # В зависимости от выбора пользователя осуществляем запросы по API к площадкам вакансий
    if choice == 1:
        HeadHunterAPI().get_vacancies(keyword)
        merged_data = JSONopener('hh.json').open_json()
    elif choice == 2:
        SuperJobAPI().get_vacancies(keyword)
        merged_data = JSONopener('superjob.json').open_json()
    elif choice == 3:
        HeadHunterAPI().get_vacancies(keyword)
        SuperJobAPI().get_vacancies(keyword)
        merged_data = JSONopener('hh.json').open_json() + JSONopener('superjob.json').open_json()



    # Фильтруем список вакансий по дополнительному фильтру, указанному пользователю
    filtered_data = [x for x in merged_data if filter in x['title'] or filter in x['requirement']]
    # Создаем список из экземпляров класса Vacancy из отфильтрованного списка
    vacancies = [Vacancy(x['title'], x['url'], x['salary_from'], x['salary_to'], x['salary_currency'], x['requirement'])
                 for x in filtered_data]
    n = 1
    for vacancy in vacancies:
        print(f"{n}. {vacancy}")

        # Проверяем достигло ли число выведенных вакансий максимального (указанного пользователем)
        if n == n_max:
            break
        else:
            n += 1




    #Предлагаем провести сортировку по мин зарплате
    sort_choice = int(input('Хотите отсортировать вакансии по зарплате? Нажмите - 1'))
    if sort_choice == 1:

        sorted_vacancies = sorted(vacancies, reverse=True)
        n = 1
        for vacancy in sorted_vacancies:
            print(f"{n}. {vacancy}")
            if n == n_max:
                break
            else:
                n += 1
    else:
        print("Работа завершена")

if __name__ == "__main__":
    user_interaction()