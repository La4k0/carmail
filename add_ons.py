import random

def available_prices():
    all_prices = []
    price = 500

    while price <= 50000:
        all_prices.append(price)

        if price < 12500:
            price += 500
        else:
            price += 2500
    return all_prices

available_prices()

def random_select_from_list(param):
    return random.choice(param)

def random_select_between_numbers(min_num, max_num):
    return random.randint(min_num, max_num)