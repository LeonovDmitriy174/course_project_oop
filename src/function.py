import requests
from src.classes import Vacancy, Headhunter, SaveInfoJson


def user_interaction():
    print('Приветствую!\n'
          'Я помогу подобрать самые интересные предложения на HeadHunter по вашему запросу\n')
    user_vacancies = input('Введите описание, интересующей вас вакансии: ').strip()

    vacancies = Headhunter(user_vacancies).vacancies['items']
    save_vac = SaveInfoJson(vacancies)
    save_vac.add_vacancies_to_file()

    continue_user = input('\nХотите ли вы отфильтровать получаемые вакансии?[yes]: ').strip().lower()
    if continue_user not in ['y', 'ye', 'yes', 'yeah', 'д', 'да', '', ' ']:
        for i in save_vac.data_from_file()[:5]:
            print(Vacancy(i))
        exit()

    try:
        user_salary = int(input('Введите числом минимальный размер зарплаты[50000]: '))
    except ValueError:
        user_salary = 50000

    try:
        user_quantity = int(input('Какое количество вакансий вы бы хотели рассмотреть?[5]: '))
    except ValueError:
        user_quantity = 5

    more_salary = []
    for i in save_vac.data_from_file():
        if i['salary'] is None:
            continue
        elif i['salary']['from'] is None:
            continue
        else:
            more_salary.append(i)

    order_by = input(
        'Введите ключевое слово для фильтрации вакансий (по дате публикации; по зарплате)[по дате]: ').strip().lower()

    while True:
        if order_by in ['дата', 'дате', 'по дате', '', ' ']:
            currency_rate_list = currency_rate(more_salary)
            sorted_vacancies = sorted(currency_rate_list, key=lambda x: (x['published_at']), reverse=True)
            break
        elif order_by in ['зарплата', 'зарплате', 'по зарплате']:
            currency_rate_list = currency_rate(more_salary)
            sorted_vacancies = sorted(currency_rate_list, key=lambda x: (x['salary']['from']), reverse=True)
            break
        else:
            order_by = input(
                '\nПожалуйста выберите из предложенного (по дате; по зарплате)[по зарплате]: ').strip().lower()

    finally_list_vacancies = []
    for i in sorted_vacancies:
        if i['salary']['from'] >= user_salary:
            finally_list_vacancies.append(i)

    if len(finally_list_vacancies) < user_quantity:
        print(
            f'\nПредупреждаю!\n'
            f'Количество вакансий по заданным параметрам меньше ожидаемого - {len(finally_list_vacancies)}')

    for i in finally_list_vacancies[:user_quantity]:
        print(Vacancy(i))


def currency_rate(more_salary):
    response_rate = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    currency_rate_list = []
    for i in more_salary:
        if i['salary']['currency'] == 'BYR':
            i['salary']['currency'] = 'BYN'
        try:
            i['salary']['to'] *= 5
        except TypeError:
            pass
        else:
            if i['salary']['currency'] != 'RUR':
                i['salary']['to'] *= (response_rate['Valute'][i['salary']['currency']]['Value']
                                      / response_rate['Valute'][i['salary']['currency']]['Nominal'])
                i['salary']['to'] = round(i['salary']['to'], 1)
        finally:
            if i['salary']['currency'] != 'RUR':
                i['salary']['from'] *= (response_rate['Valute'][i['salary']['currency']]['Value']
                                        / response_rate['Valute'][i['salary']['currency']]['Nominal'])
                i['salary']['from'] = round(i['salary']['from'], 1)
                currency_rate_list.append(i)
    return currency_rate_list
