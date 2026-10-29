import pandas as pd


def load_ticket_sales(file_path):
    # TODO: Read the ticket sales CSV and return the required columns
    # in the specified order, excluding sale_date.
    df = pd.read_csv(file_path)
    return df.loc[:,:'discount_pct']
    raise NotImplementedError


def clean_ticket_sales(df):
    # TODO: Remove rows with missing buyer_email values and remove
    # duplicate sale_id records, retaining the earliest input row.
    dfc:pd.DataFrame = df.copy()
    dfc = dfc.dropna(subset=['buyer_email'])
    dfc = dfc.drop_duplicates(subset=['sale_id'],keep='first')
    return dfc
    raise NotImplementedError


def merge_with_events(df, ref_file_path):
    # TODO: Load the events reference CSV and inner join on event_id.
    # Keep all transaction columns and add event_name, category, and venue.
    dfc : pd.DataFrame = df.copy()
    events_df = pd.read_csv(ref_file_path)
    merged_df = pd.merge(dfc,events_df,on='event_id',how='inner')
    return merged_df
    raise NotImplementedError


def add_net_ticket_value(df):
    # TODO: Add net_ticket_value using tickets, ticket_price, and
    # discount_pct. Round each calculated value to two decimal places.
    dfc : pd.DataFrame = df.copy()
    dfc['net_ticket_value'] = (dfc['tickets'] * dfc['ticket_price'] * (1-dfc['discount_pct']/100)).round(2)
    return dfc
    raise NotImplementedError


def aggregate_by_category(df):
    # TODO: Group by category and calculate the average net ticket value,
    # total net ticket revenue, and valid sale count using the required names.
    dfc = df.copy()
    dfc = dfc.groupby('category').agg(avg_net_ticket_value = ('net_ticket_value','mean'),
                                                total_net_ticket_revenue = ('net_ticket_value','sum'),
                                                valid_sale_count = ('net_ticket_value','count')).reset_index()

    return dfc
    raise NotImplementedError


def finalize_summary(df):
    # TODO: Select the required output columns, round monetary columns to
    # two decimal places, sort by category, and reset the index.
    # Preserve the required schema when the DataFrame is empty.

    dfc : pd.DataFrame = df.copy()
    dfc = dfc[['category','avg_net_ticket_value','total_net_ticket_revenue','valid_sale_count']]
    dfc['avg_net_ticket_value'] = dfc['avg_net_ticket_value'].round(2)
    dfc['total_net_ticket_revenue'] = dfc['total_net_ticket_revenue'].round(2)
    dfc = dfc.sort_values('category').reset_index(drop=True)
    return dfc
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: Run functions 1–6 in order using the CSV files from data/
    # and print only the final summary DataFrame.
    loaded_df = load_ticket_sales('data/ticket_sales.csv')
    ticket_df = loaded_df.copy()
    cleaned_df = clean_ticket_sales(ticket_df)
    merged_df = merge_with_events(cleaned_df,'data/events.csv')
    add_net_tickets_df = add_net_ticket_value(merged_df)
    agg_df = aggregate_by_category(add_net_tickets_df)
    summary_df = finalize_summary(agg_df)
    print(summary_df)
    pass