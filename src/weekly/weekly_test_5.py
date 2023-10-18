from pathlib import Path
import pandas as pd
import random
import src.utils
import src.weekly



file_to_load = Path.cwd().parent.joinpath('data').joinpath('chipotle.tsv')

food = pd.read_csv(file_to_load)


def change_price_to_float(input_df):
    local_df = input_df.copy(deep=True)
    local_df["item_price"] = local_df["item_price"].astype(float)
    return local_df


food = change_price_to_float(food)

def number_of_observations(input_df):
    return len(input_df)

def items_and_prices(input_df):
    result_df = input_df[["item_name", "item_price"]]
    return result_df

def sorted_by_price(input_df):
    local_df = input_df.sort_values("item_price")
    return local_df

def avg_price(input_df):
    avg = input_df["item_price"].mean()
    return avg

def unique_items_over_ten_dollars(input_df):
    local_df = input_df[["item_name", "choice_description", "item_price"]].copy(deep=True)
    local_df = local_df[local_df["item_price"] > 10]
    local_df.drop_duplicates()
    return local_df


def items_starting_with_s(input_df):
    local_df = input_df.copy(deep=True)
    local_df = local_df[local_df["item_name"].str.startswith('s')]
    return local_df

def first_three_columns(input_df):
    local_df = input_df.iloc[: , :3]
    return local_df

def all_columns_except_last_two(input_df):
    local_df = input_df.iloc[:, :-2]
    return local_df

def sliced_view(input_df, columns_to_keep, column_to_filter, rows_to_keep):
    local_df = input_df.loc[rows_to_keep, columns_to_keep]
    local_df.filter(column_to_filter)
    return local_df

def generate_quartile(input_df):
    local_df = input_df.copy(deep=True)
    local_df[local_df["item_price"] < 10, "Quartile"] = "low-cost"
    local_df[20 > local_df["item_price"] >= 10, "Quartile"] = "medium-cost"
    local_df[30 > local_df["item_price"] >= 20, "Quartile"] = "high-cost"
    local_df[local_df["item_price"] >= 30, "Quartile"] = "premium"
    return local_df

def average_price_in_quartiles(input_df):
    local_df = input_df.copy(deep=True)
    local_df = local_df.groupby("Quartile").agg({
        "item_price":"mean"
    }
    )
    return local_df

def minmaxmean_price_in_quartile(input_df):
    local_df = input_df.copy(deep=True)
    local_df = local_df.groupby("Quartile").agg({
        "item_price":["min", "max", "mean"]
    })
    return local_df

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

def gen_uniform_mean_trajectories(distribution, number_of_trajectories, length_of_trajectory):
    random.seed(42)
    result = []
    for a in range(number_of_trajectories):
        templist = []
        for b in range(length_of_trajectory):
            templist.append(distribution.gen_rand())
            result.append(cumavg_list(templist))
        templist.clear()
    return result


def gen_logistic_mean_trajectories(distribution, number_of_trajectories, length_of_trajectory):
    random.seed(42)
    result = []
    for a in range(number_of_trajectories):
        templist = []
        for b in range(length_of_trajectory):
            templist.append(distribution.gen_rand())
            result.append(cumavg_list(templist))
        templist.clear()
    return result

def gen_laplace_mean_trajectories(distribution, number_of_trajectories, length_of_trajectory):
    random.seed(42)
    result = []
    for a in range(number_of_trajectories):
        templist = []
        for b in range(length_of_trajectory):
            templist.append(distribution.gen_rand())
            result.append(cumavg_list(templist))
        templist.clear()
    return result


def gen_cauchy_mean_trajectories(distribution, number_of_trajectories, length_of_trajectory):
    random.seed(42)
    result = []
    for a in range(number_of_trajectories):
        templist = []
        for b in range(length_of_trajectory):
            templist.append(distribution.gen_rand())
            result.append(cumavg_list(templist))
        templist.clear()
    return result


def gen_chi2_mean_trajectories(distribution, number_of_trajectories, length_of_trajectory):
    random.seed(42)
    result = []
    for a in range(number_of_trajectories):
        templist = []
        for b in range(length_of_trajectory):
            templist.append(distribution.gen_rand())
            result.append(cumavg_list(templist))
        templist.clear()
    return result