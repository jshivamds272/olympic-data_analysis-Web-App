#import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

import helper
import processing
#import datasets
df = pd.read_csv(r'C:\Users\Shivam Joshi\PycharmProjects\olympic_data_web_app\athlete_events1.zip.zip')
region_df = pd.read_csv(r'C:\Users\Shivam Joshi\PycharmProjects\olympic_data_web_app\noc_regions.csv')


df = processing.preprocess(df, region_df)
st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athelete wise Analysis')

)
#st.dataframe(df)
if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Selected Year',years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_country=='Overall' and selected_year=='Overall':
        st.title('Overall Tally')
    if selected_country=='Overall' and selected_year!='Overall':
        st.title('Medal Tally in '+str(selected_year)+'Olympics')
    if selected_country!='Overall' and selected_year=='Overall':
        st.title(selected_country + ' Overall performance')
    if selected_year!= 'Overall' and selected_country!='Overall':
        st.title(selected_country +' performance in '+str(selected_year))
    st.table(medal_tally)

if user_menu== 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities= df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events= df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3= st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nation_over_time=helper.participating_nations_over_time(df)
    fig=px.line(nation_over_time,x='Edition', y='No. of countries')
    st.title('Participating Nations Over The Years')
    st.plotly_chart(fig)

    events_over_time=helper.events_over_time(df,'Event')
    fig=px.line(events_over_time , x='Edition', y='Event')
    st.title('Events Over The Years')
    st.plotly_chart(fig)


    athelete_over_time=helper.events_over_time(df,'Name')
    fig=px.line(athelete_over_time , x='Edition', y='Name')
    st.title('Athelete Over The Years')
    st.plotly_chart(fig)

    st.title('No. of Events Over Time')
    fig,ax= plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)
    plt.show()

    st.title('Most Successful Athletes')
    sport_list= df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

if user_menu == 'Country Wise Analysis':
    st.sidebar.title('Country wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country ',country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(selected_country+'Medal Tally Over The Years')
    st.plotly_chart(fig)
    plt.show()
    st.title(selected_country+'excels in the following sport')
    pt=helper.country_event_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)
    plt.show()

    st.title('Top 10 Atheletes Of'+ selected_country)
    top10_df=helper.most_successful_cont(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athelete wise Analysis':
    athelete_df = df.drop_duplicates(subset=['Name','region'])
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()
    st.title('Medal winning Players Age Distribution')
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False , width =100, height=200)
    st.title('Distribution of Age')
    st.plotly_chart(fig)
    plt.show()

    # famous_sports = df['Sport'].unique().tolist()
    # x = []
    # name= []
    # #select_sport = st.selectbox('Please select Sport',famous_sports)
    # for sport in famous_sports:
    #     temp_df = athelete_df[athelete_df['Sport'] == sport]
    #     x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
    #     name.append(sport)
    # st.title('Gold winning Players Age Distribution of ', sport)
    # fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False, width=1000, height=600)
    # st.title('Distribution Of Age with respect to Sports')
    # st.plotly_chart(fig)
    # plt.show()

    sport_list = df['Sport'].unique().tolist()
    selected_sport= st.selectbox('Select Sport NAme', sport_list)
    temp_df= athelete_df[athelete_df['Sport']==selected_sport]
    fig,ax = plt.subplots()
    ax= sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style= temp_df['Sex'])
    st.title('Heights vs Weight')
    st.pyplot(fig)

    st.title('Men vs Women participation over the year')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year',y=['Male','Female'])
    st.plotly_chart(fig)
