# import pandas as pd
from timeit import default_timer as timer

import psycopg2
dbname = "test1"
con = psycopg2.connect("dbname=%s" % dbname)

from jutge import *
from jutgeAnalyser import *

import matplotlib.pyplot as plt
print(plt.style.available)
plt.style.use('ggplot')

# u = select_users(con, course_id="C00198")
# p = select_pbls(con, course_id="C00198", )

# m, v, h = process(u[:4], p[:4], src="csv/means.csv", verbose=True)
# m_m, diff_m, abil_m = process(u, p, src="csv/means.csv", verbose=True,
#                               vert_name="diff_m", hor_name="abil_m")
# m_b, diff_b, abil_b = process(u, p, src="csv/bin.csv", verbose=True,
#                               vert_name="diff_b", hor_name="abil_b")

# ax = s.hist()  # s is an instance of Series
# Abilities = pd.DataFrame([abil_m, abil_b]).T
# Abilities.sort_values(by='abil_m', inplace=True)


# for sty in plt.style.available:
#     plt.style.use(sty)
#     ttl = 'Population, size and age expectancy in the European Union'
#     a = 0.7
#     axes = Abilities.plot.hist(stacked=True, bins=20, subplots=True,
# title=ttl, )  # ax=ax)
#     ax = axes[0]
#     ax.set_title("title 1", fontsize=14, alpha=a, ha='left')
#     axes[1].set_title("title 2", fontsize=14, alpha=a, ha='left')
#     fig = ax.get_figure()
#     fig.suptitle(ttl, fontsize=18, alpha=a)
# fig.savefig('figure.pdf', bbox_inches='tight', dpi=300)
#     fig.savefig('%s.png'%sty, bbox_inches='tight', dpi=300)
#     print '%s.png'%sty

def mkdir_p(mypath):
    '''Creates a directory. equivalent to using mkdir -p on the command line'''

    from errno import EEXIST
    from os import makedirs, path

    try:
        makedirs(mypath)
    except OSError as exc:  # Python >2.5
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else:
            raise


def hist_course(cid, crs):

    # cid = crs.course_id

    u = select_users(con, course_id=cid)
    p = select_pbls(con, course_id=cid)

    # print "%5d ; %5d" % (crs.usrcnt, len(u))
    # return
    if not u or not p:
        return

    # m, v, h = process(u[:4], p[:4], src="csv/means.csv", verbose=True)
    m_m, diff_m, abil_m = process(u, p, src="csv/means.csv", verbose=True,
                                  vert_name="diff_m", hor_name="abil_m")
    m_b, diff_b, abil_b = process(u, p, src="csv/bin.csv", verbose=True,
                                  vert_name="diff_b", hor_name="abil_b")


    # ax = s.hist()  # s is an instance of Series
    Abilities = pd.DataFrame([abil_m, abil_b]).T
    Difficulties = pd.DataFrame([diff_m, diff_b]).T
    # Abilities.sort_values(by='abil_m', inplace=True)

    ttl = 'Difficulties distribution for course %s' % cid
    ttl += '\n %5s (%3d U - %3d P)' % (crs.kw, crs.usrcnt, crs.pblcnt)
    print
    print ttl
    a = 1
    # axes = Abilities.plot.hist(stacked=True, bins=30, subplots=True,
    # title=ttl, )  # ax=ax)
    axes = Difficulties.plot.hist(stacked=True, bins=30, subplots=True,
                                  title=ttl, )  # ax=ax)
    ax = axes[0]
    ax.set_title("Analysis on means matrice",
                 fontsize=14, alpha=a, ha='left')
    axes[1].set_title("Analysis on binary matrice",
                      fontsize=14, alpha=a, ha='left')
    fig = ax.get_figure()
    fig.suptitle(ttl, fontsize=18, alpha=a)
    if not cid:
        cid = timer()

    # Create new directory
    output_dir = "hist/Diff/%s" % (crs.kw)
    mkdir_p(output_dir)

    fig.savefig('%s/%s.png' %
                (output_dir,cid), bbox_inches='tight', dpi=300)
    print '%s.png' % cid


    ttl = 'Abilities distribution for course %s' % cid
    ttl += '\n %5s (%3d U - %3d P)' % (crs.kw, crs.usrcnt, crs.pblcnt)
    print
    print ttl
    a = 1
    # axes = Abilities.plot.hist(stacked=True, bins=30, subplots=True,
    # title=ttl, )  # ax=ax)
    axes = Abilities.plot.hist(stacked=True, bins=20, subplots=True,
                                  title=ttl, )  # ax=ax)
    ax = axes[0]
    ax.set_title("Analysis on means matrice",
                 fontsize=14, alpha=a, ha='left')
    axes[1].set_title("Analysis on binary matrice",
                      fontsize=14, alpha=a, ha='left')
    fig = ax.get_figure()
    fig.suptitle(ttl, fontsize=18, alpha=a)
    if not cid:
        cid = timer()

    # Create new directory
    output_dir = "hist/Diff/%s" % (crs.kw)
    mkdir_p(output_dir)

    fig.savefig('%s/%s.png' %
                (output_dir,cid), bbox_inches='tight', dpi=300)
    print '%s.png' % cid


if __name__ == "__main__":
    courses = get_courses(con)
    # print courses[courses.course_id == 'C00198']
    # print courses[(courses.usrcnt > 20) & (courses.pblcnt > 20)]
    # print courses[courses.usrcnt > 20 ]
    # print courses[courses.pblcnt > 20 ]
    # print courses
    # hist_course()
    for c, row in courses.iterrows():
        # print row.course_id
        hist_course(c, row)
