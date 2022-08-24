from utils import sum_kwh, get_cost, sort_kwh_by_tier


def get_standard_cost(month_data, price_model):
    net_kwh = sum_kwh(month_data)
    kwh_hour_tiers = sort_kwh_by_tier(net_kwh)
    cost = 0

    for tier in kwh_hour_tiers:
        tier_name, kwh = tier
        tier_price = price_model["pricing"][tier_name]
        cost += get_cost(kwh, tier_price)

    return cost
