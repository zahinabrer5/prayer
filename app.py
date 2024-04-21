import json
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime, time


def pad_right(s, c, l):
    return s+c*(l-len(s))


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
def print_date(prayer_times, date_islamic, date_greg, bold):
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


def prayer(use_colour=True):
    url = 'https://www.islamicfinder.org/world/canada/6094817/ottawa-prayer-times/'

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

        nbsp = u'\xa0'
        date_greg = soup.select_one('div.pt-date.font-dark.font-sm>p') \
            .text.strip() \
            .replace(nbsp, ' ')
        date_islamic = soup.select_one('.font-weight-bold.pt-date-right') \
            .text.strip() \
            .replace(nbsp, ' ')

        prayer_names = soup.find_all('span', class_='prayername')
        prayer_times = soup.find_all('span', class_='prayertime')

        print_date(prayer_times, date_islamic, date_greg, bold)

        next_prayer = json.loads(
            soup.find(id='common-config').text.strip())["nextPrayer"][5:]
        next_prayer_arr = ['fajar', 'dhuhar', 'asr', 'maghrib', 'isha']
        curr_prayer = next_prayer_arr[next_prayer_arr.index(next_prayer)-1]

        print(f'{bold}+---------+----------+')
        print(f'{bold}| Prayer  | Time     |')
        print(f'{bold}+---------+----------+')
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

            current = prayer_name.lower() == curr_prayer
            if prayer_name == 'Fajr' and curr_prayer == 'fajar':
                current = True
            if prayer_name == 'Dhuhr' and curr_prayer == 'dhuhar':
                current = True
            color = green if current else color

            s = f'| {padded_prayer_name}| {prayer_time} |{nc}'
            print(f'{color}{bold}'+s)
            print(f'{bold}+---------+----------+')
        print(nc, end='')

    except:
        print(f'{red}ERROR{nc} :(\nOpen URL manually:\n{url}')


def main():
    use_colour = sys.argv[1] if len(sys.argv) > 1 else True
    prayer(use_colour)


if __name__ == '__main__':
    main()
