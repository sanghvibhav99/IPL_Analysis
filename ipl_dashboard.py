import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import cv2
import streamlit as st


# Cleaning & Processing
temp = pd.read_csv('/Users/bhavsanghvi/Engineering/Projects/IPL_Analysis/IPL Matches 2008-2020.csv')
temp['date'] = pd.to_datetime(temp['date'])
temp['year'] = temp['date'].dt.year
temp['month'] = temp['date'].dt.month
temp['day'] = temp['date'].dt.day

temp['team1'] = temp['team1'].replace({'Pune Warriors' : 'Rising Pune Supergiants','Rising Pune Supergiant':'Rising Pune Supergiants','Delhi Daredevils' : 'Delhi Capitals'})
temp['team2'] = temp['team2'].replace({'Pune Warriors' : 'Rising Pune Supergiants','Rising Pune Supergiant':'Rising Pune Supergiants','Delhi Daredevils' : 'Delhi Capitals'})
temp['winner'] = temp['winner'].replace({'Pune Warriors' : 'Rising Pune Supergiants','Rising Pune Supergiant':'Rising Pune Supergiants','Delhi Daredevils' : 'Delhi Capitals'})
remove_teams = ['Gujarat Lions' , 'Kochi Tuskers Kerala']

# Dashboard
st.set_page_config(page_title='IPL Analysis',layout='wide')
st.title('IPL Dashboard')

# MAIN DATAFRAME
teams = sorted(
    set(temp['team1']).union(set(temp['team2']))
)
teams = [team for team in teams if team not in remove_teams]

# SELECTION SIDEBAR
team = st.sidebar.selectbox(
    "Select Team",
    teams
)

# GENERIC INFORMATION
team_df = temp[(temp['team1'] == team) |(temp['team2'] == team)]
matches = team_df.shape[0]
wins = team_df[team_df['winner'] == team].shape[0]
losses = matches - wins
if matches > 0:
    win_pct = round(wins * 100 / matches, 2)
else:
    win_pct = 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Matches : " , matches)
c2.metric("Wins/Matches : " , wins)
c3.metric("Losses : " , losses)
c4.metric("Win Percentage : " , f"{win_pct}%")

# DIVIDER
st.divider()
left,middle,right = st.columns([2,4,1])

# LEFT DIVISION (1/3)
# TOSS DECISION - GRAPH
with left:
    st.subheader('Toss Decision')
    t = team_df[team_df['toss_winner'] == team].groupby('toss_decision')['toss_decision'].count()
    fig , ax = plt.subplots(figsize=(4,4))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    colors = ['#00ADB5', '#393E46']
    ax.pie(t.values,labels=t.index,autopct='%1.1f%%',wedgeprops={'edgecolor' : 'black'},colors=colors,textprops={'color' : 'white'})
    st.pyplot(fig,transparent=True)

# MIDDLE DIVISION (2/3)
# WIN MARGIN - GRAPH
with middle:
    st.subheader('Win Margin')
    t = team_df[team_df['winner'] == team].groupby('year')['result_margin'].mean()
    fig , ax = plt.subplots(figsize=(4,3))

    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.plot(t.index,t.values,marker='o',linewidth=2)
    ax.set_xlabel('Year',color='white')
    ax.set_ylabel('Avg. Win Margin',color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white') 
    ax.grid(alpha=0.3)
    st.pyplot(fig,transparent=True)

# RIGHT DIVISION (3/3)
with right:
    toss_p = round(team_df[team_df['toss_winner']==team]['toss_winner'].count() * 100 / matches,2)
    bf = team_df[((team_df['toss_winner'] == team) & (team_df['toss_decision'] == 'bat')) | (((team_df['team1'] == team) | (team_df['team2'] == team)) & (team_df['toss_winner'] != team) & (team_df['toss_decision'] == 'field'))]['toss_decision'].count()
    bf_win = team_df[(((team_df['toss_winner'] == team) & (team_df['toss_decision'] == 'bat')) | (((team_df['team1'] == team) | (team_df['team2'] == team)) & ((team_df['toss_winner'] != team) & (team_df['toss_decision'] == 'field')))) & (team_df['winner'] == team)]['toss_decision'].count()
    bf1 = team_df[((team_df['toss_winner'] == team) & (team_df['toss_decision'] == 'field')) | (((team_df['team1'] == team) | (team_df['team2'] == team)) & (team_df['toss_winner'] != team) & (team_df['toss_decision'] == 'bat'))]['toss_decision'].count()
    bf1_win = team_df[(((team_df['toss_winner'] == team) & (team_df['toss_decision'] == 'field')) | (((team_df['team1'] == team) | (team_df['team2'] == team)) & ((team_df['toss_winner'] != team) & (team_df['toss_decision'] == 'bat')))) & (team_df['winner'] == team)]['toss_decision'].count()
    sp = team_df[(team_df['team1'] == team) | (team_df['team2'] == team)]['year'].nunique()
    bat_pct = round(bf_win*100/bf,2) if bf else 0
    field_pct = round(bf1_win*100/bf1,2) if bf1 else 0
    st.write("")
    st.write("")
    st.metric("Toss Winning % :", f"{toss_p} %")
    st.metric("Win % when Bat first : " , f"{bat_pct}%")
    st.metric("Win % when Field first : " , f"{field_pct}%")
    st.metric("Seasons Played : " , f"{sp}")



# Divider
st.divider()

# WIN 5 PER SEASON - GRAPH
t = team_df[team_df['winner'] == team].groupby('year')['year'].count() * 100 / team_df[(team_df['team1'] == team) | (team_df['team2'] == team)].groupby('year')['year'].count()
fig , ax = plt.subplots(figsize=(6,4))
ax.bar(t.index,t.values)
ax.set_xlabel('Year',color='white')
ax.set_ylabel('Wins',color='white')
ax.set_title('Win % per Season',color='white',fontsize=14)
ax.tick_params(axis='x', colors='white',labelsize=8)
ax.tick_params(axis='y', colors='white',labelsize=8) 
fig.patch.set_alpha(0)
ax.set_facecolor("none")
st.pyplot(fig,transparent=True)