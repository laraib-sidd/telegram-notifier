import requests
import os
import xmltodict
from datetime import datetime as dt
import pytz
from bs4 import BeautifulSoup


def calculate_time_difference(date_string):
    ist_dt = dt.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")
    ist_tz = pytz.timezone("Asia/Kolkata")
    now_dt = dt.now(ist_tz)
    total_seconds_passed = (now_dt - ist_dt).total_seconds()
    minutes_passed = total_seconds_passed / 60

    if minutes_passed >= 60:
        hours_passed = minutes_passed / 60
        return f"{hours_passed:.2f} hours have passed this post was created {ist_dt:%Y/%m/%d-%H:%M} hours"
    else:
        return f"{minutes_passed:.2f} minutes have passed this post was created {ist_dt:%Y/%m/%d-%H:%M} hours"


def convert_encoded_content_to_text(encoded_content):
    parsed_html = BeautifulSoup(encoded_content, features="html.parser")
    return parsed_html.get_text()



def extract_techenclave_data():
    dict_data = xmltodict.parse(requests.get(os.getenv("TECHENCLAVE_URL")).content)

    techenclave_data = []

    for item in dict_data["rss"]["channel"]["item"]:
        techenclave_dict = {}
        techenclave_dict["title"] = item["title"]
        techenclave_dict["url"] = item["link"]
        techenclave_dict["posted_ago"] = calculate_time_difference(item["pubDate"])
        techenclave_dict["selftext"] = convert_encoded_content_to_text(item["content:encoded"])
        techenclave_data.append(techenclave_dict)

    return techenclave_data


if __name__ == "__main__":
    data = extract_techenclave_data()
    data = data[0]
   