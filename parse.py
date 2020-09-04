# импорт библиотек
from selenium import webdriver
import csv
from bs4 import BeautifulSoup as bs
from datetime import date, datetime

# путь к драйверу chrome
chromedriver = '/home/dony/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
options.add_argument('--no-sandbox')  # 
browser = webdriver.Chrome(executable_path=chromedriver, options=options)
url = 'https://kbp.aero/ru'


# Запускаем хром для получения данных
browser.get(url)
# Получение HTML-содержимого
requiredHtml = browser.page_source
browser.quit()

# Метод для парсинга
def parse(url):
    soup = bs(requiredHtml, 'html5lib')
    headers = []
    data = []
    
    # ищем таблицы на сегодня(прилет, вылет)
    arrival = soup.find('div', class_='table_wrp in today')
    departure = soup.find('div', class_='table_wrp out today')
    arrival_table = arrival.find('table', attrs={"class":"tbody"})
    departure_table = departure.find('table', attrs={"class":"tbody"})
    
    # готовим Заголовки
    headers.append('дата')
    for th in arrival_table.findAll('th', class_="th"):
        headers.append( th.text.replace('\n', ' ').strip())

    # Парсим данные на одну из направлений (departure)
    for tr in departure_table.findAll('tr'):
        table_data = []
        table_data.append(str(date.today()))
        for td in tr.findAll('td', class_='td'):
            table_data.append(td.text)
        data.append(table_data)
    
    return  [headers] + data


# Записываем данные в файл
def write_file(data):
    with open( date.today().strftime('%Y-%m-%d') +'.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

write_file(parse(url))