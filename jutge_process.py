# import pandas as pd
from timeit import default_timer as timer

import psycopg2
dbname = "test1"
con = psycopg2.connect("dbname=%s" % dbname)

from jutge import *
from jutgeAnalyser import *


u = select_users(con, course_id="C00198")
p = select_pbls(con, course_id="C00198", )

m = process(u, p, src="csv/means.csv")

print m.apply(float)