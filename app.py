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

# times = []

red = '\033[0;31m'
nc = '\033[0m' # No color

print('+---------+----------+')
print('| Prayer  | Time     |')
print('+---------+----------+')
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

    print(f'| {color}{prayer_name}{nc}{space}| {color}{prayer_time}{nc} |')
    print('+---------+----------+')

    """
    if prayer_name != 'Sunrise':
        splitted = re.split('[: ]', prayer_time)
        m = int(splitted[1])
        h = int(splitted[0])
        if splitted[2] == 'PM' and h != 12:
            h += 12
        times.append(f'{m} {h}')
    """

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
