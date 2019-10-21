#!/usr/bin/env python3


from bs4 import BeautifulSoup
import requests


URL = "https://na.finalfantasyxiv.com/lodestone/worldstatus/"


def _query_lodestone(url=URL):
    """
    Returns a Requests module Response object from Lodestone.
    requests.Response.raise_for_status() is used to raise an exception when the
    resposne is non-HTTP-200.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response


def _status_map(html=None):
    """
    Returns a dictionary of region -> datacenter -> servers -> status, or raise
    an exception if the underlying API returns non-HTTP-200 response.

    Example: {
        "North America Data Center":
            "Crystal": {
                "Goblin": "Online",
            },
    }

    This is done by parsing source HTML and looking for specific CSS classes.
    The classes update overtime, so this function will need to mutate to match
    new, future logic.
    """
    if not html:
        html = _query_lodestone().text

    bs = BeautifulSoup(html, "html.parser")
    mapping = {}

    CSS_REGION = "data-region"
    CSS_DATACENTER_GROUP = "world-dcgroup__item"
    CSS_DATACENTER_TITLE = "world-dcgroup__header"
    CSS_WORLD = "world-list__item"
    CSS_WORLD_TITLE = "world-list__world_name"
    CSS_WORLD_STATUS = "world-list__status_icon"
    CSS_WORLD_CATEGORY = "world-list__world_category"

    for r in bs.find(class_="world__tab").find_all("li"):
        r_name = r.a.span.string.strip()
        r_indx = r[CSS_REGION]
        mapping[r_name] = {}
        for dc in bs.find_all(attrs={CSS_REGION: r_indx})[1].find_all(class_=CSS_DATACENTER_GROUP):
            dc_name = dc.find(class_=CSS_DATACENTER_TITLE).string.strip()
            mapping[r_name][dc_name] = {}

            for w in dc.find_all(class_=CSS_WORLD):
                w_name = w.find(class_=CSS_WORLD_TITLE).p.string.strip()
                w_status = w.find(
                    class_=CSS_WORLD_STATUS).i["data-tooltip"].strip()
                w_category = w.find(class_=CSS_WORLD_CATEGORY).p.string.strip()
                mapping[r_name][dc_name][w_name] = "{} ({})".format(
                    w_status, w_category)

    return mapping


def status(target=None):
    """
    Returns the online status of the input target, or raise an exception if the
    underlying API returns non-HTTP-200 response.

    If the target is a specific server, it returns that mapping:
        {"Goblin": "Online"}

    If the target is a datacetner, it returns that mapping:
        {
            "Goblin": "Online",
            "Malboro": "Online",
        }

    If the target is an empty string or None, returns the whole mapping:
        {
            "Crystal": {
                "Goblin": "Online",
                "Malboro": "Online",
            },
            "Elemental": {
                "Gungnir": "Online",
                "Carbuncle": "Online",
            },
        }

    The function performs beginning partial matching and is case-insensitive.
    """
    mapping = _status_map()

    if not target:
        return mapping

    for r in mapping:
        if r.lower().startswith(target.lower()):
            return {r: mapping[r]}
        for dc in mapping[r]:
            if dc.lower().startswith(target.lower()):
                return {dc: mapping[r][dc]}
            for w in mapping[r][dc]:
                if w.lower().startswith(target.lower()):
                    return {w: mapping[r][dc][w]}

    return None


if __name__ == "__main__":
    import json
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else None
    print(json.dumps(status(target)))
