# import pandas as pd
from timeit import default_timer as timer

import psycopg2
dbname = "test1"
con = psycopg2.connect("dbname=%s" % dbname)

from jutge import *
from jutgeAnalyser import *

start = timer()
d1 = start

# Select every users from the db as a python pandas dataframe
# everyusers = select_users(con, ids_list=True)
everyusers = select_users(con, course_id="C00198")
print len(everyusers), "\tusers selected"

# Select every pbls from the db as a python pandas dataframe
# everypbls = select_pbls(con, ids_list=True)
everypbls = select_pbls(con, course_id="C00198", )
print len(everypbls), "\tproblems selected"

subs = select_submissions(con, lusr=everyusers, lpbl=everypbls)
print subs.index.size, "\tsubmissions found"

d2 = timer()
print "timestamp = %.3f seconds\n" % (d2 - d1)

print "bianary matrix generation ..."
bmat = bianary_mat(everyusers, everypbls, subs)
bmat.to_csv("csv/bin.csv", decimal=',', sep=';')

d3 = timer()
print "timestamp = %.3f seconds\n" % (d3 - d2)

print "means matrix generation ..."
mmat = means_mat(everyusers, everypbls, subs)
mmat.to_csv("csv/means.csv",  decimal=',', sep=';')

d4 = timer()
print "timestamp = %.3f seconds\n" % (d4 - d3)

end = d4
print "Total time = %.3f seconds\n" % (end - start)
