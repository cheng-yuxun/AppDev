import os
import shelve
basedir = os.getcwd()
dbdir = f'{basedir}/data/db/database'

def get_db():
    return dbdir

def create_db():
    db = shelve.open(dbdir, 'c')
    labels = {
        'Users',
        'Events',
        'current_session',
        'Products',
        'Shirts',
        'Inventory',
        'Rewards',
        'History',
        'registered',
        'points',
        'Accounts_created',
        'Admin',
        'expirytime',
        'forgetful_user'
    }
    for x in labels:
        db[x] = {}
    db.close()
    print('---creating db---')