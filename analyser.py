#!/usr/bin/python
import pandas as pd
import numpy as np
import random

import psycopg2


def generate_submissions(users=4, pbls=8):
	'''
	return a pandas dataframe :

   submission_uid user_id problem_id veredict submission_id
0      S000000000  U00000     P00000       EE          S000
...

	generate randomly with a number given number of users
	and problems

	for each 
	'''

	# define ids for users and problems
	users = [ ("U%05d"%i) for i in range(users)]
	pbls = [ ("P%05d"%i) for i in range(pbls)]

	headers =  ["submission_uid", "user_id", "problem_id", 
				"veredict", "submission_id"]
	verdicts = ["AC", "EE"]
	
	#
	df = pd.DataFrame(columns=headers) # dataframe to be returned

	submission_uid = 0

	for u in users:
	    for p in pbls:
	    	# define a random nb of attemps for a user and a specific pbl
	        attempts = random.randint(0,5)
	        submission_id = 0
	        for i in range(attempts):
	            v = "EE"
	            # randomly define if the user succed or not for his last attempt
	            if i == attempts - 1:
	                v = random.choice(verdicts)
	            sub = ["S%09d"%submission_uid, u, p, v, "S%03d"%submission_id]
	            df.loc[len(df)] = sub
	            submission_uid+=1
	            submission_id+=1

	return df

def import_submissions(course_id = "C00198", dbname="test1"):
	con = psycopg2.connect("dbname=%s"%dbname)
	# subs = generate_submissions(users=10, pbls=100)

	userslist = pd.read_sql_query("select user_id from coursesusers where course_id like '%s';" % course_id,con=con)
	userslist = [u[0] for u in userslist.values if u[0]]
	usersstr = str(userslist).strip('[]')

	users = pd.read_sql_query("select user_id, creation_date from users \
	                            where demo=0 and instructor=0 and administrator=0\
	                            and user_id in (%s);" % usersstr,con=con)

	lusers = users.user_id.tolist()
	usersstr = str(lusers).strip('[]')

	problists = pd.read_sql_query("select list_id from courseslists where course_id like '%s';" % course_id ,con=con)
	problists = [l[0] for l in problists.values if l[0]]
	problistsstr = str(problists).strip('[]')

	probs = pd.read_sql_query("select problem_nm from listitems where list_id \
	                                in(%s);" % problistsstr,con=con)

	lprobs = [p[0] for p in probs.values if p[0]]
	lprobsstr = str(lprobs).strip('[]')

	submissions = pd.read_sql_query("select submission_uid, user_id, problem_id, submission_id, \
	                        state, time_out, time_in, veredict, score \
	                        from submissions where user_id in (%s);" % (usersstr) ,
	                       con=con)

	submissions.problem_id = submissions.problem_id.apply(lambda x: x[:-3])
	#submissions.set_index('submission_uid', inplace=True)

	subs = submissions[submissions.problem_id.isin(lprobs)]
	return subs

def magnitude(v):
	'''
	return the magnitude of a list of values
	'''
	return np.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def normalize(v):
	'''
	normalize a list of values
	'''
	vmag = magnitude(v)
	if vmag:
		for i in range(len(v)):
			v[i] = v[i]/vmag

def bianary_mat(subs):
	'''
	return a binary matrix representative
	of witch problems each user has solved

	need a dataframe of submisions as input
	'''

	# get lists of unique users and pbls
	users = subs.user_id.unique()
	pbls = subs.problem_id.unique()
	table = pd.DataFrame(data = 0, columns=users , index=pbls)

	couples = subs[subs.veredict == "AC"][["user_id","problem_id"]].values

	for u, p in couples:
	    table[u][p] = 1

	return table

from itertools import product

def succes_mat(subs):
    '''
    '''
    # get lists of unique users and pbls
    users = subs.user_id.unique()
    pbls = subs.problem_id.unique()
    table = pd.DataFrame(data = 0.0, columns=users , index=pbls)

    #couples = subs[subs.veredict == "AC"][["user_id","problem_id"]].values
    for u, p in product(users, pbls):
    	dfTot =  subs[(subs.user_id == u) & (subs.problem_id == p)]

        ACs = dfTot[(dfTot.veredict == "AC")].submission_uid.count()
        TOT = dfTot.submission_uid.count()
        if TOT:
            table[u][p] = float(ACs) / TOT
        else:
            table[u][p] = 0

    return table

def linear1(row, vector):
    '''
    return the level of a row relatively to a vector
    '''
    return  (row[1] * vector).sum() / len(row[1])

def linear2(row, vector):
    '''
    return the level of a row relatively to a vector
    '''
    return 1 - ((row[1] * vector).sum()  / len(row[1]))


def process_bianary_mat(bm, rel_v, f=linear1, name='V', Horiz=False):
    '''
    evaluate the vector from a bm using a method
    and relatively to another vector
    '''
    # evaluate for each row of the binary table
    bmm = bm
    if Horiz:
        bmm=bm.T
    
    vector = [f(row, rel_v) for row in bmm.iterrows()]
    vector = pd.Series(vector, index=bmm.index, 
                             name=name)
    normalize(vector)
    
    return vector


def succes_means(subs, col_name='problem_id'):
    
    idx = subs[col_name].unique()
    df = pd.DataFrame(index=idx, columns=["tots", "goods", "means"])

    for i in idx:
        #print dfProbs
        df.tots[i] = subs[(subs[col_name] == i)].submission_uid.count()
        df.goods[i] = subs[(subs[col_name] == i) & (subs.veredict == "AC")].submission_uid.count()
        if df.tots[i]:
	        df.means[i] = float(df.goods[i]) / df.tots[i]

    return df

from itertools import product

def succes_mat(subs):
    '''
    '''

    # get lists of unique users and pbls
    users = subs.user_id.unique()
    pbls = subs.problem_id.unique()
    table = pd.DataFrame(data = 0.0, columns=users , index=pbls)

    #couples = subs[subs.veredict == "AC"][["user_id","problem_id"]].values
    for u, p in product(users, pbls):
        ACs = subs[(subs.user_id == u) & (subs.problem_id == p) & 
                           (subs.veredict == "AC")].submission_uid.count()
        TOT = subs[(subs.user_id == u) & (subs.problem_id == p)].submission_uid.count()
        if TOT:
            table[u][p] = float(ACs) / TOT
        else:
            table[u][p] = 0

    return table

def cmpVect(v1, v2):
    #m1 = magnitude(v1)
    #m2 = magnitude(v2)
    #mx = float(m1+m2)/2
    D = (v1 - v2) #/ mx
    return(magnitude(D.apply(abs)))