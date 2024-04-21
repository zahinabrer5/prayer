# import re
# import os
import json
import requests
# import time
from datetime import datetime, time
from bs4 import BeautifulSoup

def pad_right(s, c, l):
    return s+c*(l-len(s))

"""
fmt = '%I:%M %p'

def time_diff(start, end):
    start_h, start_m, start_p = re.split(r'[: ]', start)
    start_h = int(start_h) % 12
    start_m = int(start_m)
    end_h, end_m, end_p = re.split(r'[: ]', end)
    end_h = int(end_h) % 12
    end_m = int(end_m)

    diff_h = abs(end_h - start_h)
    diff_m = abs(end_m - start_m)

    if end_p != start_p:
        diff_h = 12 - diff_h

    str_h = ('0' if diff_h < 10 else '')+str(diff_h)
    str_m = ('0' if diff_m < 10 else '')+str(diff_m)

    return str_h+':'+str_m
"""

def military_time(t):
    space_splitted = t.split(' ')
    a = space_splitted[1]
    colon_splitted = space_splitted[0].split(':')
    h = int(colon_splitted[0])
    if a == 'PM' and h != 12:
        h += 12
    elif a == 'AM' and h == 12:
        h -= 12
    return str(h)+':'+colon_splitted[1]

def str_to_time(t):
    return time(*(map(int, t.split(':'))))

# increment day of Islamic month if current time has passed Maghrib time
def print_date(prayer_times, date_islamic):
    offset = 0
    maghrib = military_time(prayer_times[4].text.strip())
    maghrib_time = str_to_time(maghrib)
    if datetime.today().time() > maghrib_time:
        offset += 1
    date_islamic_splitted = date_islamic.split(' ')
    day_of_islamic_month = int(date_islamic_splitted[0])+offset
    date_islamic = ' '.join([
        str(day_of_islamic_month),
        date_islamic_splitted[1],
        date_islamic_splitted[2]
    ])
    print(f'{bold}{date_islamic}')
    print(f'{bold}{date_greg}')

url = 'https://www.islamicfinder.org/world/canada/6094817/ottawa-prayer-times/'

use_colour = True

bold = '\033[1m'
red = '\033[0;41m'
green = '\033[0;42m'
nc = '\033[0m' # No color

if not use_colour:
    bold = ''
    red = ''
    green = ''
    nc = ''

try:
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    non_break_space = u'\xa0'
    date_greg = soup.select_one('div.pt-date.font-dark.font-sm>p') \
        .text.strip() \
        .replace(non_break_space, ' ')
    date_islamic = soup.select_one('.font-weight-bold.pt-date-right') \
        .text.strip() \
        .replace(non_break_space, ' ')

    prayer_names = soup.find_all('span', class_='prayername')
    prayer_times = soup.find_all('span', class_='prayertime')

    print_date(prayer_times, date_islamic)

    next_prayer = json.loads(
        soup.find(id='common-config').text.strip())["nextPrayer"][5:]
    next_prayer_arr = ['fajar', 'dhuhar', 'asr', 'maghrib', 'isha']
    curr_prayer = next_prayer_arr[next_prayer_arr.index(next_prayer)-1]

    # times = []

    print(f'{bold}+---------+----------+')
    print(f'{bold}| Prayer  | Time     |')
    print(f'{bold}+---------+----------+')
    """
    print(f'{bold}+---------+----------+-----------+')
    print(f'{bold}| Prayer  | Time     | Remaining |')
    print(f'{bold}+---------+----------+-----------+')
    """
    for i in range(6):
        prayer_name = prayer_names[i].text.strip()
        prayer_time = prayer_times[i].text.strip()
        padded_prayer_name = pad_right(prayer_name, ' ', 8)

        upcoming = prayer_name.lower() == next_prayer
        if prayer_name == 'Fajr' and next_prayer == 'fajar':
            upcoming = True
        if prayer_name == 'Dhuhr' and next_prayer == 'dhuhar':
            upcoming = True
        color = red if upcoming else nc

        """
        msg = ' '*9
        if upcoming:
            now = time.strftime(fmt)
            diff = time_diff(now, prayer_time)
            msg = pad_right(diff, ' ', 9)
        """

        current = prayer_name.lower() == curr_prayer
        if prayer_name == 'Fajr' and curr_prayer == 'fajar':
            current = True
        if prayer_name == 'Dhuhr' and curr_prayer == 'dhuhar':
            current = True
        color = green if current else color

        # s = f'| {padded_prayer_name}| {prayer_time} | {msg} |{nc}'
        s = f'| {padded_prayer_name}| {prayer_time} |{nc}'
        print(f'{color}{bold}'+s)
        print(f'{bold}+---------+----------+')
        # print(f'{bold}+---------+----------+-----------+')

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
            f.write(f'{times[i]} * * * ffplay -nodisp -autoexit \
                {working_dir+adhan}.mp3 >/dev/null 2>&1\n')

    os.system(f'crontab {cronfile}')
    """

except:
    print(f'{red}ERROR{nc} :(\nOpen URL manually:\n{url}')
