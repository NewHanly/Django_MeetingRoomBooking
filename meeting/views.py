# coding:utf-8
import pickle
import json
from meeting.DelFunc import isAdmin
from meeting.WeChatAPI import getUsername, getUserid, getUsername_ID
from meeting.MeetingRoom import MeetingRoom, Meeting
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect

with open('meeting/static/pkl/rooms.pkl', 'rb') as rf:
    try:
        MeetingRoom.rooms = pickle.load(rf)
    except:
        pass

def index(request):
    usercode = request.GET.get('code')
    with open('meeting/static/pkl/rooms.pkl', 'wb') as rf:
        pickle.dump(MeetingRoom.rooms, rf)
    if(usercode is not None):
        item_list = list(MeetingRoom.rooms.values())
        return render(request, 'roomlist.html', {'string': '会议室列表', 'item_list': item_list, 'code': '/?code=' + usercode})
    else:
        return alert(request, '请用企业微信登录')


def roomList(request, *args, **kwargs):
    with open("/static/pkl/rooms.pkl") as rf:
        item_list = pickle.loads(rf.read())
    usercode = request.GET.get('code')
    return render(request, 'roomlist.html', {'string': '会议室列表', 'item_list': item_list.values(), 'code': '/?code=' + usercode})


def meetingList(request, *args, **kwargs):
    usercode = request.GET.get('code')
    if(usercode != None):
        item_list = sorted(list(MeetingRoom.rooms[str(kwargs['mtno'])].meeting.values()),key=lambda x: x.st_stamp, reverse=True)
        if(item_list != []):
            string = '会议列表'
        else:
            item_list = []
            string = '该会议室暂无会议'
        return render(request, 'meetinglist.html', {'string': string, 'item_list': item_list, 'code': '/?code=' + usercode, 'num': kwargs['mtno']})
    else:
        return alert(request, '请用企业微信登录')


def addmeeting(request, *args, **kwargs):
    usercode = request.GET.get('code')
    num = request.GET.get('num')
    if(usercode is not None):
        try:
            userid = getUserid(usercode)
            user_name = getUsername_ID (userid)
        except:
            user_name = ''
        return render(request, 'addmeeting.html', {'username': user_name, 'userid':userid, 'num': num})
    else:
        return alert(request, '请用企业微信登录')


def addroom(request, *args, **kwargs):
    userid = getUserid(request.GET.get('code'))
    print(userid)
    print(isAdmin(userid))
    if(isAdmin(userid)):
        return render(request, 'addroom.html')
    else:
        return render(request, 'goback.html')


def addcallback(request):
    num = str(request.GET.get('num'))
    if(num != ''):
        try:
            data = json.loads(request.body.decode('UTF-8'))
        except:
            return HttpResponse('请重新登录')
        if(num == '-1'):
            MeetingRoom(data['room_name'], data['room_info'])
        else:
            if(MeetingRoom.rooms[num].addMeeting(
                data['mttitle'], data['mtdate'], data['mtst'], data['mtet'], data['host'], data['hostid'])):
                return HttpResponse('预约成功')
    return HttpResponse('时间冲突,预约失败')


def delcallback(request):
    try:
        data = json.loads(request.body.decode('UTF-8'))
    except:
        return HttpResponse('')
    if(data['type'] == 'meeting'):
        userid = getUserid(request.GET.get('code'))
        if(MeetingRoom.rooms[data['from']].delMeeting(data['mtno'], userid)):
            return HttpResponse('取消成功')
        else:
            return HttpResponse('失败:没有权限或登录失效!')
    elif(data['type'] == 'room'):
        if(isAdmin(getUserid(request.GET.get('code')))):
            del(MeetingRoom.rooms[data['rmno']])
            return HttpResponse('删除成功')
        else:
            return HttpResponse('您没有权限')
    return HttpResponse('未知操作')


def alert(request, msg):
    return render(request, 'message.html', {'msg': msg})
