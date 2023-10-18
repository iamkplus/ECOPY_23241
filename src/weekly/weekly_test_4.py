import pandas as pd
import typing
import matplotlib.pyplot as plt
import random
import src.weekly

euro12 = pd.read_csv(r"C:\Users\mnb-hallg-14\Documents\GitHub\ECOPY_23241\data\Euro_2012_stats_TEAM.csv")

def number_of_participants(input_df):
    return len(input_df["Team"])

print(number_of_participants(euro12))

def goals(input_df):
    test_df = input_df["Team", "Goals"]
    return test_df

def sorted_by_goal(input_df):
    test_df = input_df.copy()
    test_df = test_df.sort_values("Goals")
    return test_df

def avg_goal(input_df):
    avg_of_Goals = input_df["Goals"].mean()
    return avg_of_Goals

def countries_over_five(input_df):
    result = input_df[input_df["Goals"] >= 6]
    return result

def countries_starting_with_g(input_df):
    result = pd.DataFrame()
    result = input_df[input_df["Team"].str[0] == 'G']
    return result

def first_seven_columns(input_df):
    result = input_df[:, :7]
    return result

def every_colum_except_last_three(input_df):
    result = input_df[:, :-3]
    return result

def sliced_view(input_df, columns_to_keep, column_to_filter, rows_to_keep):
    result = input_df
    return result

def generate_quartile(input_df):
    result = input_df.copy()
    result["Quartile"] = 4
    result[result["Goals"] >= 3, "Quartile"] = 3
    result[result["Goals"] >= 5, "Quartile"] = 2
    result[result["Goals"] >= 6, "Quartile"] = 1
    return result

def average_yellow_in_quartiles(input_df):
    result = input_df.copy()
    result = result.groupby("Quartile").agg({
        "Passes":"mean"
    }
    )
    return result

def minmax_block_in_quartile(input_df):
    result = input_df.copy()
    result = result.groupby("Quartile").agg({
        "Blocks":["min", "max"]
    }
    )
    return result

def gen_pareto_mean_trajectories(pareto_distribution, number_of_trajectories, length_of_trajectory):
    random.seed(42)
    result = []
    for a in range(number_of_trajectories):
        templist = []
        for b in range(length_of_trajectory):
            templist.append(pareto_distribution.gen_rand())
            result.append(cumavg_list(templist))
        templist.clear()
    return result

def scatter_goals_shots(input_df):
    fig, ax = plt.subplots()
    ax.scatter(input_df["Goals"], input_df["Shots on target"])
    ax.set_xlabel("Goals")
    ax.set_ylabel("Shots on target")
    ax.set_title("Goals and Shot on target")
    plt.show()
    return fig, ax

def scatter_goals_shots_by_quartile(input_df):
    fig, ax = plt.subplots()
    ax.scatter(input_df["Goals"], input_df["Shots on target"], marker=input_df["Quartiles"], cmap="gray")
    ax.set_xlabel("Goals")
    ax.set_ylabel("Shots on target")
    ax.set_title("Goals and Shot on target")
    plt.show()
    return fig, ax

scatter_goals_shots_by_quartile(generate_quartile(euro12))

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


