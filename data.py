import pandas as pd
import csv
import argparse
import json
import pprint
import requests
import sys
import urllib


from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

API_KEY = "_vUhPam91Q1xRIPuyjZakWzTH2VDwmYrxENgtWUQ9M85R4xkzv7th0yyIquj6P_MyEZDzH19p9nGF0NlLzjw_3gUGEiJr2QwgqGQDLoMt4QFlqxzIDh7QehvPr5CXHYx"

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def search(api_key, term, location, lim=10, offset=0, sort_by = "rating"):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
        lim (int): The number results to return

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': lim,
        'offset': offset,
        'sort_by': sort_by
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

def clean_yelp_string(name: str) -> str:
    # Clean up the name string
    name_split = list(map(str.title, name.split("-")))
    # for i in range(len(name_split)):
    last_index = len(name_split) - 1
    if name_split[last_index].isdigit():
        name_split[last_index] = ''  # Strip out the 2 or 3 that yelp adds

    name_proper = " ".join(name_split)

    return name_proper


def get_data(location="Toronto"):
    # Creates csv file with the desired data

    limit = 50 # max 50 per request
    num_requests = 20
    # num_requests = 20 # (to get 20*50 = 1000)

    dataframes = []

    for i in range(num_requests):

        # try:
        df = pd.DataFrame(search(API_KEY, "restaurants", location, lim=limit, offset=i*limit)['businesses'],
                          columns=['id', 'alias', 'rating', 'review_count', 'categories', 'coordinates'],
                          )
        # except:
        #     # Make the CSV file blank to show no results
        #     #open('results.csv', 'w').close()
        #     return "This is not working"

        dataframes.append(df)

        # print(df['review_count'].quantile(0))
        # print(df['review_count'].quantile(0.1))
        # print(df['review_count'].quantile(0.2))

        # print(df[['alias', 'rating', 'review_count']])

    # print(yelp.search(API_KEY, "", 'toronto', lim=50))

    combined_df = pd.concat(dataframes)

    start_quantile = 0
    quantile_interval = 0.2
    quantile_increment = 0.01
    min_review_threshold = 5
    # What this code does is start with the places with the bottom 10% of reviews
    # Then what it does is it says, if there are just few reviews in general
    # (ie consider Markham vs Toronto)
    # Then maybe we say there needs to be at least 5 reviews
    # And so adjust the quantile increment upwards
    quantile1 = combined_df['review_count'].quantile(start_quantile)
    while quantile1 < min_review_threshold:
        start_quantile += quantile_increment
        quantile1 = combined_df['review_count'].quantile(start_quantile)
        if start_quantile > 0.9: # ie there are just not enough reviews
            start_quantile = 0
            quantile_interval = 1
            # Get everything, if there just aren't enough results
            break

    quantile2 = combined_df['review_count'].quantile(start_quantile + quantile_interval)

    data = []

    for index, row in combined_df.iterrows():
        if quantile1 < row['review_count'] < quantile2:

            coord_d = row['coordinates']
            # latitude is first key and longitude is second key in this dict
            latitude = coord_d['latitude']
            longitude = coord_d['longitude']

            data.append([row['alias'], row['rating'], row['review_count'],
                        latitude, longitude])

        # Possible to do? More precise location (Toronto is big!)? But
        # somewhere like Markham isn't that big

        # print(row['alias'], row['rating'])

    data.sort(key= lambda x: -float(x[1])) # reverse order, highest rating first

    num_results = 20


    # print(out)

    with open('results.csv', 'w', newline='') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=',')

        for lst in data[:num_results]:

            out = []

            name = lst[0]  # Pick up only the name

            name_proper = clean_yelp_string(name)

            out.append(name_proper)
            out.extend(lst[1:])

            print(out)

            data_writer.writerow(out)


if __name__ == "__main__":
    pass
