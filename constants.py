tiers = [
    {
        "name": "tier_1",
        "range": (0, 351),
    },
    {
        "name": "tier_2",
        "range": (351, 1080),
    },
    {
        "name": "tier_3",
        "range": (1080, float("inf")),
    },
]

price_models = [
    {
        "name": "standard",
        "rate": {
            "tier_1": {
                "default": 0.393,
            },
            "tier_2": {
                "default": 0.495,
            },
        },
    },
    {
        "name": "tou_dr1",
        "rate": {
            "tier_1": {
                "super_off_peak": 0.234,
                "off_peak": 0.356,
                "peak": 0.588,
            },
            "tier_2": {
                "super_off_peak": 0.336,
                "off_peak": 0.458,
                "peak": 0.69,
            },
        },
        "time_ranges": {
            "super_off_peak": [(0, 6)],
            "off_peak": [(6, 16), (21, 24)],
            "peak": [(16, 21)],
        },
    },
    {
        "name": "tou_dr2",
        "rate": {
            "tier_1": {
                "off_peak": 0.303,
                "peak": 0.594,
            },
            "tier_2": {
                "off_peak": 0.405,
                "peak": 0.696,
            },
        },
        "time_ranges": {
            "off_peak": [(0, 16), (21, 24)],
            "peak": [(16, 21)],
        },
    },
]
