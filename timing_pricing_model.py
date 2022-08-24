from utils import (
    filter_by_time_range,
    get_tier,
    group_by_day,
    sum_kwh,
)


def initialize_timing_data(price_model):
    timing_data = {}
    tiers = price_model["pricing"].keys()
    categories = price_model["timing"].keys()

    for tier in tiers:
        tier_obj = timing_data.setdefault(tier, {})

        for category in categories:
            tier_obj.setdefault(category, 0)

    return timing_data


def get_category_kwh(day_data, ranges):
    category_total_kwh = 0

    for range in ranges:
        range_data = filter_by_time_range(day_data, range)
        category_total_kwh += sum_kwh(range_data)

    return category_total_kwh


def get_partial_kwh_for_tiers(kwh, net_kwh, tier_range):
    start, end = tier_range

    next_tier_kwh = net_kwh - end
    prev_tier_kwh = kwh - next_tier_kwh

    return (prev_tier_kwh, next_tier_kwh)


def get_timing_data_per_day(month_data, price_model):
    data = group_by_day(month_data)
    month_net_kwh = 0
    current_tier = get_tier(0)
    monthly_timing_data = []

    for day_data in data:
        day_timing_data = initialize_timing_data(price_model)

        for category, ranges in price_model["timing"].items():
            category_kwh = get_category_kwh(day_data, ranges)

            month_net_kwh += category_kwh

            next_tier = get_tier(month_net_kwh)

            if next_tier["name"] == current_tier["name"]:
                day_timing_data[current_tier["name"]][category] += category_kwh

            if next_tier["name"] != current_tier["name"]:
                prev_tier_kwh, next_tier_kwh = get_partial_kwh_for_tiers(
                    category_kwh, month_net_kwh, current_tier["range"]
                )

                day_timing_data[current_tier["name"]][category] += prev_tier_kwh
                day_timing_data[next_tier["name"]][category] += next_tier_kwh

                current_tier = next_tier

        monthly_timing_data.append(day_timing_data)

    return monthly_timing_data


def sum_daily_timing_data(daily_data, price_model):
    timing_data = initialize_timing_data(price_model)

    for entry in daily_data:
        for tier, data in entry.items():
            for category, kwh in data.items():
                timing_data[tier][category] += kwh

    return timing_data


def sum_costs_for_month(month_data, price_model):
    cost = 0

    for tier, data in month_data.items():
        tier_categories = price_model["pricing"][tier]
        tier_cost = 0

        for category, kwh in data.items():
            tier_cost += kwh * tier_categories[category]

        cost += tier_cost

    return round(cost, 2)


def get_timing_price_model_cost(month_data, price_model):

    daily_data = get_timing_data_per_day(month_data, price_model)

    month_data = sum_daily_timing_data(daily_data, price_model)

    return sum_costs_for_month(month_data, price_model)
