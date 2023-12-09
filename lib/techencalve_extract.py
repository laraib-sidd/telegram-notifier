import os
from datetime import datetime as dt
import pytz
import xmltodict
import requests
from bs4 import BeautifulSoup
from utils import create_mongo_client, check_post_id_mongo, insert_mongo_collection


def calculate_time_difference(date_string):
    ist_dt = dt.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")
    ist_tz = pytz.timezone("Asia/Kolkata")
    now_dt = dt.now(ist_tz)
    total_seconds_passed = (now_dt - ist_dt).total_seconds()
    minutes_passed = total_seconds_passed / 60

    time_unit = "hours" if minutes_passed >= 60 else "minutes"
    formatted_time = f"{minutes_passed:.2f}" if time_unit == "minutes" else f"{minutes_passed / 60:.2f}"
    
    return f"{formatted_time} {time_unit} have passed. This post was created {ist_dt:%Y/%m/%d-%H:%M} hours"

def convert_encoded_content_to_text(encoded_content):
    parsed_html = BeautifulSoup(encoded_content, features="html.parser")
    return parsed_html.get_text()



def extract_techenclave_data():
    dict_data = xmltodict.parse(requests.get(os.getenv("TECHENCLAVE_URL")).content)
    mongo_client = create_mongo_client()
    mongo_collection = mongo_client['techencalve']
    techenclave_data = []

    for item in dict_data.get("rss", {}).get("channel", {}).get("item", []):
        id_exist = check_post_id_mongo(data['guid']['#text'], mongo_collection)
        if id_exist:
            continue
        else:  
            techenclave_dict = {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "posted_ago": calculate_time_difference(item.get("pubDate", "")),
                "selftext": convert_encoded_content_to_text(item.get("content:encoded", "")),
            }
            insert_mongo_collection(data['guid']['#text'],mongo_collection)
            techenclave_data.append(techenclave_dict)
    return techenclave_data


if __name__ == "__main__":
    data = extract_techenclave_data()
    data = data[0]
   