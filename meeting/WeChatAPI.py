import requests
import json

corpid = ''
corpsecret = ''


def getAc_token():
    token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + \
        corpid + '&corpsecret=' + corpsecret
    ac_token = requests.get(token_url).json().get('access_token')
    return ac_token


def getUserid(usercode):
    userid_url = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=' + \
        getAc_token() + '&code=' + usercode
    userid = requests.get(userid_url).json().get('UserId')
    return userid


def getUsername(usercode):
    username_url = 'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=' + \
        getAc_token() + '&userid=' + getUserid(usercode)
    username = requests.get(username_url).json().get('name')
    return username

def getUsername_ID(userid):
    username_url = 'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=' + \
        getAc_token() + '&userid=' + userid
    username = requests.get(username_url).json().get('name')
    return username