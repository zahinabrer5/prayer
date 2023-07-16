# import re
# import os
import json
import requests
from bs4 import BeautifulSoup

url = 'https://www.islamicfinder.org/world/canada/6094817/ottawa-prayer-times/'
soup = BeautifulSoup(requests.get(url).content, 'html.parser')

prayer_names = soup.find_all('span', class_='prayername')
prayer_times = soup.find_all('span', class_='prayertime')
next_prayer = json.loads(soup.find(id='common-config').text.strip())["nextPrayer"][5:]
next_prayer_arr = ['fajar', 'dhuhar', 'asr', 'maghrib', 'isha']
curr_prayer = next_prayer_arr[next_prayer_arr.index(next_prayer)-1]

# times = []

bold = '\033[1m'
red = '\033[0;41m'
green = '\033[0;42m'
nc = '\033[0m' # No color

print(f'{bold}+---------+----------+')
print(f'{bold}| Prayer  | Time     |')
print(f'{bold}+---------+----------+')
for i in range(6):
    prayer_name = prayer_names[i].text.strip()
    prayer_time = prayer_times[i].text.strip()
    space = ' '*(8-len(prayer_name))

    upcoming = prayer_name.lower() == next_prayer
    if prayer_name == 'Fajr' and next_prayer == 'fajar':
        upcoming = True
    if prayer_name == 'Dhuhr' and next_prayer == 'dhuhar':
        upcoming = True
    color = red if upcoming else nc

    current = prayer_name.lower() == curr_prayer
    if prayer_name == 'Fajr' and curr_prayer == 'fajar':
        current = True
    if prayer_name == 'Dhuhr' and curr_prayer == 'dhuhar':
        current = True
    color = green if current else color

    print(f'{color}{bold}| {prayer_name}{space}| {prayer_time} |{nc}')
    print(f'{bold}+---------+----------+')

    """
    if prayer_name != 'Sunrise':
        splitted = re.split('[: ]', prayer_time)
        m = int(splitted[1])
        h = int(splitted[0])
        if splitted[2] == 'PM' and h != 12:
            h += 12
        times.append(f'{m} {h}')
    """

print(nc, end='')

"""
working_dir = '$HOME/code/prayer/'

cronfile = working_dir+'times.txt'

with open(cronfile, 'w') as f:
    f.write(f'5 0 * * * {working_dir}dist/app/app\n')
    for i in range(5):
        adhan = 'fajr' if i == 0 else 'adhan'
        f.write(f'{times[i]} * * * ffplay -nodisp -autoexit {working_dir+adhan}.mp3 >/dev/null 2>&1\n')

os.system(f'crontab {cronfile}')
"""
