import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

def simulate_data(n_influencers=20, n_posts=100, n_tracking=500, n_payouts=20):
    platforms = ['Instagram', 'YouTube', 'Twitter']
    categories = ['Fitness', 'Wellness', 'Lifestyle']
    products = ['Whey Protein', 'Multivitamin', 'Omega-3', 'Gainer']
    brands = ['MuscleBlaze', 'HKVitals', 'Gritzo']

    influencers = pd.DataFrame([{
        'influencer_id': i,
        'name': fake.name(),
        'category': random.choice(categories),
        'gender': random.choice(['Male', 'Female']),
        'followers': random.randint(1000, 500000),
        'platform': random.choice(platforms)
    } for i in range(n_influencers)])

    posts = pd.DataFrame([{
        'influencer_id': random.choice(influencers['influencer_id']),
        'platform': random.choice(platforms),
        'date': fake.date_this_year(),
        'url': fake.url(),
        'caption': fake.sentence(),
        'reach': random.randint(1000, 100000),
        'likes': random.randint(100, 10000),
        'comments': random.randint(0, 500)
    } for _ in range(n_posts)])

    tracking_data = pd.DataFrame([{
        'source': 'influencer',
        'campaign': random.choice(brands),
        'influencer_id': random.choice(influencers['influencer_id']),
        'user_id': fake.uuid4(),
        'product': random.choice(products),
        'date': fake.date_this_year(),
        'orders': random.randint(1, 5),
        'revenue': round(random.uniform(100, 2000), 2)
    } for _ in range(n_tracking)])

    payouts = pd.DataFrame([{
        'influencer_id': row['influencer_id'],
        'basis': random.choice(['post', 'order']),
        'rate': random.randint(500, 5000),
        'orders': tracking_data[tracking_data['influencer_id'] == row['influencer_id']]['orders'].sum(),
        'total_payout': 0  # to be calculated
    } for _, row in influencers.iterrows()])

    payouts['total_payout'] = payouts.apply(
        lambda x: x['rate'] * (1 if x['basis'] == 'post' else x['orders']), axis=1)

    return influencers, posts, tracking_data, payouts 