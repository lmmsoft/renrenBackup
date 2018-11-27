# coding: utf8

import argparse
import logging
import logging.config

from playhouse.shortcuts import model_to_dict

from config import config

logging.config.fileConfig(config.LOGGING_INI)
logger = logging.getLogger(__name__)


def prepare_db():
    from models import database, FetchedUser, User, Comment, Like
    from models import Status, Gossip, Album, Photo, Blog
    from models import Friend

    with database:
        database.create_tables([FetchedUser, User, Comment, Like])
        database.create_tables([Status, Gossip, Album, Photo, Blog])
        database.create_tables([Friend])


def prepare_crawler(args):
    from crawl.crawler import Crawler

    config.crawler = Crawler(args.email, args.password, Crawler.load_cookie())

    return config.crawler


def update_fetch_info(uid):
    from models import database, FetchedUser, User, Status, Gossip, Album, Photo, Blog

    with database:
        user = User.get_or_none(User.uid == uid)
        if not user:
            raise KeyError("no such user")

        fetched_info = model_to_dict(user)
        fetched_info.update(
            status=Status.select().where(Status.uid == uid).count(),
            gossip=Gossip.select().where(Gossip.uid == uid).count(),
            album=Album.select().where(Album.uid == uid).count(),
            photo=Photo.select().where(Photo.uid == uid).count(),
            blog=Blog.select().where(Blog.uid == uid).count(),
        )

        FetchedUser.insert(**fetched_info).on_conflict('replace').execute()

        logger.info('update fetched info {fetched_info}'.format(fetched_info=fetched_info))

    return True


def fetch_status(uid):
    logger.info('prepare to fetch status')
    from crawl import status as crawl_status

    status_count = crawl_status.get_status(uid)
    logger.info('fetched {status_count} status'.format(status_count=status_count))


def fetch_gossip(uid):
    logger.info('prepare to fetch gossip')
    from crawl import gossip as crawl_gossip

    gossip_count = crawl_gossip.get_gossip(uid)
    logger.info('fetched {gossip_count} gossips'.format(gossip_count=gossip_count))


def fetch_album(uid):
    logger.info('prepare to fetch albums')
    from crawl import album as crawl_album

    album_count = crawl_album.get_albums(uid)
    logger.info('fetched {album_count} albums'.format(album_count=album_count))


def fetch_blog(uid):
    logger.info('prepare to fetch blogs')
    from crawl import blog as crawl_blog

    blog_count = crawl_blog.get_blogs(uid)
    logger.info('fetched {blog_count} blogs'.format(blog_count=blog_count))


def fetch_friend(uid):
    from crawl import friends as crawl_friend

    friend_count = crawl_friend.load_friend_list(uid)
    logger.info('fetched {friend_count} friends'.format(friend_count=friend_count))

    friend_list = crawl_friend.fetch_all_friend(uid)
    for f in friend_list:
        if f.gossipStatus == 0:
            try:
                fetch_gossip(f.fid)
                crawl_friend.update_friend_gossip_state(uid, f.fid, 1)
                logger.info('fetched album succeed on user {fid}'.format(fid=f.fid))
            except Exception:
                crawl_friend.update_friend_gossip_state(uid, f.fid, 2)
                logger.info('fetched album error on user {fid}'.format(fid=f.fid))
        elif f.gossipStatus == 1:
            logger.info('fetched album skip for succeed on user {fid}'.format(fid=f.fid))
        else:
            logger.info('fetched album skip for error on user {fid}'.format(fid=f.fid))


def fetch_user(uid, args):
    fetched_flag = False

    from crawl.utils import get_user
    get_user(uid)

    if args.fetch_status:
        fetch_status(uid)
        fetched_flag = True

    if args.fetch_gossip:
        fetch_gossip(uid)
        fetched_flag = True

    if args.fetch_album:
        fetch_album(uid)
        fetched_flag = True

    if args.fetch_blog:
        fetch_blog(uid)
        fetched_flag = True

    if args.fetch_friend:
        fetch_friend(uid)
        fetched_flag = True

    return fetched_flag


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="fetch renren data to backup")
    parser.add_argument('email', help="your renren email for login")
    parser.add_argument('password', help="your renren password for login")
    parser.add_argument('-s', '--fetch-status', help="fetch status or not", action="store_true")
    parser.add_argument('-g', '--fetch-gossip', help="fetch gossip or not", action="store_true")
    parser.add_argument('-a', '--fetch-album', help="fetch album or not", action="store_true")
    parser.add_argument('-b', '--fetch-blog', help="fetch blog or not", action="store_true")
    parser.add_argument('-f', '--fetch-friend', help="fetch friend or not", action="store_true")
    parser.add_argument('-u', '--fetch-uid',
                        help="user to fetch, or the login user by default", type=int)
    parser.add_argument('-r', '--refresh-count',
                        help="refresh fetched user count", action="store_true")

    cmd_args = parser.parse_args()

    prepare_db()

    cralwer = prepare_crawler(cmd_args)

    fetch_uid = cmd_args.fetch_uid if cmd_args.fetch_uid else cralwer.uid

    fetched = fetch_user(fetch_uid, cmd_args)
    if not fetched:
        logger.info('nothing need to fetch, just test login')

    if fetched or cmd_args.refresh_count:
        update_fetch_info(fetch_uid)
