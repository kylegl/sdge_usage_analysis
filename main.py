from constants import pricing_models
from standard_pricing_model import get_standard_cost
from timing_pricing_model import get_timing_price_model_cost
from utils import (
    group_by_month,
    load_data,
)

price_model_calculator_map = {
    "standard": get_standard_cost,
    "tou_dr1": get_timing_price_model_cost,
    "tou_dr2": get_timing_price_model_cost,
}


def main():
    data = load_data()

    grouped_by_month = group_by_month(data)

    for month_data in grouped_by_month:
        print(f"\n Month: {month_data[0]['Date']}")
        for price_model in pricing_models:
            cost = price_model_calculator_map[price_model["name"]](month_data, price_model)

            print(f"{price_model['name']} cost: {cost}")


main()
