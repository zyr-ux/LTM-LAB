import pandas as pd

def load_student_enquiries(file_path):
    df = pd.read_csv(file_path)

    return df.loc[:,:'enquiry_date']

def clean_enquiry_data(df):
    df_cleaned = df.dropna(subset=['email'])
    df_cleaned.drop_duplicates(subset=['enquiry_id'])

    return df

def merge_with_courses(enquiries_df, ref_file_path):
    courses_df = pd.read_csv(ref_file_path)
    merged_df = pd.merge(enquiries_df,courses_df, on='course_id', how='inner')
    merged_df = merged_df.drop(columns=['course_id'])
    return merged_df

def add_net_quoted_fee(df):
    # return df.loc[round(df['quoted_fee']*(1-df['discount_pct']/100),2)]

    df['net_quoted_fee'] = (df['quoted_fee'] * (1-df['discount_pct']/100)).round(2)

    return df

def aggregate_by_course(df):
    return df.groupby('course_name').agg(avg_net_quoted_fee = ('net_quoted_fee','mean'),
                                        enquiry_count = ('enquiry_id','count')).reset_index()

def finalize_summary(df):
    result = df[['course_name','avg_net_quoted_fee','enquiry_count']]

    result['avg_net_quoted_fee'] = result['avg_net_quoted_fee'].round(2)

    result = result.sort_values('course_name',ascending=True)

    result = result.reset_index(drop=True) # drop = True may not be needed

    return result
    

if __name__ == "__main__":
    df = load_student_enquiries('data/training_enquiries.csv')
    clean_enquires_df = clean_enquiry_data(df)
    merged_df = merge_with_courses(clean_enquires_df,'data/training_courses.csv')
    merged_df = add_net_quoted_fee(merged_df)
    merged_df = aggregate_by_course(merged_df)
    merged_df = finalize_summary(merged_df)

    print(merged_df)
