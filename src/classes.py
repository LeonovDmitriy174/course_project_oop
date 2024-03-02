import requests
from datetime import date
from abc import ABC, abstractmethod

"""from src.util import get_currency_rate"""
import json


class AbstractClassAPI(ABC):

    def __init__(self, url, user_vacancies):
        response = requests.get(
            f'{url}?per_page=100&text={user_vacancies}&order_by=relevance&currency=RUR')
        self.vacancies = response.json()


class Headhunter(AbstractClassAPI, ABC):

    def __init__(self, user_vacancies, url='https://api.hh.ru/vacancies'):
        super().__init__(url, user_vacancies)


class Vacancy:
    name = None
    employer = None
    url = None
    __salary = True
    requirement = None
    area = None

    def __init__(self, vacancies):
        try:
            self.salary_to = vacancies['salary']['to']
            self.salary_from = vacancies['salary']['from']
        except TypeError:
            self.__salary = False
        else:
            if self.salary_to is None or self.salary_from is None:
                self.__salary = False
            else:
                self.salary_from = vacancies['salary']['from']
                self.salary_to = vacancies['salary']['to']
        finally:
            self.name = vacancies['name']
            self.employer = vacancies['employer']['name']
            self.url = vacancies['alternate_url']
            self.requirement = vacancies['snippet']['requirement']
            self.area = vacancies['area']['name']
            self.date = vacancies['published_at']

    @property
    def salary(self):
        if self.__salary:
            return f"{self.salary_from} - {self.salary_to} RUB"
        else:
            return 'Зарплата не указана'

    def __str__(self):
        return (f'\nНазвание: {self.name}\n'
                f'Работадатель: {self.employer}\n'
                f'Зарплатная вилка: {self.salary}\n'
                f'Требования: {self.requirement}\n'
                f'Url вакансии: {self.url}\n'
                f'Место работы: {self.area}\n'
                f'Дата и время публиикации: {self.date[:10]} ({self.date[11:19]})\n')

    def __lt__(self, other):
        if isinstance(other, Vacancy) and self.__salary and other.__salary:
            if self.salary_to + self.salary_from < other.salary_to + other.salary_from:
                return True
        return False

    def __gt__(self, other):
        if isinstance(other, Vacancy) and self.__salary and other.__salary:
            if self.salary_to + self.salary_from > other.salary_to + other.salary_from:
                return True
        return False


class AbstractClassFile(ABC):
    def __init__(self, vacancies):
        self.vacancies = vacancies

    @abstractmethod
    def add_vacancies_to_file(self):
        pass

    @abstractmethod
    def data_from_file(self):
        pass

    @abstractmethod
    def del_info_about_vacancies(self):
        pass


class SaveInfoJson(AbstractClassFile, ABC):
    def __init__(self, vacancies):
        super().__init__(vacancies)

    def add_vacancies_to_file(self):
        with open('vacancies.json', 'w') as json_file:
            json.dump(self.vacancies, json_file)

    def data_from_file(self):
        with open('vacancies.json', 'r') as json_file:
            file = json.load(json_file)
            return file

    def del_info_about_vacancies(self):
        with open('vacancies.json', 'w') as json_file:
            json.dump(None, json_file)