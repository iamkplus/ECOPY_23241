# 1
mylist = [17, 18, 3.14, "a", "alma"]
# 2
mylist2 = list((1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
# 3
print(mylist[1])
# 4
print(mylist[3])
# 5
print(max(mylist2))
# 6
print(mylist2.index(max(mylist2)))


# 7
def contains_value(input_list, element):
    contains_it = False
    for i in input_list:
        if i == element:
            contains_it = True
    return contains_it


# 8
def number_of_elements_in_list(input_list):
    return len(input_list)


# 9
def remove_every_element_from_list(input_list):
    input_list.clear()


# 10
def reverse_list(input_list):
    input_list.reverse()
    return input_list


# 11
def odds_from_list(input_list):
    oddlist = []
    for i in input_list:
        if i % 2 == 1:
            oddlist.append(i)
    return oddlist


# 12
def number_of_odds_in_list(input_list):
    num = 0
    for i in input_list:
        if i % 2 == 1:
            num += 1
    return num


# 13
def contains_odd(input_list):
    does_it = False
    for i in input_list:
        if i % 2 == 1:
            does_it = True
    return does_it


# 14
def second_largest_in_list(input_list):
    temp_list = input_list.sorted(reverse=True)
    return temp_list[1]

# 15
def sum_of_elements_in_list(input_list):
    sum = 0
    for i in input_list:
        sum += i
    return sum


# 16
def cumsum_list(input_list):
    newlist = []
    i = 0
    temp = 0
    while i < len(input_list):
        if i == 0:
            newlist.append(input_list[i])
        else:
            newlist.append(input_list[i] + newlist[i-1])
        i += 1
    return newlist


# 17
def element_wise_sum(input_list1, input_list2):
    i = 0
    output_list = []
    while i < len(input_list1):
        if input_list1[i] != None and input_list2[i] != None:
            output_list.append(input_list1[i] + input_list2[i])
            i += 1
        else:
            break
    return output_list


# 18
def subset_of_list(input_list, start_index, end_index):
    output = []
    i = start_index
    while i <= end_index:
        output.append(input_list[i])
        i += 1
    return output


# 19
def every_nth(input_list, step_size):
    output = []
    n = step_size
    i = 0
    while i < len(input_list):
        output.append(input_list[i])
        i += n
    return output


# 20
def only_unique_in_list(input_list):
    if len(set(input_list)) == len(input_list):
        return True
    else:
        return False


# 21
def keep_unique(input_list):
    temp = set(input_list)
    output = list(temp)
    return output


# 22
def swap(input_list, first_index, second_index):
    temp = input_list[first_index]
    input_list[first_index] = input_list[second_index]
    input_list[second_index] = temp
    return input_list


# 23
def remove_element_by_value(input_list, value_to_remove):
    input_list.remove(value_to_remove)
    return input_list

# 24
def remove_element_by_index(input_list, index):
    input_list.pop(index)
    return input_list

# 25
def multiply_every_element(input_list, multiplier):
    output = [i * multiplier for i in input_list]
    return output

# 2.1
thisdict = {
    "a": 9,
    "b": [12, "c"]
}

# 2.2
print(thisdict["a"])

# 2.3
print(thisdict.get("d"))

# 2.4
def remove_key(input_dict, key):
    input_dict.pop(key)
    return input_dict


# 2.5
def sort_by_key(input_dict):
    dict(sorted(input_dict.items()))
    return input_dict


# 2.6
def sum_in_dict(input_dict):
    sum = 0.0
    for i in input_dict.values():
        sum += i
    return sum

# 2.7
def merge_two_dicts(input_dict1, input_dict2):
    input_dict1.update(input_dict2)
    return input_dict1


# 2.8
def merge_dicts(*dicts):
    resultdict = {}
    for d in dicts:
        resultdict.update(d)
    return resultdict

# 2.9
def sort_list_by_parity(input_list):
    odd = []
    even = []
    for i in input_list:
        if i % 2 == 0:
            even.append(i)
        else:
            odd.append(i)
    resultdict = {
        "odd": odd,
        "even": even
    }
    return resultdict

# 2.10
def mean_by_key_value(input_dict):
    newdict = {}
    keys = input_dict.keys()
    for k in keys:
        newdict[k] = mean(input_dict[k])
    return newdict


def mean(input_list):
    return sum(input_list) / len(input_list)


# 2.11
def count_frequency(input_list):
    newdict = {}
    for i in input_list:
        if newdict.get(i) is None:
            newdict[i] = 1
        else:
            newdict[i] += 1
    return newdict