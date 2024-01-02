import re

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

for h1 in range(24):
    for start_m in range(60):
        for h2 in range(24):
            for end_m in range(60):
                start_h = h1 % 12
                if start_h == 0:
                    start_h = 12

                end_h = h2 % 12
                if end_h == 0:
                    end_h = 12

                start_p = 'PM' if h1 > start_h or h1 == 12 else 'AM'
                end_p = 'PM' if h2 > end_h or h2 == 12 else 'AM'

                start_h_str = ('0' if start_h < 10 else '')+str(start_h)
                start_m_str = ('0' if start_m < 10 else '')+str(start_m)

                end_h_str = ('0' if end_h < 10 else '')+str(end_h)
                end_m_str = ('0' if end_m < 10 else '')+str(end_m)

                start = f'{start_h_str}:{start_m_str} {start_p}'
                end = f'{end_h_str}:{end_m_str} {end_p}'
                print(f'abs({end} - {start}) = {time_diff(start, end)}')
