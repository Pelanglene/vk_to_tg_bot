import shelve


def set_message_id(user_id, new_message_id):
    with shelve.open('last_message') as shlv:
        shlv[str(user_id)] = new_message_id


def get_message_id(user_id):
    with shelve.open('last_message') as shlv:
        try:
            return shlv[str(user_id)]
        except:
            shlv[str(user_id)] = -1
            return -1


def get_groups(user_id):
    with shelve.open('groups') as groups:
        try:
            return groups[str(user_id)].split(',')
        except:
            groups[str(user_id)] = ','
            return ','.split(',')


def get_groups_str(user_id):
    with shelve.open('groups') as groups:
        try:
            return groups[str(user_id)]
        except:
            groups[str(user_id)] = ','
            return ','


def add_group(user_id, new_group):   # first check if in list
    print('+', new_group)
    grps = get_groups_str(user_id)
    if grps.find(','+new_group+',') != -1:
        return
    grps += new_group + ','
    print('added ', grps)
    with shelve.open('groups') as groups:
        groups[str(user_id)] = grps


def delete_group(user_id, group):
    grps = get_groups_str(user_id)
    grps = grps.replace(',' + group + ',', ',')
    with shelve.open('groups') as groups:
        groups[str(user_id)] = grps


def set_state(user_id, new_state):
    with shelve.open('states') as states:
        states[str(int(user_id))] = new_state


def get_state(user_id):
    try:
        with shelve.open('states') as states:
            return states[str(user_id)]
    except:
        with shelve.open('states') as states:
            states[str(int(user_id))] = 'menu'
        return 'menu'


def get_users(need_list=False):
    with shelve.open('users') as users:
        try:
            if need_list:
                return users['0'].split(',')
            else:
                return users['0']
        except:
            users['0'] = ''
            if need_list:
                return ''.split(',')
            else:
                return ''


def add_user(user_id):
    users_str = get_users()
    if users_str.find(str(user_id)) == -1:
        users_str += str(user_id) + ','
        with shelve.open('users') as users:
            users['0'] = users_str