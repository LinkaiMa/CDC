import numpy as np
import matplotlib.pyplot as plt
import json

p1_more_adv = json.load(open("p1-b2vsp2-b1.json", "r"))
p2_more_adv = json.load(open("p1-b1vsp2-b2.json", "r"))

# plot number of wins for adv player
adv_win = p1_more_adv["P1_win_count"] + p2_more_adv["P2_win_count"]
adv_potential_win = p1_more_adv["P1_better_count"] + p2_more_adv["P2_better_count"]

# plot number of wins for non-adv player
non_adv_win = p1_more_adv["P2_win_count"] + p2_more_adv["P1_win_count"]
non_adv_potential_win = p1_more_adv["P2_better_count"] + p2_more_adv["P1_better_count"]

# plot them in a bar chart
labels = ["Baseline 2", "Baseline 1"]
adv = [adv_win, non_adv_win]
# non_adv = [non_adv_win, adv_win]
adv_potential = [adv_potential_win, non_adv_potential_win]
# non_adv_potential = [non_adv_potential_win, adv_potential_win]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, (ax1, ax2) = plt.subplots(1, 2)
rects1 = ax1.bar(x, adv, width, label='Wins', color='tab:orange')
# rects2 = ax1.bar(x + width/2, non_adv, width, label='Losses')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax1.set_ylabel('Number of games')
ax1.set_title('Wins')
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.legend()

rects3 = ax2.bar(x, adv_potential, width, label='Wins')
# rects4 = ax2.bar(x + width/2, non_adv_potential, width, label='Losses')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax2.set_ylabel('Number of games')
ax2.set_title('Potential wins')
ax2.set_xticks(x)
ax2.set_xticklabels(labels)
ax2.legend()


fig.tight_layout()
plt.show()
