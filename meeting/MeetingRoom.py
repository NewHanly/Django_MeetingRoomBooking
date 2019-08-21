import time,json

class MeetingRoom():
    roomscount = 0
    rooms = {}
    def __init__(self, name, info = '暂无描述', *args):
        self.name = name
        self.no = str(MeetingRoom.roomscount + 1)
        self.info = info
        self.meeting = {}
        MeetingRoom.roomscount += 1
        MeetingRoom.rooms[self.no] = self

    def addMeeting(self, mttitle,mtdate, mtst, mtet, host, hostid):
        st = mtdate + ' ' + mtst
        et = mtdate + ' ' + mtet
        st_stamp = time.mktime(time.strptime(st, '%Y-%m-%d %H:%M'))
        et_stamp = time.mktime(time.strptime(et, '%Y-%m-%d %H:%M'))
        for m in self.meeting.values():
            if(max(m.st_stamp,st_stamp) < min(m.et_stamp,et_stamp)):
                return False
        mt = Meeting(mttitle, st, et, host, hostid, st_stamp, et_stamp)
        self.meeting[str(mt.no)] = mt
        return True

    def delMeeting(self, mtno, userid):
        if(userid == self.meeting[mtno].hostid or self.isAdmin(userid)):
            del(self.meeting[mtno])
            return True
        return False

        
    def isAdmin(self, userid):
        with open('meeting/static/json/admins.json') as fp:
            admins = json.load(fp)
            for a in admins:
                if(a == userid):
                    return True
        return False

class Meeting():
    meetingcount = 0
    def __init__(self, mttitle, mtst, mtet, host, hostid, st_stamp, et_stamp):
        self.title = mttitle
        self.no = Meeting.meetingcount + 1
        self.host = host
        self.hostid = hostid
        self.st = mtst
        self.et = mtet
        self.et_stamp = et_stamp
        self.st_stamp = st_stamp
        Meeting.meetingcount += 1