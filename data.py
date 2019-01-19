import sample as yelp
import pandas as pd
from key import API_KEY


limit = 50 # max 50 per request
num_requests = 20
# num_requests = 20 # (to get 20*50 = 1000)
location = 'toronto'

dataframes = []


for i in range(num_requests):

    df = pd.DataFrame(yelp.search(API_KEY, "", location, lim=limit, offset=i*limit)['businesses'],
                      columns=['id', 'alias', 'rating', 'review_count', 'categories'],
                      )

    dataframes.append(df)

    # print(df['review_count'].quantile(0))
    # print(df['review_count'].quantile(0.1))
    # print(df['review_count'].quantile(0.2))

    # print(df[['alias', 'rating', 'review_count']])

# print(yelp.search(API_KEY, "", 'toronto', lim=50))


combined_df = pd.concat(dataframes)
quantile1 = combined_df['review_count'].quantile(0)
quantile2 = combined_df['review_count'].quantile(0.1)


out = []

for index, row in combined_df.iterrows():
    if quantile1 < row['review_count'] < quantile2:
        out.append([row['alias'], row['rating'], row['review_count']])

    # TODO FILTER OUT LANDMARKS, only restaurants
    # TODO actual sort by rating
    # TODO more precise location (Toronto is big!)

    # print(row['alias'], row['rating'])

print(out)

# for alias in combined_df['alias']:



# for count in df['review_count']:
#     print(count)
