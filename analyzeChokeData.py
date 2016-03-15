import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


choke_df = pd.read_csv("chokeDataframe.csv", index_col=0)

choke_df["HomeWin"] = (choke_df["HomeWinMargin"] > 0).astype(int)
choke_df["RoadWin"] = (choke_df["HomeWinMargin"] < 0).astype(int)

numbers_list = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
			    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]

# counts games choked at certain leads
for i in range(0, 21):
	choke_df["{}+ Pt HBlow".format(i)] = ((choke_df["HomeMax4thLead"] >= i) & (choke_df["HomeWinMargin"] < 0)).astype(int)
	choke_df["{}+ Pt RBlow".format(i)] = ((choke_df["RoadMax4thLead"] >= i) & (choke_df["HomeWinMargin"] > 0)).astype(int)
for i in range(0, 21):
	choke_df["HWin at {} margin".format(i)] = ((choke_df["HomeMax4thLead"] <= i) & (choke_df["HomeWin"] == 1)).astype(int)
	choke_df["RWin at {} margin".format(i)] = ((choke_df["RoadMax4thLead"] <= i) & (choke_df["RoadWin"] == 1)).astype(int)


blown_count_df = choke_df["HomeTeam"].value_counts().add(choke_df["AwayTeam"].value_counts())  # games played
wins = (choke_df.groupby("HomeTeam", as_index = True)["HomeWin"].sum().add(choke_df.groupby("AwayTeam", as_index = True)["RoadWin"].sum(), fill_value = 0))
losses = (choke_df.groupby("AwayTeam", as_index = True)["HomeWin"].sum().add(choke_df.groupby("HomeTeam", as_index = True)["RoadWin"].sum(), fill_value = 0))
blown_count_df = pd.concat([blown_count_df, wins, losses], axis = 1)

print choke_df.head()

for i in range(0, 21):
	wins_at_margin = (choke_df.groupby("HomeTeam", as_index = True)["HWin at {} margin".format(i)].sum().add(choke_df.groupby("AwayTeam", as_index = True)["RWin at {} margin".format(i)].sum(), fill_value = 0))
	losses_at_margin = (choke_df.groupby("HomeTeam", as_index = True)["{}+ Pt HBlow".format(i)].sum().add(choke_df.groupby("AwayTeam", as_index = True)["{}+ Pt RBlow".format(i)].sum(), fill_value = 0))
	percent_at_margin = wins_at_margin.divide(wins_at_margin.add(losses_at_margin, fill_value = 0)).round(3)
	blown_count_df = pd.concat([blown_count_df, percent_at_margin], axis = 1)
	           
blown_count_df.columns = ["games", "wins", "losses", "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
		    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"] 

y_axis = blown_count_df.loc[u'ORL',:][8:24]
y_axis2 = blown_count_df.loc[u'NY',:][8:24]
y_axis3 = blown_count_df.loc[u'LAL',:][8:24]

print blown_count_df.head()

# Plot for a couple of teams (haven't plotted yet for whole league agains't orlando)
x_axis = np.linspace(5,20,16)
fig, ax = plt.subplots()
ax.set_xlabel('largest 4th quarter lead')
ax.set_ylabel('win percentage')
ax.plot(x_axis, y_axis, label='Orlando')
ax.plot(x_axis, y_axis2, label='NY Knicks')
ax.plot(x_axis, y_axis3, label='Lakers')
plt.show()
# print choke_df

# count home and road blows for each team (at home and on road), and combine to one series for blown lead of each size
# eight_point_blows_per_hteam = choke_df.groupby("HomeTeam", as_index = True)["eight+ Pt HBlow"].sum()
# eight_point_blows_per_rteam = choke_df.groupby("AwayTeam", as_index = True)["eight+ Pt RBlow"].sum()
# eight_point_blows = eight_point_blows_per_hteam.add(eight_point_blows_per_rteam, fill_value = 0)
# print eight_point_blows

# ten_point_blows_per_hteam = choke_df.groupby("HomeTeam", as_index = True)["10+ Pt HBlow"].sum()
# ten_point_blows_per_rteam = choke_df.groupby("AwayTeam", as_index = True)["10+ Pt RBlow"].sum()
# ten_point_blows = ten_point_blows_per_hteam.add(ten_point_blows_per_rteam, fill_value = 0)
# print ten_point_blows.sum()

# fifteen_point_blows_per_hteam = choke_df.groupby("HomeTeam", as_index = True)["15+ Pt HBlow"].sum()
# fifteen_point_blows_per_rteam = choke_df.groupby("AwayTeam", as_index = True)["15+ Pt RBlow"].sum()
# fifteen_point_blows = fifteen_point_blows_per_hteam.add(fifteen_point_blows_per_rteam, fill_value = 0)
# print fifteen_point_blows.sum()

# # combine into one dataframe, check for interesting trend? Small sample size... 
# blown_count_df = pd.concat([eight_point_blows, ten_point_blows, fifteen_point_blows], axis = 1)
# blown_count_df.columns = ["8+ Pt Blow", "10+ Pt Blow", "15+ Pt Blow"]

# print blown_count_df

# (1) Orlando's only blown 4 games where they've had an 8+ point lead, which is 4 out of the 68 such games all season where a 
# team blew an 8+ point lead, which isn't many.
# (2) All 4 of Orlando's 8+ point blown leads were also 10+ point blown leads, so they've got 4 of the 35 10+ blown leads 
# all season. That's not very good.
# (3) They've got 2 of the 7 15+ blown leads this season, also not great.


