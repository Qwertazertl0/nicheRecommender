import sample as yelp
import pandas as pd
from key import API_KEY

limit = 50 # max 50 per request
num_requests = 20 # (to get 20*50 = 1000)

df = pd.DataFrame(yelp.search(API_KEY, "", 'toronto', lim=limit, offset=0)['businesses'],
                      columns=['id', 'alias', 'rating', 'review_count', 'categories'],
                      )
for i in range(1, num_requests):
    new_df = pd.DataFrame(yelp.search(API_KEY, "", 'toronto', lim=limit, offset=i*limit)['businesses'],
                      columns=['id', 'alias', 'rating', 'review_count', 'categories'],
                      )
    df = df.append(new_df)
    print(new_df[['alias', 'rating', 'review_count', 'categories']])

df.to_csv(r'<insert location to store>', index=None)
