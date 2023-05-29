class Vacancy():
    '''Класс создает экземпляр вакансий и определяет метод одображдения для print'''
    def __init__(self, title, url, salary_from, salary_to, salary_currency, requirement):
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.requirement = requirement

    #Методы сравнения
    def __lt__(self, other):
        return self.salary_from < other.salary_from
    def __gt__(self, other):
        return self.salary_from > other.salary_from

    # Метод для вывода экземляра класса на печать
    def __str__(self):
        # Делаем дополнительные проверки на случай того, если работодатель не указал данные (или указал частично) о зарплате
        if self.salary_to == 0 and self.salary_from == 0:
            salary_currency = "Зарплата не указана"
        else:
            salary_currency = self.salary_currency
        if self.salary_from == 0:
            salary_from = ""
        else:
            salary_from = "от " + str(self.salary_from)
        if self.salary_to == 0:
            salary_to = ""
        else:
            salary_to = " до " + str(self.salary_to)

        return f'{self.title} ({self.url}) {salary_from}{salary_to} {salary_currency}'