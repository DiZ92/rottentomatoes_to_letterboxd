import requests
import json
import datetime
import csv


def time_extract(x):

    number = int(''.join(filter(str.isdigit, x)))
    if "day" in x:
        date_str = (datetime.datetime.now() - datetime.timedelta(days=number)).strftime("%Y-%m-%d")
    elif "month" in x:
        date_str = (datetime.datetime.now() - datetime.timedelta(weeks=4*number)).strftime("%Y-%m-%d")
    elif "year" in x:
        date_str = (datetime.datetime.now() - datetime.timedelta(weeks=4*12*number)).strftime("%Y-%m-%d")
    else:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    return date_str


debug = False

url = 'https://www.rottentomatoes.com/napi/userProfile/movieRatings/363836495'

still_go = True
json_payload = []
num = 0
cursor = ""

while still_go:
    response = requests.get(url, params={"endCursor": cursor})
    if response.status_code != 200:
        print('No Payload')
        still_go = False
    payload = response.text
    this_json = json.loads(payload)
    json_payload.append(this_json['ratings'])

    if not this_json['pageInfo']['hasNextPage']:
        still_go = False

    num += len(json_payload[0])
    print(str(num) + " reviews received")
    cursor = this_json['pageInfo']['endCursor']
    if debug:
        still_go = False

print("Parsing json")
all_payload = [item for sublist in json_payload for item in sublist]

titles = [x['item']['title'] for x in all_payload]
release_years = [x['item']['releaseYear'] for x in all_payload]
ages = [x['review']['age'] for x in all_payload]
dt_ages = [time_extract(x) for x in ages]
ratings = [x['review']['score'] for x in all_payload]

final_payloads = list(zip(titles, release_years, dt_ages, ratings))

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Year", "WatchedDate", "Rating"])
    writer.writerows(final_payloads)

print('Done')
