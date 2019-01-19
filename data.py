import sample as yelp
import pandas as pd
from key import API_KEY


limit = 50 # max 50 per request
num_requests = 20 # (to get 20*50 = 1000)

for i in range(num_requests):

    df = pd.DataFrame(yelp.search(API_KEY, "", 'toronto', lim=limit, offset=i*limit)['businesses'],
                      columns=['id', 'alias', 'rating', 'review_count', 'categories'],
                      )

    # print(df['review_count'].quantile(0.1))
    # print(df['review_count'].quantile(0.2))
    print(df[['alias', 'rating', 'review_count']])

# print(yelp.search(API_KEY, "", 'toronto', lim=50))






# for count in df['review_count']:
#     print(count)
