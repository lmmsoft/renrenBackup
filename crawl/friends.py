# coding: utf8

import logging
import json
from config import config
from models import Friend

logger = logging.getLogger(__name__)
crawler = config.crawler


def load_friend_list(uid):
    json_mfriends = get_mfriends()

    for f in json_mfriends:
        print("name={name}, id={id}".format(name=f["fname"], id=f['fid']))
        frined = {
            'uid': uid,
            'fid': f.get('fid', 0),
            'fgroups': f.get('fgroups', ''),
            'fname': f.get('fname', ''),
            'info': f.get('info', ''),
            'headPicLargeUrl': f.get('large_url', ''),
            'headPicTinyUrl': f.get('tiny_url', ''),
            'albumStatus': 0,
            'blogStatus': 0,
            'friendsStatus': 0,
            'gossipStatus': 0,
            'statusStatus': 0
        }
        Friend.insert(**frined).on_conflict('ignore').execute()

    return len(json_mfriends)


def crawal_all_friend(uid):
    return Friend.select().where(Friend.uid == uid)


def update_friend_gossip_state(uid, fid, state):
    Friend.update(gossipStatus=state).where(Friend.uid == uid, Friend.fid == fid).execute()


def get_mfriends():
    # get my friends
    # 数据格式：data[x]['fid']/['timepos']/['comf']/['compos']/['large_url']/['tiny_url']/['fname']/['info']/['pos']
    # groups/friends/specialfriends/'hotFriends' / 'hostFriendCount'

    # {'fid': 276427164, 'timepos': 654, 'fgroups': ['MSRA'], 'comf': 21, 'compos': 969, 'large_url': 'http://hdn.xnimg.cn/photos/hdn321/20140508/1310/h_large_ZdRm_e0a50000799a195a.jpg', 'tiny_url': 'http://hdn.xnimg.cn/photos/hdn321/20140508/1310/h_tiny_OsvD_e0a50000799a195a.jpg', 'fname': '艾可', 'info': '江西', 'pos': 1}

    resp = crawler.get_url(config.FRIENDS_URL)

    raw_html = resp.text
    string = raw_html.partition('"data" : ')[2]
    string = string.rpartition('}')[0]
    json_string = json.loads(string)

    return json_string['friends']


def get_ofriends(ownerid):
    # get others friends
    # 数据格式 data[x]['id']/['netName']/['netNamePrefix']/['head']/['isOnLine']/['name']

    data = crawler.get_json(config.FRIENDS_OTHER_URL.format(ownerid=ownerid))
    return data['candidate']


def get_sfriends(ownerid):
    # get share friends 共同好友
    # 数据格式 data[x]['id']/['netName']/['netNamePrefix']/['head']/['isOnLine']/['name']
    url = config.FRIENDS_SHARE_URL.format(ownerid=str(ownerid))
    data = crawler.get_json(url)
    return data['candidate']
