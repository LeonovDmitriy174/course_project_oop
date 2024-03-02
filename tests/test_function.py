from src.function import user_interaction, currency_rate

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
     "salary": {"from": 300000,
                "to": 1500000,
                "currency": "BYR"},
     "published_at": "2024-03-01T18:59:12+0300",
     "alternate_url": "https://hh.ru/vacancy/94123275",
     "employer": {"name": "test_name_employer"},
     "snippet": {
         "requirement": "hello"}},
    {"name": "test_name",
     "area": {"name": "test_area"},
     "salary": {"from": 300000,
                "to": None,
                "currency": "BYR"},
     "published_at": "2024-03-01T18:59:12+0300",
     "alternate_url": "https://hh.ru/vacancy/94123275",
     "employer": {"name": "test_name_employer"},
     "snippet": {
         "requirement": "hello"}}]


def test_currency_rate():
    assert currency_rate(vacancy)[0]['name'] == 'test_name'
