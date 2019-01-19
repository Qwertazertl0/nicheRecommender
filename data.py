import sample as yelp
import pandas as pd
from key import API_KEY


df = pd.DataFrame(yelp.search(API_KEY, "", 'chicago')['businesses'], columns=['id', 'alias', 'rating', 'review_count', 'categories'])
