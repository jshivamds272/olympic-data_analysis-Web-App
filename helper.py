#import library
import pandas as pd
import numpy as np

#import datasets
df = pd.read_csv(r'C:\Users\Shivam Joshi\PycharmProjects\olympic_data_web_app\athlete_events1.zip.zip\athlete_events1.csv.csv')
region_df = pd.read_csv(r'C:\Users\Shivam Joshi\PycharmProjects\olympic_data_web_app\noc_regions.csv')


def medal_tally(df):  # made function of medal tally according to there resion and medals
    medal_taly = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_taly = medal_taly.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold', ascending= False).reset_index()
    medal_taly['total'] = medal_taly['Gold'] + medal_taly['Silver'] +medal_taly['Bronze']
    medal_taly['Gold'] = medal_taly['Gold'].astype('int')
    medal_taly['Silver'] = medal_taly['Silver'].astype('int')
    medal_taly['Bronze'] = medal_taly['Bronze'].astype('int')
    medal_taly['total'] = medal_taly['total'].astype('int')
    return medal_taly

def country_year_list(df): #return years and country list
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def fetch_medal_tally(df,year, country):  #country and year wise medal tally
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby("Year").sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False)
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

def participating_nations_over_time(df):  #participating nations year wise
    nation_over_time= df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('index')
    nation_over_time.rename(columns={'index': 'Edition', 'Year': 'No. of countries'}, inplace=True)
    return nation_over_time

def events_over_time(df,col):  # events year wise
    events_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('index')
    events_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return events_over_time

def athelete_over_time(df,col):  # athelete over time
    athelete_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('index')
    athelete_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return athelete_over_time


def most_successful(df, sport): #succesful athelete for particular sport
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index().merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    return x

def yearwise_medal_tally(df,country):  #year wise country medal tally
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country): # events country wise heatmap
    temp_df = df.dropna(subset=['Medal'])  # we have to remove those lines which have nan medal
    temp_df.drop_duplicates(subset=['Team', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_cont(df,country):   #most successful countries
    temp_df=df.dropna(subset=['Medal'])
    temp_df=temp_df[temp_df['Sport']==country]
    x = temp_df['Name'].value_counts().reset_index().merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index').head(10)
    x.rename(columns={'Index':'Name','Name_x':'Medals'},inplace=True)
    return x

def weight_vs_height(df,sport):  #weight and height for particular sport
    athlete_df=df.drop_duplicates(subset = ['Name','region'])
    athlete_df['Medal'].fillna('No Medal', inplcae=True)
    if sport!='Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):  #men vs women participation
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace = True)
    final.fillna(0, inplace=True)

    return final
