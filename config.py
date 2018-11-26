# coding: utf8

import sys


class LocalConfig(object):
    py3 = sys.version_info[0] >= 3

    LOGGING_INI = './logging.ini'

    crawler = None
    DATABASE = 'renren_bak.db'

    BAK_OUTPUT_TAR = 'backup.tar'

    COOKIE_FILE = "./.cookies.json"

    ITEMS_PER_PAGE = 20
    TIMEOUT = 15
    RETRY_TIMES = 10

    DEFAULT_HEAD_PIC = './static/men_tiny.gif'

    ENCRYPT_KEY_URL = "http://login.renren.com/ajax/getEncryptKey"
    LOGIN_URL = "http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp={ts}"
    ICODE_URL = "http://icode.renren.com/getcode.do?t=web_login&rnd={rnd}"
    ICODE_FILEPATH = "./static/icode.jpg"

    HOMEPAGE_URL = "http://www.renren.com/{uid}/profile"

    COMMENT_URL = "http://comment.renren.com/comment/xoa2"
    GLOBAL_COMMENT_URL = "http://comment.renren.com/comment/xoa2/global"
    LIKE_URL = "http://like.renren.com/showlikedetail"

    STATUS_URL = "http://status.renren.com/GetSomeomeDoingList.do"

    GOSSIP_PAGE_URL = "http://gossip.renren.com/list/{uid}"
    GOSSIP_URL = "http://gossip.renren.com/ajaxgossiplist.do"

    ALBUM_LIST_URL = "http://photo.renren.com/photo/{uid}/albumlist/v7"
    ALBUM_SUMMARY_URL = "http://photo.renren.com/photo/{uid}/album-{album_id}/v7"
    PHOTO_INFO_URL = "http://photo.renren.com/photo/{uid}/photo-{photo_id}/layer"

    BLOG_LIST_URL = "http://blog.renren.com/blog/{uid}/blogs"
    BLOGS_PER_PAGE = 10
    BLOG_DETAIL_URL = "http://blog.renren.com/blog/{uid}/{blog_id}"

    FRIENDS_URL = "http://friend.renren.com/groupsdata"
    FRIENDS_OTHER_URL = "http://friend.renren.com/friendfriendSelector?p={%22init%22:true,%22uid%22:true,%22uhead%22:true,%22uname%22:true,%22group%22:true,%22net%22:true,%22param%22:{%22guest%22: {ownerid}}}"
    FRIENDS_SHARE_URL = "http://friend.renren.com/shareFriends?&p={%22init%22:true,%22uid%22:true,%22uhead%22:true,%22uname%22:true,%22group%22:true,%22net%22:true,%22param%22:{%22guest%22: {ownerid}}}"

config = LocalConfig
