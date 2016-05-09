#!/usr/bin/python
import pandas as pd
import numpy as np
import random
from timeit import default_timer as timer

from itertools import product


def magnitude(v):
    '''
    return the magnitude of a list of values
    '''
    return np.sqrt(sum(v[i] * v[i] for i in range(len(v))))


def normalize(v):
    '''
    normalize a list of values
    '''
    vmag = magnitude(v)
    if vmag:
        for i in range(len(v)):
            v[i] = v[i] / vmag


def bianary_mat(users, pbls, subs=pd.DataFrame()):
    '''
    return a binary matrix representative
    of witch problems each user has solved

    need a dataframe of submisions as input
    '''

    # get lists of unique users and pbls
    # users = subs.user_id.unique()
    # pbls = subs.problem_id.unique()
    table = pd.DataFrame(data=0, columns=users, index=pbls)

    if not subs.empty:
        couples = subs[subs.veredict == "AC"][["user_id", "problem_id"]].values

        for u, p in couples:
            table[u][p] = 1

    return table


def tots_mats(users, pbls, subs=pd.DataFrame()):
    '''
    '''
    # get lists of unique users and pbls
    # users = subs.user_id.unique()
    # pbls = subs.problem_id.unique()
    ac_table = pd.DataFrame(data=0.0, columns=users, index=pbls)
    tot_table = pd.DataFrame(data=0.0, columns=users, index=pbls)

    if not subs.empty:
        couples = subs[subs.veredict == "AC"][["user_id", "problem_id"]].values
        for u, p in couples:
            ac_table[u][p] += 1

        couples = subs[["user_id", "problem_id"]].values
        for u, p in couples:
            tot_table[u][p] += 1

    return ac_table, tot_table


def means_mat(users, pbls, subs=pd.DataFrame()):
    """
    """
    b, c = tots_mats(users, pbls, subs)
    d = b / c
    mat = d.fillna(0)
    return mat


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
    users = [("U%04d" % i) for i in range(users)]
    pbls = [("P%04d" % i) for i in range(pbls)]

    headers = ["submission_uid", "user_id", "problem_id",
               "veredict", "submission_id"]
    verdicts = ["AC", "EE"]

    #
    df = pd.DataFrame(columns=headers)  # dataframe to be returned

    submission_uid = 0

    for u in users:
        for p in pbls:
            # define a random nb of attemps for a user and a specific pbl
            attempts = random.randint(0, 5)
            submission_id = 0
            for i in range(attempts):
                v = "EE"
                # randomly define if the user succed or not for his last
                # attempt
                if i == attempts - 1:
                    v = random.choice(verdicts)
                sub = ["S%09d" % submission_uid, u, p, v, "S%03d" %
                       submission_id]
                df.loc[len(df)] = sub
                submission_uid += 1
                submission_id += 1

    return df


def linear1(row, vector):
    '''
    return the level of a row relatively to a vector
    '''
    return (row[1] * vector).sum() / len(row[1])


def process(usrs, pbls, meth='svd', src="csv/bin.csv", vert_name="diff",
            hor_name="abil", itercnt=5, verbose=True):

        # get matrixs
    start = timer()
    mat = pd.read_csv(src, index_col=0, sep=";", decimal=",", verbose=False)
    # mat = mat.applymap(lambda x: float(x.replace(',', '.')))
    # print mat.describe()
    # print mat[[0]].sum()
    mat = mat.T[pbls]
    mat = mat.T[usrs]
    # print mat
    # mat.apply()

    # vectors initialisation
    vert = pd.Series([1.0 for i in range(len(mat.index))],
                     index=mat.index, name=vert_name + '_0')
    normalize(vert)
    hor = pd.Series([1.0 for i in range(len(mat.columns))],
                    index=mat.columns, name=hor_name + '_0')
    normalize(hor)

    if meth == 'svd':
        npmat = mat.as_matrix()
        # compute scd
        U, s, V = np.linalg.svd(npmat, full_matrices=False)

        # get vertical evaluation (probls difficulties)
        U = pd.DataFrame(U, index=mat.index)
        vert = pd.Series(U[0], index=mat.index, name=vert_name)
        # vert = vert.apply(abs)
        # get rid of unactive problems
        # vert = vert[vert > 0]

        # get horizontal evaluation (users abilities)
        hor = pd.Series(V[0], index=mat.columns, name=hor_name)
        # hor = hor.apply(abs)
        # get rid of un active users
        # hor = hor[hor > 0]

    elif meth == 'lin':
        for i in range(0, itercnt):
            vert = process_matrix(
                mat, hor, f=linear2, name="%s%d" % (vert.name[:-1], i))
            hor = process_matrix(mat, vert, name="%s%d" %
                                 (hor.name[:-1], i), Horiz=True)


    end = timer()
    if verbose:
        print ("Proceed in %.3f seconds" % (end - start))
        print ("Using the %s method" % meth)
        print ("Based on the matrix %s : " % src)
        print ("For %d users and %d problems" %
               (len(mat.columns), len(mat.index)))
        print ""

    # return (mat, )
    return (mat, vert, hor)

    
