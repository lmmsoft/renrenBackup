# coding: utf8

from datetime import datetime
import logging

from config import config
from models import Status

from .utils import get_comments, get_likes


logger = logging.getLogger(__name__)
crawler = config.crawler


def load_status_page(page, uid=crawler.uid):
    r = crawler.get_json(config.STATUS_URL, {'userId': uid, 'curpage': page})

    likes = r['likeInfoMap']
    for s in r['doingArray']:
        sid = int(s['id'])
        status = {
            'id': sid,
            'uid': uid,
            't': datetime.fromtimestamp(int(s['createTime']) / 1000),
            'content': s['content'],                            # 内容
            'like': likes.get('status_{sid}'.format(sid=sid), 0),  # 点赞
            'repeat': s['repeatCountTotal'],                    # 转发
            'comment': s['comment_count'],                      # 评论
            'rootContent': s.get('rootContent', ''),            # 如果是转发，转发的原文
            'rootUid': s.get('rootDoingUserId', 0),             # 转发原 uid
            'rootUname': s.get('rootDoingUserName', ''),        # 转发原 username
            'location': s.get('location', ''),                  # 带地理位置的地名
            'locationUrl': s.get('locationUrl', ''),            # 地理位置的人人地点
        }
        Status.insert(**status).on_conflict('replace').execute()

        if status['comment']:
            get_comments(sid, 'status', owner=uid)
        if status['like']:
            get_likes(sid, 'status', owner=uid)

    logger.info('  on page {page}, {parsed} parsed'.format(page=page, parsed=len(r['doingArray'])))

    return r['count']


def get_status(uid=crawler.uid):
    cur_page = 0
    total = config.ITEMS_PER_PAGE
    total_page = int(total / config.ITEMS_PER_PAGE) + 1 if (total % config.ITEMS_PER_PAGE != 0) else 0
    while cur_page * config.ITEMS_PER_PAGE < total:
        logger.info(
            'start crawl status page {cur_page} / {total_page}'.format(cur_page=cur_page + 1, total_page=total_page)) # 显示的页面序号从第一页开始
        total = load_status_page(cur_page, uid)
        cur_page += 1

    return total
