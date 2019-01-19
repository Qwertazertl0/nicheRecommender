import sample as yelp
import pandas as pd
from key import API_KEY
import csv


def clean_yelp_string(name: str) -> str:
    # Clean up the name string
    name_split = list(map(str.title, name.split("-")))
    # for i in range(len(name_split)):
    last_index = len(name_split) - 1
    if name_split[last_index].isdigit():
        name_split[last_index] = ''  # Strip out the 2 or 3 that yelp adds

    name_proper = " ".join(name_split)

    return name_proper


def get_data(location: str) -> None:
    # Creates csv file with the desired data

    limit = 50 # max 50 per request
    num_requests = 20
    # num_requests = 20 # (to get 20*50 = 1000)

    dataframes = []

    for i in range(num_requests):

        try:
            df = pd.DataFrame(yelp.search(API_KEY, "restaurants", location, lim=limit, offset=i*limit)['businesses'],
                              columns=['id', 'alias', 'rating', 'review_count', 'categories', 'coordinates'],
                              )
        except:
            # Make the CSV file blank to show no results
            open('results.csv', 'w').close()
            return None

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
    location = input("Input location: ")
    get_data(location)
