# IHPJPL


# 1
def evens_from_list(input_list):
    even_list = []
    for i in input_list:
        if i % 2 == 0:
            even_list.append(i)
    return even_list


# 2
def every_element_is_odd(input_list):
    is_odd = True
    for i in input_list:
        if i % 2 == 0:
            is_odd = False
    return is_odd


# 3
def kth_largest_in_list(input_list, kth_largest):
    input_list.sort(reverse=True)
    element = input_list[kth_largest-1]
    return element


# 4
def cumavg_list(input_list):
    avg_list = []
    i = 0
    while i < len(input_list):
        avg_list.append(int(avguntilnow(input_list, i)))
        i += 1
    return avg_list


def avguntilnow(input_list, element):
    i = 0
    s = 0
    while i <= element:
        s += input_list[i]
        i += 1
    return s/(element + 1)


# 5
def element_wise_multiplication(input_list1, input_list2):
    result = []
    n = 0
    while n < len(input_list1):
        result.append(input_list1[n] * input_list2[n])
        n += 1
    return result


# 6
def merge_lists(*lists):
    result = []
    for l in lists:
        for i in l:
            result.append(i)
    return result


# 7
def squared_odds(input_list):
    result = []
    for i in input_list:
        if i % 2 == 1:
            result.append(i*i)
    return result


# 8
def reverse_sort_by_key(input_dict):
    result = dict(sorted(input_dict.items(), reverse=True))
    return result


# 9
def sort_list_by_divisibility(input_list):
    by_two = []
    by_five = []
    by_two_and_five = []
    by_none = []
    for i in input_list:
        if i % 2 == 0 and i % 5 == 0:
            by_two_and_five.append(i)
        elif i % 5 == 0:
            by_five.append(i)
        elif i % 2 == 0:
            by_two.append(i)
        else:
            by_none.append(i)
    result_dict = {
        'by_two': by_two,
        'by_five': by_five,
        'by_two_and_five': by_two_and_five,
        'by_none': by_none
    }
    return result_dict