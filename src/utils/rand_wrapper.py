import random

# 1
random.random()

# 2
random.randint(1, 100)

# 3
random.seed(42)
random.randint(1, 100)


# 4
def random_from_list(input_list):
    return random.choice(input_list)


# 5
def random_sublist_from_list(input_list, number_of_elements):
    return random.choices(input_list, k=number_of_elements)


# 6
def random_from_string(input_string):
    return random.choice(input_string)


# 7
def hundred_small_random():
    result = []
    i = 0
    while i < 100:
        result.append(random.random())
        i += 1
    return result


# 8
def hundred_large_random():
    result = []
    i = 0
    while i < 100:
        result.append(random.randint(10, 1000))
        i += 1
    return result


# 9
def five_random_number_div_three():
    result = []
    i = 0
    while i < 5:
        result.append(random.randint(3, 333) * 3)
        i += 1
    return result


# 10
def random_reorder(input_list):
    random.shuffle(input_list)
    return input_list


# 11
def uniform_one_to_five():
    return random.uniform(1.0, 5.0)
