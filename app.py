import re
import os
import requests
from bs4 import BeautifulSoup

url = 'https://www.islamicfinder.org/world/canada/6094817/ottawa-prayer-times/'
soup = BeautifulSoup(requests.get(url).content, 'html.parser')

prayer_names = soup.find_all('span', class_='prayername')
prayer_times = soup.find_all('span', class_='prayertime')

times = []

for i in range(6):
    prayer_name = prayer_names[i].text.strip()
    prayer_time = prayer_times[i].text.strip()
    print(f'{prayer_name}\t\t{prayer_time}')

    if prayer_name != 'Sunrise':
        splitted = re.split('[: ]', prayer_time)
        m = int(splitted[1])
        h = int(splitted[0])
        if splitted[2] == 'PM' and h != 12:
            h += 12
        times.append(f'{m} {h}')

working_dir = '/home/zahin/code/prayer/'

cronfile = working_dir+'times.txt'

with open(cronfile, 'w') as f:
    f.write(f'5 0 * * * {working_dir}dist/app/app\n')
    for i in range(5):
        adhan = 'fajr' if i == 0 else 'adhan'
        f.write(f'{times[i]} * * * ffplay -nodisp -autoexit {working_dir+adhan}.mp3 >/dev/null 2>&1\n')

os.system(f'crontab {cronfile}')
