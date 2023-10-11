import random
import matplotlib
import typing

import pandas as pd
import matplotlib.pyplot as plt


def dict_to_dataframe(test_dict):
    test_df = pd.DataFrame.from_dict(test_dict)
    return test_df

stats = {"country": ["Brazil", "Russia", "India", "China", "South Africa"],
       "capital": ["Brasilia", "Moscow", "New Dehli", "Beijing", "Pretoria"],
       "area": [8.516, 17.10, 3.286, 9.597, 1.221],
       "population": [200.4, 143.5, 1252, 1357, 52.98] }

stats_df = dict_to_dataframe(stats)


def get_column(test_df, column_name):
    return pd.Series(test_df[column_name])


def population_density(test_df):
    new_df = test_df.copy()
    new_df["density"] = new_df["population"] / new_df["area"]
    return new_df


def plot_population(test_df):
    fig = test_df.plot(x="country", y="population", kind="bar", title="Population of Countries")
    fig.set_xlabel("Country")
    fig.set_ylabel("Population")
    plt.show()
    return fig

print(plot_population(stats_df))


#StudentPerfomance

def csv_to_df(input_csv):
    df_data = pd.read_csv(input_csv)
    return df_data


def capitalize_columns(input_df):
    df_data_capitalized = input_df.copy()
    new_columns = []
    for col in df_data_capitalized.columns:
        if 'e' not in col:
            new_columns.append(col.upper())
        else:
            new_columns.append(col)
    df_data_capitalized.columns = new_columns
    return df_data_capitalized

student_df = csv_to_df("D:\GF\ECOPY_23241\data\StudentsPerformance.csv")
cap_df = capitalize_columns(student_df)
# with pd.option_context('display.max_columns', None):
    # print(cap_df)


def math_passed_count(input_df):
    passed = len(input_df[input_df["math score"] > 50])
    return passed

# print(math_passed_count(cap_df))

def did_pre_course(input_df):
    df_precourse = input_df[input_df["test preparation course"] == "completed"]
    return df_precourse

# print(did_pre_course(cap_df))

def average_scores(input_df):
    test_df = input_df.copy()
    test_df = test_df.groupby(["parental level of education"]).agg({
        "math score":"mean",
        "reading score":"mean",
        "writing score":"mean"
        }
    )
    return test_df

# print(average_scores(cap_df))


def add_age(input_df):
    df_data_with_age = input_df.copy()
    random.seed(42)
    df_data_with_age["age"] = [random.randint(18, 66) for _ in range(len(df_data_with_age))]
    return df_data_with_age


def female_top_score(input_df):
    female_df = input_df[input_df["gender"] == "female"].copy()
    female_df["total score"] = female_df["math score"] + female_df["reading score"] + female_df["writing score"]
    female_df.sort_values("total score")
    mytuple = (int(female_df["math score"].iloc[0]), int(female_df["reading score"].iloc[0]), int(female_df["writing score"].iloc[0]))
    return mytuple

# print(female_top_score(cap_df))

def add_grade(input_df):
    graded_df = input_df.copy()
    scores_columns = ["math score", "reading score", "writing score"]
    graded_df["percent"] = graded_df[scores_columns].sum(axis=1).div(300)
    graded_df["grade"] = 1
    graded_df.loc[graded_df["percent"] >= 0.5, "grade"] = 2
    graded_df.loc[graded_df["percent"] >= 0.66, "grade"] = 3
    graded_df.loc[graded_df["percent"] >= 0.8, "grade"] = 4
    graded_df.loc[graded_df["percent"] >= 0.9, "grade"] = 5
    return graded_df


# print(add_grade(cap_df))

