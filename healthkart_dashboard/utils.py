def calculate_roas(tracking_df, payout_df):
    revenue_by_influencer = tracking_df.groupby('influencer_id')['revenue'].sum()
    payout_by_influencer = payout_df.set_index('influencer_id')['total_payout']
    roas = (revenue_by_influencer / payout_by_influencer).fillna(0)
    return roas.reset_index().rename(columns={0: 'roas'})

def get_top_influencers(tracking_df, influencers, top_n=5):
    revenue_by = tracking_df.groupby('influencer_id')['revenue'].sum().sort_values(ascending=False)
    return influencers[influencers['influencer_id'].isin(revenue_by.head(top_n).index)] 