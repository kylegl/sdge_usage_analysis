from constants import tiers


def get_tier(kwh):
    for tier in tiers:
        start, end = tier["range"]

        if kwh >= start and kwh < end:
            return tier["name"]


def get_pricing_category(time, price_model):
    if not "time_ranges" in price_model:
        return "default"

    for category, time_ranges in price_model["time_ranges"].items():

        for range in time_ranges:
            start, end = range

            if time.hour >= start and time.hour < end:
                return category


def get_rate(row, price_model):
    return price_model["rate"][row["tier"]][row["rate_category"]]


def get_month_cost(month_group, price_model):
    month_group["cumulative_kwh"] = month_group["Consumption"].cumsum()
    month_group["tier"] = month_group["cumulative_kwh"].apply(get_tier)
    month_group["pricing_category"] = month_group["Start Time"].apply(
        lambda x: get_pricing_category(x, price_model)
    )
    month_group["rate"] = month_group.apply(
        lambda row: get_rate(row, price_model), axis=1
    )
    month_group["daily_cost"] = month_group["rate"] * month_group["Consumption"]

    return month_group["daily_cost"].sum()



