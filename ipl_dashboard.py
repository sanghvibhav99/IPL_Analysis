import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import cv2
import streamlit as st


# Cleaning & Processing

temp = pd.read_csv('IPL Matches 2008-2020.csv')

m = pd.read_csv('/Users/bhavsanghvi/Engineering/Projects/IPL_Analysis/deliveries.csv')
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
teams = sorted(set(temp['team1']).union(set(temp['team2'])))
teams = [team for team in teams if team not in remove_teams]

# SELECTION SIDEBAR
team_tab, player_tab = st.tabs(["🏏 Team Analysis", "👤 Player Analysis"])

with team_tab:
    left, right = st.columns([5,2])

    with right:
        team = st.selectbox("Select Team",teams,key="team")

    with left:
        st.title(team)
        
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

with player_tab:
    players = sorted(set(m['batsman'].dropna()).union(set(m['bowler'].dropna())).union(set(m['fielder'].dropna())))

    # DATA OF CURRENT PLAYER
    left, right = st.columns([5,2])
    with right:
        player = st.selectbox("Select Player",players,key="player")
    with left:
        st.title(player)

    # BATTING INFO
    bat = m[m['batsman'] == player]
    run = bat['batsman_runs'].sum()
    ball = bat[bat['wide_runs'] == 0].shape[0]
    sr = round(run * 100 / ball,2) if ball else 0
    fours = bat[bat['batsman_runs'] == 4].shape[0]
    sixes = bat[bat['batsman_runs'] == 6].shape[0]
    outs = bat[bat['player_dismissed'] == player].shape[0]
    avg = round(run / outs,2) if outs else run

    # BOWLING INFO
    bowl = m[m['bowler'] == player]
    balls = bowl[(bowl['wide_runs'] == 0) & (bowl['noball_runs'] == 0)].shape[0]
    runs_conceded = (bowl['batsman_runs']+bowl['wide_runs']+bowl['noball_runs']).sum()
    wickets = bowl[(bowl['player_dismissed'].notna()) & (bowl['dismissal_kind'] != 'run out')].shape[0]
    overs = balls/6
    economy = round(runs_conceded / overs,2) if overs else 0
    bowl_avg = round(runs_conceded/wickets,2) if wickets else 0
    balls_wicket = round(balls/wickets,2) if wickets else 0
    dots = bowl[bowl['total_runs'] == 0].shape[0]


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

    # FIELDING INFO
    field = m[m['fielder'] == player]

    # TEAM INFO
    if not bat.empty:
        team = bat['batting_team'].mode().iloc[0]
    elif not bowl.empty:
        team = bowl['bowling_team'].mode().iloc[0]
    else:
        team = 'Unknown'
    st.markdown(f"<h4 style='color:white;'>{team}</h4>", unsafe_allow_html=True)

    # TOGGLE BETWEEN BATTING & BOWLING
    mode = st.segmented_control("Mode",["Batting", "Bowling"],default="Batting")

    # BATTING STATISTICS
    if mode == 'Batting':
        if bat.empty:
            st.info("No batting data available for this player.")
            st.stop()
        # DISPLAY VALUES
        a,b,c,d,e = st.columns(5)
        a.metric('Runs : ' , run)
        b.metric('Average : ' , avg)
        c.metric('Strike Rate : ' , sr)
        d.metric('Fours : ' , fours)
        e.metric('Sixes : ' , sixes)

        powerplay = bat[bat['over'] <= 6]
        middle = bat[(bat['over'] >= 7) & (bat['over'] <= 15)]
        death = bat[bat['over'] >= 16]

        # DIVISION INTO PHASES - (POWERPLAY, MIDDLE, DEATH)
        phase = st.segmented_control("Phase",["Powerplay", "Middle", "Death"],default="Powerplay")

        if (phase == 'Powerplay'):
            df = powerplay
        elif (phase == 'Middle'):
            df = middle
        else:
            df = death

        # RUNS & STRIKE RATE FOR PHASE
        phase_runs = df['batsman_runs'].sum()
        phase_ball = df[df['wide_runs'] == 0].shape[0]
        phase_sr = round(phase_runs * 100 / phase_ball,2) if phase_ball else 0

        # DISPLAY VALUES
        c1,c2 = st.columns(2)
        c1.metric('Runs : ' , phase_runs)
        c2.metric('Strike Rate : ' , phase_sr)

        # GRAPHICAL PART FOR PHASE BATTING
        runs_match = df.groupby('match_id')['batsman_runs'].sum()
        balls_match = df[df['wide_runs'] == 0].groupby('match_id').size()

        graph = pd.concat([runs_match,balls_match],axis = 1)
        graph.columns = ['runs' , 'balls']
        graph = graph.fillna(0)
        graph['sr'] = round(graph['runs'] * 100 / graph['balls'],2).fillna(0)
        graph = graph.reset_index(drop=True)
        graph.index = graph.index + 1
        graph["runs_avg"] = graph["runs"].rolling(5,min_periods=1).mean()
        graph["sr_avg"] = graph["sr"].rolling(5,min_periods=1).mean()

        g1,g2 = st.columns(2)

        # RUNS GRAPH
        with g1:
            fig , ax = plt.subplots(figsize=(5,3))
            fig.patch.set_alpha(0)
            ax.set_facecolor('none')

            ax.plot(graph.index , graph['runs_avg'] , linewidth = 2)
            ax.set_title(f'{phase} Runs per Match' , color = 'white')
            ax.set_xlabel('Match', color='white')
            ax.set_ylabel('Runs' , color = 'white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.grid(True,alpha=0.3)
            ax.tick_params(axis = 'both',color = 'white')
            st.pyplot(fig,transparent = True)

        # STRIKE RATE GRAPH
        with g2:
            fig , ax = plt.subplots(figsize=(5,3))
            fig.patch.set_alpha(0)
            ax.set_facecolor('none')

            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.plot(graph.index , graph['sr_avg'] , linewidth = 2)
            ax.set_title(f'{phase} Strike Rate per Match' , color = 'white')
            ax.set_xlabel('Match', color='white')
            ax.set_ylabel('Strike Rate' , color = 'white')
            ax.grid(True,alpha=0.3)
            
            ax.tick_params(axis = 'both',color = 'white')
            st.pyplot(fig,transparent = True)
    
    # BOWLING STATISTICS
    elif mode == 'Bowling':
        if bowl.empty:
            st.info("This player has no bowling data.")
            st.stop()
        
        # DISPLAY VALUES
        a1,b1,c1,d1,e1,f1 = st.columns(6)
        a1.metric('Wickets : ' , wickets)
        b1.metric('Overs : ' , round(overs,1))
        c1.metric('Balls per Wicket : ' , balls_wicket)
        d1.metric('Average : ' , bowl_avg)
        e1.metric('Economy : ' , economy)
        f1.metric('Dot Balls : ' , dots)

        powerplay = bowl[bowl['over'] <= 6]
        middle = bowl[(bowl['over'] >= 7) & (bowl['over'] <= 15)]
        death = bowl[bowl['over'] >= 16]

        # DIVISION INTO PHASES - (POWERPLAY, MIDDLE, DEATH)
        phase = st.segmented_control('Phase',["Powerplay", "Middle", "Death"],default="Powerplay")

        if phase == 'Powerplay':
            df = powerplay
        elif phase == 'Middle':
            df = middle
        else:
            df = death

        phase_wickets = df[(df['player_dismissed'].notna()) & (df['dismissal_kind'] != 'run out')].shape[0]
        phase_runs_conceded = (df['batsman_runs']+df['wide_runs']+df['noball_runs']).sum()
        phase_balls = df[(df['wide_runs'] == 0) & (df['noball_runs'] == 0)].shape[0]
        phase_overs = phase_balls/6
        phase_economy = round(phase_runs_conceded/phase_overs,2) if phase_overs else 0
        phase_dots = df[(df['batsman_runs'] == 0) & (df['noball_runs'] == 0) & (df['wide_runs'] == 0)].shape[0]
        phase_dot_pct = round(phase_dots * 100 / phase_balls,2) if phase_balls else 0

        # DISPLAY VALUES
        d1,d2,d3,d4 = st.columns(4)

        d1.metric("Runs Conceded", phase_runs_conceded)
        d2.metric("Economy", phase_economy)
        d3.metric("Overs", round(phase_overs,1))
        d4.metric("Dot Ball %", f"{phase_dot_pct}%")

        # GRAPHICAL PART FOR PHASE BOWLING
        runs_match = (df.groupby('match_id').apply(lambda x : (x['batsman_runs'] + x['wide_runs'] + x['noball_runs']).sum()))
        balls_match = (df[(df['noball_runs'] == 0) & (df['wide_runs'] == 0)].groupby('match_id').size())
        wickets_match = (df[(df['player_dismissed'].notna()) & (df['dismissal_kind'] != 'run out')].groupby('match_id').size())

        graph = pd.concat([runs_match,balls_match,wickets_match],axis=1)
        graph.columns = ['runs','balls','wickets']
        graph = graph.fillna(0)
        graph = graph.reset_index(drop=True)
        graph.index = graph.index + 1
        graph['economy'] = np.where(graph['balls'] > 0,graph['runs']/(graph['balls']/6),0)
        graph['avg'] = np.where(graph['wickets']>0,graph['runs']/graph['wickets'],np.nan)
        graph['avg_avg'] = graph['avg'].rolling(5,min_periods=1).mean()
        graph['economy_avg'] = graph['economy'].rolling(5,min_periods=1).mean()

        g1,g2 = st.columns(2)

        # ECONOMY GRAPH
        with g1:
            fig , ax = plt.subplots(figsize=(5,3))
            fig.patch.set_alpha(0)
            ax.set_facecolor('none')
        
            line, = ax.plot(graph.index , graph['economy_avg'] , linewidth = 2)
            mask = graph['economy_avg'].isna()
            start = (~mask & mask.shift(1, fill_value=True))
            end = (~mask & mask.shift(-1,fill_value=True))
            ax.scatter(graph.index[start],graph['economy_avg'][start],s=20,color=line.get_color())
            ax.scatter(graph.index[end],graph['economy_avg'][end],s=20,color=line.get_color())
            ax.set_title(f'{phase} Overs Economy (Rolling) ' , color = 'white')
            ax.set_xlabel('Match', color='white')
            ax.set_ylabel('Economy' , color = 'white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.grid(True,alpha=0.3)
            ax.tick_params(axis = 'both',color = 'white')
            st.pyplot(fig,transparent = True)

        # Average GRAPH
        with g2:
            fig , ax = plt.subplots(figsize=(5,3))
            fig.patch.set_alpha(0)
            ax.set_facecolor('none')
                    
            line, = ax.plot(graph.index , graph['avg_avg'] , linewidth = 2)
            mask = graph['avg_avg'].isna()
            start = (~mask & mask.shift(1, fill_value=True))
            end = (~mask & mask.shift(-1,fill_value=True))
            ax.scatter(graph.index[start],graph['avg_avg'][start],s=20,color=line.get_color())
            ax.scatter(graph.index[end],graph['avg_avg'][end],s=20,color=line.get_color())
            ax.set_title(f'{phase} Overs Average (Rolling)' , color = 'white')
            ax.set_xlabel('Match', color='white')
            ax.set_ylabel('Average' , color = 'white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.grid(True,alpha=0.3)
            ax.tick_params(axis = 'both',color = 'white')
            st.pyplot(fig,transparent = True)
            
