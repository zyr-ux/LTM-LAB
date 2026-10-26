from numpy import inner
import pandas as pd


def load_student_enquiries(file_path):
    df = pd.read_csv(file_path)

    return df[:'enquiry_date']

def clean_enquiry_data(df):
    df_cleaned = df.dropna(subset=['email'])
    df_cleaned.drop_duplictes(subset=['enquiry_id'])

def merge_with_courses(enquiries_df, ref_file_path):
    merged_df = pd.merge(enquiries_df,pd.read_csv(ref_file_path), on='course_id', how='inner')
