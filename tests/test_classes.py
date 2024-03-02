from src.classes import Headhunter, Vacancy, SaveInfoJson

vacancy = [{
    "name": "test_name",
    "area": {"name": "test_area"},
    "salary": {"from": 300000,
               "to": 1500000,
               "currency": "KZT"},
    "published_at": "2024-03-01T18:59:12+0300",
    "alternate_url": "https://hh.ru/vacancy/94123275",
    "employer": {"name": "test_name_employer"},
    "snippet": {
        "requirement": "hello"}},
    {"name": "test_name",
     "area": {"name": "test_area"},
     "salary": None,
     "published_at": "2024-03-01T18:59:12+0300",
     "alternate_url": "https://hh.ru/vacancy/94123275",
     "employer": {"name": "test_name_employer"},
     "snippet": {
         "requirement": "hello"}},
    {"name": "test_name",
     "area": {"name": "test_area"},
     "salary": {"from": None,
                "to": 1500000,
                "currency": "KZT"},
     "published_at": "2024-03-01T18:59:12+0300",
     "alternate_url": "https://hh.ru/vacancy/94123275",
     "employer": {"name": "test_name_employer"},
     "snippet": {
         "requirement": "hello"}},
    {"name": "test_name",
     "area": {"name": "test_area"},
     "salary": {"from": 2,
                "to": 1500000,
                "currency": "KZT"},
     "published_at": "2024-03-01T18:59:12+0300",
     "alternate_url": "https://hh.ru/vacancy/94123275",
     "employer": {"name": "test_name_employer"},
     "snippet": {
         "requirement": "hello"}}]


def test_headhunter_class():
    headhunter = Headhunter('python developer')


def test_saveinfojson():
    assert SaveInfoJson(vacancy).add_vacancies_to_file('test_json.json') is None
    assert SaveInfoJson(vacancy).data_from_file('test_json.json')[0]['salary']['to'] == 1500000


def test_vacancy_class():
    vac1 = Vacancy(vacancy[0])
    vac2 = Vacancy(vacancy[1])
    vac3 = Vacancy(vacancy[2])
    vac4 = Vacancy(vacancy[3])
    assert vac1.date == "2024-03-01T18:59:12+0300"
    assert vac1.salary == '300000 - 1500000 RUB'
    assert vac2.salary == 'Зарплата не указана'
    assert vac3.salary == 'Зарплата не указана'
    assert str(vac1) == ('\n'
                         'Название: test_name\n'
                         'Работадатель: test_name_employer\n'
                         'Зарплатная вилка: 300000 - 1500000 RUB\n'
                         'Требования: hello\n'
                         'Url вакансии: https://hh.ru/vacancy/94123275\n'
                         'Место работы: test_area\n'
                         'Дата и время публиикации: 2024-03-01 (18:59:12)\n')
    try:
        vac1 < vac4
    finally:
        pass
    try:
        vac4 < vac1
    finally:
        pass
    try:
        vac1 > vac4
    finally:
        pass
    try:
        vac4 > vac1
    finally:
        pass
