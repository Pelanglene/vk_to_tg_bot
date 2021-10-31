import vk_session
from keyboa import keyboa_maker
from presets import *

menu = [
        {'text': 'Редактировать группы',
         'callback_data': 'groups'},
        {'text': 'Настройки',
         'callback_data': 'settings'},
        {'text': 'Информация',
         'callback_data': 'info'}
]


def make_groups_keyboard(groups_list):
    groups = []
    print(groups_list)
    for ind in range(len(groups_list)):
        if groups_list[ind] == '':
            continue
        groups.append([{'text': vk_session.vk_session.method('groups.getById', {'group_ids': str(groups_list[ind])})[0]['name'],
                        'url': 'https://vk.com/public' + str(groups_list[ind])},
                       {'text': 'Удалить',
                        'callback_data': 'del' + str(groups_list[ind])}])
    print('finish')

    groups += [{'text': 'Добавить группу',
                'callback_data': 'add_group'}]
    print('finish')
    groups += [{'text': 'Назад',
                'callback_data': 'menu'}]
    print(groups)
    return keyboa_maker(items=groups)


settings = [
    {'Назад': 'menu'}
]

add_group = [
    {'text': 'Назад',
     'callback_data': 'groups'}
]

kb_menu = keyboa_maker(items=menu)
kb_settings = keyboa_maker(items=settings)
kb_add_group = keyboa_maker(items=add_group)
#kb_back = keyboa_maker(items=back)