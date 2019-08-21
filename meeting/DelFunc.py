import json

def delRoom(userid, room):
    if(isAdmin(userid)):
        del(room)
        return True
    return False

def isAdmin(userid):
    with open('meeting/static/json/admins.json', 'r') as fp:
        admins = json.load(fp)
        for a in admins:
            if(a == userid):
                return True
    return False