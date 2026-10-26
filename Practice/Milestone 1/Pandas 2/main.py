import pandas as pd


def load_service_requests(file_path):
    df = pd.read_csv(file_path)
    return df.loc[:,:'discount_pct']

def clean_service_requests(df):
    df = df.dropna(subset=['email'])
    df = df.drop_duplicates(subset=['request_id'])
    return df

def merge_with_services(requests_df, ref_file_path):
    catalogue_df = pd.read_csv(ref_file_path)

    merged_df = pd.merge(requests_df,catalogue_df,on='service_id',how='inner')
    merged_df.drop(columns=['service_id'])

    return merged_df

def add_net_quoted_fee(df):

    df['net_quoted_fee'] = (df['quoted_fee'] * (1-df['discount_pct']/100)).round(2)

    return df

def aggregate_by_service(df):
    aggregate_df = df.groupby('service_name').agg(avg_net_quoted_fee = ('net_quoted_fee','mean'),
                                                request_count = ('request_id','count')).reset_index()

    return aggregate_df

def finalize_summary(df):
    df['avg_net_quoted_fee'] = df['avg_net_quoted_fee'].round(2)

    fianl_df = df[['service_name','avg_net_quoted_fee','request_count']].sort_values('service_name',ascending=True).reset_index(drop=True)
    return fianl_df


if __name__ == '__main__':
    requests_df = load_service_requests('data/service_requests.csv')
    cleaned_requests_df = clean_service_requests(requests_df)
    merged_df = merge_with_services(cleaned_requests_df,'data/service_catalogue.csv')
    merged_df = add_net_quoted_fee(merged_df)
    agg_df = aggregate_by_service(merged_df)
    fianl_df = finalize_summary(agg_df)

    print(fianl_df)


