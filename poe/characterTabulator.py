# 1) Make sure the input file is named 'input.txt'
# 2) Make sure dividers are 3+ dashes and have the character name on the same line
#       Ex: ------- Tornado Shot Raider
# 3) All costs should be suffixed by 'c' or 'ex'
# 4) The tabulator will ignore descriptions of expenses

import re
DIVIDER_PATTERN = re.compile('(-){3,}')
MONEY_PATTERN = re.compile('(\d|\d\s)+(c|ex)')


def prettify(char_dict: dict) -> None:
    print('Chaos Spent | Character')
    print('-' * 50)
    for char, chaos in char_dict.items():
        print(str(chaos).rjust(11, ' ') + f' | {char}')


if __name__ == '__main__':
    chars = dict()
    exalt_price = int(input('Enter current exalt price: '))
    cur_char = ''
    line_num = 0
    with open('input.txt', 'r') as infile:
        for line in infile:
            line_num += 1
            if re.search(DIVIDER_PATTERN, line) is not None:
                cur_char = line.replace('-', '')[:30].strip()
                chars[cur_char] = 0
            else:
                money = re.search(MONEY_PATTERN, line)
                try:
                    raw_money = money.group()
                    if 'c' in raw_money:
                        chars[cur_char] += int(raw_money.rstrip('c'))
                    else:
                        chars[cur_char] += exalt_price * int(raw_money.rstrip('ex'))
                except AttributeError as err:
                    print(f'Error for \'{cur_char}\' on Line #{line_num}: {line}')
                    print(err)
        prettify(chars)
