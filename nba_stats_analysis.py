# -*- coding: utf-8 -*-
"""NBA-Stats-IC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/176d2VT6roYT69LPsj7ggfLJb0EAIEmQm
"""

# PYTHON MODULES
# import user-installed modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# pandas options
pd.set_option('display.max_rows', 100)

# use !wget -nc 'github path' to pull the nba stats data
#player logs
!wget "https://raw.githubusercontent.com/emilyyyyyleeeee/ITP487_NBAStats_lee/main/nba_game_log_2021_22.csv"
nba_player_log = pd.read_csv('nba_game_log_2021_22.csv')
# player salaries
!wget "https://raw.githubusercontent.com/emilyyyyyleeeee/ITP487_NBAStats_lee/main/nba_salary_2021_22.csv"
player_salaries = pd.read_csv('nba_salary_2021_22.csv')

# view columns and null counts for each column in the data frames
print(nba_player_log.columns)
print(nba_player_log.info())
print(player_salaries.columns)
print(player_salaries.info())

# shape of the data frames
# player game log:
print("NBA player log shape:")
print(nba_player_log.shape)
# player salaries
print("Player salary data shape:")
print(player_salaries.shape)

# show first five rows of each data frame
# nba player log
print(nba_player_log.head())
print("\n")
# player salaries
print(player_salaries.head())

# clean player logs
top_scorer_df = nba_player_log[['game_id', 'game_date','H_A', 'Team_Abbrev','Opponent_Abbrev','player', 'pts','minutes']]
print(top_scorer_df.head())

print("Player log data: ")
print("Shape before dropping duplicates and unneeded columns: ")
print(nba_player_log.shape)

top_scorer_df = top_scorer_df.drop_duplicates()

print("Shape after dropping duplicates and unneeded columns: ")
print(top_scorer_df.shape)

# clean player salary data
top_salary_df = player_salaries[['Player','2021/22']]
print(top_salary_df.head())

print("Player salary data: ")
print("Shape before dropping dupplicates and unneeded columns: ")
print(player_salaries.shape)

top_salary_df = top_salary_df.drop_duplicates()

print("Shape after dropping duplicates and unneeded columns: ")
print(top_salary_df.shape)

# show first five rows of each data frame
# nba player log
print(nba_player_log.head())
print("\n")
# player salaries
print(player_salaries.head())

# use pd.merge() to combine to two datasets, then clean the resulting data frame
player_stats_salaries = pd.merge(top_scorer_df,player_salaries,how='left',left_on='player',right_on='Player')

# shape of the data frames

# player game log:
print("NBA player log shape:")
print(nba_player_log.shape)
# player salaries
print("Player salary data shape:")
print(player_salaries.shape)

# drop null rows with null values
player_stats_salaries = player_stats_salaries.dropna(how='any')

# rename columns
player_stats_salaries = player_stats_salaries.rename(columns={"2021/22":"Salary", "H_A":"Home_Away"})
 # player_stats_salaries.rename(columns={"2021/22":"Salary", "H_A":"Home_Away"}, inplace=True)

player_season_stats = player_stats_salaries[['player', 'pts', 'minutes', 'Salary']]
player_season_stats = player_stats_salaries.groupby(by=['Player'], as_index=False).agg({'pts':'sum', 'minutes':'sum', 'Salary':'mean'})


player_season_stats['PPG/$'] = player_season_stats['pts']/player_season_stats['Salary']


player_season_stats = player_season_stats.sort_values(by=['PPG/$'], ascending=False)
print(player_season_stats.head())

# Histogram prep - need total points grouped by game_id
print(player_stats_salaries.head())
print('\n')
# store view in df named 'points_by_game_dist'
points_by_game_dist = player_stats_salaries.groupby(by=['game_id'], as_index=False).agg({'pts':'sum'})
print(points_by_game_dist.head())

# set title and axis labels
plt.title(label='')
plt.xlabel('')
plt.ylabel('')
# write code to create histogram here
plt.hist(points_by_game_dist['pts'], bins=30, color='blue', rwidth=0.9)

plt.show()

# bar chart/horizontal bar chart prep
team_salary_breakdown = player_stats_salaries.groupby(by=['Player', 'Team_Abbrev'], as_index=False).agg({'Salary':'mean'})

# total team salary breakdown
total_team_salary = team_salary_breakdown.groupby(by=['Team_Abbrev'], as_index=False).agg({'Salary':'sum'})
total_team_salary['Salary'] = total_team_salary['Salary'].apply(lambda x: x*.000001)
total_team_salary = total_team_salary.sort_values(by=['Salary'], ascending=False)

print(total_team_salary.head())

# Bar chart - break down of total salaries paid by team
fig, ax = plt.subplots(figsize=(14,8), dpi=100)

# set title, and axis labels
plt.title(label='')
plt.xlabel('')
plt.ylabel('')
plt.yticks

# write code to create bar chart here
plt.bar(total_team_salary['Team_Abbrev'], total_team_salary['Salary'], width=0.9)
plt.xticks(rotation=90)  # To rotate team abbreviations for better readability
plt.tight_layout()
plt.show()

# Horizontal bar chart
fig, ax = plt.subplots(figsize=(14,8), dpi=100)

# set title, and axis labels
plt.title('Total Payroll Costs by Team')
plt.ylabel('Teams')
plt.xlabel('Total Salaries Paid in 21-22 Season (in millions of $)')

# write code to create horizontal bar chart here
plt.barh(total_team_salary['Team_Abbrev'], total_team_salary['Salary'], height=0.9)
plt.tight_layout()
plt.show()

# Pie Chart prep
# player, team, salary breakdown
team_salary_breakdown = player_stats_salaries.groupby(by=['Player', 'Team_Abbrev'], as_index=False).agg({'Salary':'mean'})
print(team_salary_breakdown.head())
team_salary_breakdown = team_salary_breakdown[team_salary_breakdown['Team_Abbrev'] == 'LAL'].sort_values(by='Salary', ascending=False)
team_salary_breakdown['top_players'] = team_salary_breakdown['Player'].apply(lambda x:
                                                                             'Russell Westbrook' if x=='Russell Westbrook' else
                                                                         'LeBron James' if x=='LeBron James' else
                                                                             'Anthony Davis' if x== 'Anthony Davis' else
                                                                             'DeAndre Jordan' if x== 'DeAndre Jordan' else
                                                                             'Talen Horton-Tucker' if x== 'Talen Horton-Tucker' else
                                                                             'Rajon Rondo' if x== 'Rajon Rondo' else 'Other Players')
LAL_top_salaries = team_salary_breakdown.groupby(by=['top_players'], as_index=False).agg({'Salary':'sum'}).sort_values(by='Salary', ascending=False)
print(LAL_top_salaries)

# Pie Chart - Show  the Lakers players salary breakdown, who takes up the most of the salary budget?
fig, ax = plt.subplots(figsize=(14,8), dpi=100)

# set title
plt.title(label='')

# write code to create pie chart here
plt.pie(LAL_top_salaries['Salary'], labels=LAL_top_salaries['top_players'], autopct='%1.1f%%')

plt.show()
