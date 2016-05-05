# import pandas as pd
from timeit import default_timer as timer

import psycopg2
dbname = "test1"
con = psycopg2.connect("dbname=%s" % dbname)

from jutge import *
from jutgeAnalyser import *

import matplotlib.pyplot as plt
plt.style.use('ggplot')


u = select_users(con, course_id="C00198")
p = select_pbls(con, course_id="C00198", )

# m, v, h = process(u[:4], p[:4], src="csv/means.csv", verbose=True)
m_m, diff_m, abil_m = process(u, p, src="csv/means.csv", verbose=True,
                              vert_name="diff_m", hor_name="abil_m")
m_b, diff_b, abil_b = process(u, p, src="csv/bin.csv", verbose=True,
                              vert_name="diff_b", hor_name="abil_b")

# ax = s.hist()  # s is an instance of Series
Abilities = pd.DataFrame([abil_m, abil_b]).T
Abilities.sort_values(by='abil_m', inplace=True)




# Create a figure of given size
fig = plt.figure(figsize=(16,12))
# Add a subplot
ax = fig.add_subplot(111)
# Set title
ttl = 'Population, size and age expectancy in the European Union'


# ax = Abilities.plot(title="Abilities order comparison for C00198")  # .hist(subplots=True, stacked=True,bins=20)
# Abilities.plot(title="Abilities order comparison for C00198")  # .hist(subplots=True, stacked=True,bins=20)
Abilities.plot.hist(stacked=True,bins=20, subplots=True, title=ttl, ax=ax)
 
# Set color transparency (0: transparent; 1: solid)
a = 0.7

# Customize title, set position, allow space on top of plot for title
ax.set_title(ax.get_title(), fontsize=26, alpha=a, ha='left')
# plt.subplots_adjust(top=0.9)
ax.title.set_position((0,1.08))

# fig = ax.get_figure()
# fig.savefig('figure.pdf')
# Save figure in png with tight bounding box
# plt.savefig('figure.pdf', bbox_inches='tight', dpi=300)
fig.savefig('figure.pdf', bbox_inches='tight', dpi=300)