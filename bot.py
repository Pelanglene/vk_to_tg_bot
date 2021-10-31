import conffig
import keyboards
import shelve
import vk_session
import time
from presets import *
import os
from bd import *
from keyboa import keyboa_maker
from tg_bot import *


@bot.message_handler(commands=['menu', 'start'])
def menu(message):
    add_user(message.chat.id)
    set_state(message.chat.id, 'menu')
    bot.send_message(message.chat.id, texts['menu'], reply_markup=keyboards.kb_menu)


@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def menu(call):
    set_state(call.message.chat.id, 'menu')

    cid = call.message.chat.id
    mid = call.message.message_id
    try:
        bot.edit_message_text(texts['menu'], cid, mid, reply_markup=keyboards.kb_menu)
    except:
        print('q1')
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'groups')
def callback(call):
    set_state(call.message.chat.id, 'groups')
    cid = call.message.chat.id
    mid = call.message.message_id
    try:
        print(get_groups(call.message.chat.id))
        bot.edit_message_text(texts['groups'], cid, mid,
                              reply_markup=keyboards.make_groups_keyboard(get_groups(call.message.chat.id)))
    except Exception as e:
        print('q2 ', e)
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'settings')
def callback(call):
    set_state(call.message.chat.id, 'settings')
    cid = call.message.chat.id
    mid = call.message.message_id
    try:
        bot.edit_message_text(texts['settings'], cid, mid,
                              reply_markup=keyboards.kb_settings)
    except:
        print('q3')
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'info')
def callback(call):
    set_state(call.message.chat.id, 'info')
    cid = call.message.chat.id
    mid = call.message.message_id
    try:
        bot.edit_message_text(texts['info'], cid, mid,
                              reply_markup=keyboards.kb_settings)
    except:
        print('q3')
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'add_group')
def callback(call):
    set_state(call.message.chat.id, 'add_group')
    cid = call.message.chat.id
    mid = call.message.message_id

    set_message_id(cid, mid)

    try:
        bot.edit_message_text(texts['add_group'], cid, mid,
                              reply_markup=keyboards.kb_add_group)
    except:
        print('q4')
        pass


@bot.message_handler(func=lambda message: get_state(message.chat.id) == 'add_group')
def menu(message):
    bot.delete_message(message.chat.id, message.message_id)
    cid = message.chat.id
    mid = get_message_id(cid)

    set_state   (message.chat.id, 'add_group_1')

    id = 0

    try:
        print(message.text.split('/')[-1])
        added = False
        group = vk_session.vk_session.method('groups.getById', {'group_ids': message.text.split('/')[-1]})[0]
        id = group['id']
        print(group)
        if group['name'] == '':
            if len(message.text.split('/')[-1]) > 6 and message.text.split('/')[-1][:6] == 'public':
                print(message.text.split('/')[-1][6:])
                group = vk_session.vk_session.method('groups.getById', {'group_ids': message.text.split('/')[-1][6:]})[0]
                id = group['id']
                if group['name'] != '' and 'deactivated' not in group.keys(): #и если не забанена
                    added = True
        else:
            if 'deactivated' not in group.keys():
                added = True #проверка на удаленную группу

        if added:
            add_group(message.chat.id, str(id))
            bot.edit_message_text(texts['ok'], cid, mid,
                                  reply_markup=keyboards.kb_add_group)
        else:
            bot.edit_message_text(texts['error'], cid, mid,
                                  reply_markup=keyboards.kb_add_group)
    except Exception as e:
        try:
            if len(message.text.split('/')[-1]) > 6 and message.text.split('/')[-1][:6] == 'public':
                print(message.text.split('/')[-1][6:])
                group = vk_session.vk_session.method('groups.getById', {'group_ids': message.text.split('/')[-1][6:]})[0]
                id = group['id']
                if group['name'] != '' and 'deactivated' not in group.keys():  # и если не забанена
                    add_group(message.chat.id, str(id))
                    bot.edit_message_text(texts['ok'], cid, mid,
                                          reply_markup=keyboards.kb_add_group)
            else:
                bot.edit_message_text(texts['error'], cid, mid,
                                      reply_markup=keyboards.kb_add_group)
        except:
            print(e)
            bot.edit_message_text(texts['error'], cid, mid,
                                  reply_markup=keyboards.kb_add_group)


@bot.callback_query_handler(func=lambda call: call.data[0:3] == 'del')
def callback(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    try:
        delete_group(cid, call.data[3:])
        print(get_groups(call.message.chat.id))
        bot.edit_message_text(texts['groups'], cid, mid,
                              reply_markup=keyboards.make_groups_keyboard(get_groups(call.message.chat.id)))
    except Exception as e:
        print('q6 ', e)
        pass


bot.polling()