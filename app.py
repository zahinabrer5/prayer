import requests
from bs4 import BeautifulSoup

url = 'https://www.islamicfinder.org/world/canada/6094817/ottawa-prayer-times/'
soup = BeautifulSoup(requests.get(url).content, 'html.parser')

prayer_names = soup.find_all('span', class_='prayername')
prayer_times = soup.find_all('span', class_='prayertime')
for i in range(6):
    prayer_name = prayer_names[i].text.strip()
    prayer_time = prayer_times[i].text.strip()
    print(f'{prayer_name}\t\t{prayer_time}')
