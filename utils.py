import pandas as pd
import json
from datetime import datetime
from constants import tiers
import matplotlib.pyplot as plt


def load_data():
    with open("data.json") as f:
        return json.load(f)


def get_month(date):
    return datetime.strptime(date, "%m/%d/%Y").month


def get_day(date):
    return datetime.strptime(date, "%m/%d/%Y").day


def get_days(data):
    return set([get_day(entry["Date"]) for entry in data])


def get_months(data):
    return set([get_month(entry["Date"]) for entry in data])


def group_by_month(data):
    months = get_months(data)

    for month in months:
        yield list(filter(lambda x: get_month(x["Date"]) == month, data))


def group_by_day(month_data):
    days = get_days(month_data)

    for day in days:
        yield list(filter(lambda x: get_day(x["Date"]) == day, month_data))


def filter_by_time_range(day_data, range):
    start, end = range

    return list(
        filter(
            lambda x: convert_time_12h_to_24h(x["Start Time"]) >= start
            and convert_time_12h_to_24h(x["Start Time"]) < end,
            day_data,
        )
    )


def sum_kwh(data):
    total = 0
    for entry in data:
        total += entry["Net"]
    return round(total, 2)


def get_cost(kwh, price):
    return round(kwh * price, 2)


def get_tier(kwh):
    for tier in tiers:
        start, end = tier["range"]

        if kwh >= start and kwh < end:
            return tier['name']


def convert_time_12h_to_24h(time_str):
    raw_time, AM_PM = time_str.split()
    time = int(raw_time[:-3])

    if AM_PM == "PM" and time != 12:
        time = time + 12

    if AM_PM == "AM" and time == 12:
        time = 0

    return time


def sort_kwh_by_tier(kwh):
    result = []

    for tier in tiers:
        start, end = tier["range"]

        if kwh >= end:
            result.append((tier["name"], end))

        if kwh >= start and kwh < end:
            result.append((tier["name"], kwh - start))

    return result


def get_time_range(time):
    time = int(time)
    if time > 12:
        return "PM"

    return "AM"


def create_pivot_table(csv_path):
    df = pd.read_csv(csv_path, skiprows=13)

    df["Start Time"] = df["Start Time"].apply(convert_time_12h_to_24h)

    grp = df.groupby("Start Time")

    print(grp["Date"])

    print(df)
    pivot_table = grp.pivot_table(
        df, "Consumption", "Date", "Start Time", aggfunc="sum", margins=True
    )

    print(pivot_table)



def get_month_cost(month_group, price_model):
    for day, day_group in month_group.groupby(month_group.Date.dt.day):
        entries_in_timing_range = day_group[day_group['Start Time'].dt.hour.between(0, 6, 'left')]
        print(entries_in_timing_range)

