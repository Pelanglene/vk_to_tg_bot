import time
import requests
import bd
import shelve
from bd import *
import conffig
import vk_session
from tg_bot import *


def make_link(post):
    return 'https://vk.com/wall-{0}_{1}'.format(abs(post['from_id']), abs(post['id']))


params = {'owner_id': '',
          'access_token': conffig.vk_token,
          'v': '5.130',
          'count': '3'}

while True:
    users = get_users(True)
    cur_time = time.time()
    for user in users:
        groups = get_groups(user)
        print(user, groups)
        for group in groups:
            try:
                if group == '':
                    continue
                #if group['is_closed']:
                #    print(group['owner_id'], end='!!!\n')
                group_info = vk_session.vk_session.method('groups.getById', {'group_ids': int(group), 'v': '5.130'})
                params['owner_id'] = -int(group)
                posts_gg = vk_session.vk_session.method('wall.get', params)
                posts = posts_gg['items']
                #print(group_info)
                #print(user, posts, end='!!!\n')
                #print(len(posts))
                for post in posts:
                    if post['date'] + 60.5 > cur_time:
                        if group_info[0]['is_closed'] == 1:
                            print('group name:', group_info[0]['name'])
                            try:
                                bot.send_message(user, make_link(post) + '\n<b>' + group_info[0]['name'] + '</b>:\n' + post['text'], parse_mode='HTML')
                            except:
                                bot.send_message(user, make_link(post))
                        else:
                            bot.send_message(user, make_link(post))
            except:
                print('gg')
                pass
    time.sleep(60)