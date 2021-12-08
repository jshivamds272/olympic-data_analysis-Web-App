import pandas as pd   #import library

#import datasets
df = pd.read_csv(r'C:\Users\Shivam Joshi\PycharmProjects\olympic_data_web_app\athlete_events1.zip.zip\athlete_events1.csv.csv')
region_df = pd.read_csv(r'C:\Users\Shivam Joshi\PycharmProjects\olympic_data_web_app\noc_regions.csv')

def preprocess(df,region_df):  #did preprocessing step and we took only summer season olympics
    df = df[df['Season'] == 'Summer']
    df = df.merge(region_df, on='NOC' , how='left')  #merged on "NOC"
    df.drop_duplicates(inplace=True)     # removed duplicates rows
    df = pd.concat([df, pd.get_dummies(df['Medal'])],axis=1)  # concatinate df dataframe and one hot enocoding vector of medal
    return df

