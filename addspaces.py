import re

def add_spaces(data):
    data = data.replace(",", ".")
    numbers = re.findall(r'[-+×÷()]|\d[\d,.]*', data)
    for i, num in enumerate(numbers):
        if re.match(r'\d+\.?\d*', num):
            num_without_commas = num.replace(",", "")
            if '.' in num_without_commas:
                integer_part, decimal_part = num_without_commas.split('.')
                if len(integer_part) > 3:
                    formatted_integer_part = '{:,}'.format(int(integer_part)).replace(",", " ")
                    numbers[i] = formatted_integer_part + '.' + decimal_part
            else:
                if len(num_without_commas) > 3:
                    numbers[i] = '{:,}'.format(int(num_without_commas)).replace(",", " ")
    numbers = str(''.join(numbers))
    numbers = numbers.replace(".", ",")
    return numbers


















