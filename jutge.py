"""
This file contain basics operations to manipulate data
from the Jutge.org database

"""

import pandas as pd


class User():
    """Contain data from users in db"""

    def __init__(self, user_id, creation_date="2001-01-01", administrator=0,
                 instructor=0, demo=0, unregistered=0):
        self.user_id = user_id
        self.creation_date = creation_date
        self.administrator = administrator
        self.instructor = instructor
        self.demo = demo
        self.unregistered = unregistered


class Problem(object):
    """docstring for Problem"""

    def __init__(self, problem_id, language_id="",
                 title="", original_language_id="", checked=1):
        # can be given with or without language id
        self.problem_id = problem_id
        self.problem_nm = problem_id[:-3]
        self.language_id = language_id
        if len(problem_id) > 6:
            self.language_id = problem_id[-3:]
        self.title = title
        self.original_language_id = original_language_id
        self.checked = checked


def select_users(con, ids_list=True, course_id=None, d1=None, d2=None):
    """
    Return a dataframe of user (ids)
    which are subsribed to a specific course (course_id)
    registered after d1 and before d2

    If nothing is given the selection will be perform
    on the entire database (omitting irrelevant users)

    note :
        course_id='%' every user reated to at least one course
    """

    req = "select user_id, creation_date from users \
            where demo=0 and instructor=0 and administrator=0"

    if course_id:
        userslist = pd.read_sql_query(
            "select user_id from coursesusers\
            where course_id like '%s';" % course_id, con=con)
        userslist = [u[0] for u in userslist.values if u[0]]
        usersstr = str(userslist).strip('[]')
        req += " and user_id in (%s);" % usersstr

    if d1:
        pass
    if d2:
        pass

    users = pd.read_sql_query(req, con=con)

    if ids_list:
        users = users.user_id.tolist()
        # usersstr = str(lusers).strip('[]')

    return users


def select_pbls(con, ids_list=True, course_id=None, list_id=None, ptype="%P%"):
    """
    Return a dataframe of problems (ids)
    which are contained to a specific course (course_id)
    or a specific list inside a course (list_id)

    If nothing is given the selection will be perform
    on the entire database (omitting irrelevant users)

    note :
        course_id='%' every problem related to at least one course
        ptype='%' every types of problems
    """

    if list_id:
        problists = [list_id]
        problistsstr = str(problists).strip('[]')
        probs = pd.read_sql_query("select problem_nm from listitems \
            where list_id in(%s);" % problistsstr, con=con)
    elif course_id:
        # userslist = pd.read_sql_query(
        #     "select user_id from coursesusers\
        #     where course_id like '%s';" % course_id, con=con)
        # userslist = [u[0] for u in userslist.values if u[0]]
        # usersstr = str(userslist).strip('[]')
        # req += " and user_id in (%s);" % usersstr

        problists = pd.read_sql_query(
            "select list_id from courseslists \
            where course_id like '%s';" % course_id, con=con)
        problists = [l[0] for l in problists.values if l[0]]
        problistsstr = str(problists).strip('[]')
        probs = pd.read_sql_query("select problem_nm from listitems \
            where list_id in(%s) and problem_nm like '%s';"
                                  % (problistsstr, ptype), con=con)

    else:
        probs = pd.read_sql_query("select problem_nm from abstractproblems \
            where problem_nm like '%s';" % ptype, con=con)

    # users = pd.read_sql_query(req, con=con)
    if ids_list:
        probs = probs.problem_nm.tolist()

    return probs


def select_submisions(con, lusr=None, lpbl=None, course_id=None):
    """"
    Return a subset of submission as a pandas dataframe
    regarding to :
        * a specific list of users (lusr)
        * a specific list of problems
        * a specific course

    The logic is if no list is provided for users and pbls,
    They will be match with the course_id.
    By default, none course_id means the entire db
    """

    if not lusr:
        lusr = select_users(con, course_id=course_id)
    if not lpbl:
        lpbl = select_pbls(con, course_id=course_id)

    usersstr = str(lusr).strip('[]')
    submissions = pd.read_sql_query("select submission_uid, user_id, problem_id, \
        submission_id, state, time_out, time_in, veredict, score \
        from submissions where user_id in (%s);" % (usersstr), con=con)

    # get rid of the language id's
    submissions.problem_id = submissions.problem_id.apply(lambda x: x[:-3])
    submissions.set_index('submission_uid', inplace=True)

    subs = submissions[submissions.problem_id.isin(lpbl)]
    subs.reset_index(inplace=True)
    return subs
