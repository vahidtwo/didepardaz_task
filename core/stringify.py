ENG_TO_PERSIAN_MAP = {
    "0": "۰",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "۴",
    "5": "۵",
    "6": "۶",
    "7": "۷",
    "8": "۸",
    "9": "۹",
}


def comma_seperated(value: int) -> str:
    return "{:,}".format(value)


def persian_comma_seperated(value: int) -> str:
    cs = comma_seperated(value)
    for key, value in ENG_TO_PERSIAN_MAP.items():
        cs = cs.replace(key, value)

    return cs


def persianize(target: str) -> str:
    for key, value in ENG_TO_PERSIAN_MAP.items():
        target = target.replace(key, value)

    return target
