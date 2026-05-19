import re
import ast
import json
import requests
import urllib


def extract_entity_details(html_text):
    match = re.search(r"initEmbed\((\[.*\])\);", html_text, re.DOTALL)

    if not match:
        raise Exception("initEmbed data not found")

    raw = match.group(1)
    python_text = raw.replace("null", "None")
    data = ast.literal_eval(python_text)
    result = {}

    try:
        result["language"] = data[7][0]
    except:
        pass

    try:
        endpoints = data[8]

        result["api_endpoints"] = {
            "entity_details": endpoints[3],
            "upgrade": endpoints[4],
            "record": endpoints[6],
        }
    except:
        pass

    try:
        result["session_token"] = data[17]
    except:
        pass

    try:
        map_info = data[21][0]

        result["map_view"] = {
            "zoom": map_info[3],
            "center_lng": map_info[0][1],
            "center_lat": map_info[0][2],
            "map_scale": map_info[0][0],
        }
    except:
        pass

    try:
        place = data[21][3]

        result["place"] = {
            "google_maps_id": place[0][0],
            "entity_id": place[29],
            "cid": place[0][0],
            "full_address": place[1],
            "short_address": place[13],
            "country": place[2][0],
            "latitude": place[0][2][0],
            "longitude": place[0][2][1],
            "place_type": place[27],
            "google_cid": place[14],
            "search_token": place[30],
        }

    except Exception as e:
        result["place_error"] = str(e)

    try:
        bbox = data[5][3][0][13][0][11]

        result["bounding_box"] = {
            "southwest": {"lat": bbox[0][0] / 1e7, "lng": bbox[0][1] / 1e7},
            "northeast": {"lat": bbox[1][0] / 1e7, "lng": bbox[1][1] / 1e7},
        }

    except:
        pass

    try:
        result["raw_place_data"] = data[21][3]
    except:
        pass

    return result

def get_map_details_from_adrress_str(address:str):
    url = "https://maps.google.com/maps?q={address};&z=16&output=embed".format(address=urllib.parse.quote(address))
    data = requests.get(url)
    return extract_entity_details(data.text)

get_map_details_from_adrress_str("Zydus Healthcare Ltd., Village Mandoli, Mandoli, New Delhi, 201102")

################## Output ###################
"""{
    "language": "en_US",
    "api_endpoints": {
        "entity_details": "/maps/api/js/ApplicationService.GetEntityDetails",
        "upgrade": "/maps/embed/upgrade204",
        "record": "/maps/embed/record204",
    },
    "session_token": "6fILaoiZM87eseMPw8X2gAM",
    "map_view": {
        "zoom": 13.10000038146973,
        "center_lng": 77.31569379999999,
        "center_lat": 28.7137778,
        "map_scale": 3499.192891881535,
    },
    "place": {
        "google_maps_id": "0x390cfbdb5a692065:0x220f1706f1cc7615",
        "entity_id": None,
        "cid": "0x390cfbdb5a692065:0x220f1706f1cc7615",
        "full_address": "Zydus Healthcare Ltd.",
        "short_address": "MJ 6 & 6A, J R Complex, Gate no 2, Village Mandoli, Mandoli, New Delhi, Uttar Pradesh 201102",
        "country": "MJ 6 & 6A, J R Complex, Gate no 2, Village Mandoli",
        "latitude": 28.7137778,
        "longitude": 77.31569379999999,
        "place_type": "ChIJZSBpWtv7DDkRFXbM8QYXDyI",
        "google_cid": None,
        "search_token": "0ahUKEwjIscKazcSUAxVOb2wGHcOiHTAQ8BcIAygA",
    },
    "raw_place_data": [
        [
            "0x390cfbdb5a692065:0x220f1706f1cc7615",
            "Zydus Healthcare Ltd., MJ 6 & 6A, J R Complex, Gate no 2, Village Mandoli, Mandoli, New Delhi, Uttar Pradesh 201102",
            [28.7137778, 77.31569379999999],
            "2454205640534160917",
        ],
        "Zydus Healthcare Ltd.",
        [
            "MJ 6 & 6A, J R Complex, Gate no 2, Village Mandoli",
            "Mandoli",
            "New Delhi, Uttar Pradesh 201102",
        ],
        3,
        "6 reviews",
        None,
        None,
        "079 2686 8100",
        None,
        None,
        None,
        [
            "/url?q=http://zyduscadila.com/&opi=79508299&sa=U&ved=0ahUKEwjIscKazcSUAxVOb2wGHcOiHTAQ61gIFigQ&usg=AOvVaw0iKInRMGRdtOsNlgJzbLqQ",
            "zyduscadila.com",
            None,
            "0ahUKEwjIscKazcSUAxVOb2wGHcOiHTAQ61gIFigQ",
        ],
        "Pharmaceutical company",
        "MJ 6 & 6A, J R Complex, Gate no 2, Village Mandoli, Mandoli, New Delhi, Uttar Pradesh 201102",
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        "ChIJZSBpWtv7DDkRFXbM8QYXDyI",
        None,
        None,
        "0ahUKEwjIscKazcSUAxVOb2wGHcOiHTAQ8BcIAygA",
        "जयदुस हेल्थकेयर एलटीडी.",
        None,
        ["tel:07926868100"],
        None,
        None,
        None,
        1,
        [
            "0ahUKEwjIscKazcSUAxVOb2wGHcOiHTAQqtMBCA4oCg",
            ["7JWVP878+G7"],
            ["P878+G7 Mandoli, Delhi"],
            2,
        ],
        [
            None,
            [
                None,
                None,
                None,
                1,
                ["Open now", [[0, 8, [None, [4279862841, 4285388172]]]]],
            ],
            2,
        ],
    ],
}
"""
#########################################################
