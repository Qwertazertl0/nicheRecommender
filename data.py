import sample as yelp
import pandas as pd
from key import API_KEY

limit = 50 # max 50 per request
num_requests = 20
# num_requests = 20 # (to get 20*50 = 1000)
location = 'markham'

dataframes = []

for i in range(num_requests):

    df = pd.DataFrame(yelp.search(API_KEY, "restaurants", location, lim=limit, offset=i*limit)['businesses'],
                      columns=['id', 'alias', 'rating', 'review_count', 'categories'],
                      )

    dataframes.append(df)

    # print(df['review_count'].quantile(0))
    # print(df['review_count'].quantile(0.1))
    # print(df['review_count'].quantile(0.2))

    # print(df[['alias', 'rating', 'review_count']])

# print(yelp.search(API_KEY, "", 'toronto', lim=50))

combined_df = pd.concat(dataframes)

start_quantile = 0
quantile_interval = 0.1
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

quantile2 = combined_df['review_count'].quantile(start_quantile + quantile_interval)

out = []

for index, row in combined_df.iterrows():
    if quantile1 < row['review_count'] < quantile2:
        out.append([row['alias'], row['rating'], row['review_count']])

    # Possible to do? More precise location (Toronto is big!)? But
    # somewhere like Markham isn't that big

    # print(row['alias'], row['rating'])

out.sort(key= lambda x: -float(x[1])) # reverse order, highest rating first

num_results = 10

print(out[:num_results])
