# -*- coding: utf-8 -*-
#!/usr/bin/python3

import telebot
import ovconfig
import os
import time
import requests
import re
import json
import overwatch.stats
from over_logger import *

bot = telebot.TeleBot(ovconfig.tgtoken)


def rankings(rating):
    log.debug
    if rating < 1499:
        tier = 'Bronze'
    elif 1500 <= rating < 1999:
        tier = 'Silver'
    elif 2000 <= rating < 2499:
        tier = 'Gold'
    elif 2500 <= rating < 2999:
        tier = 'Platinum'
    elif 3000 <= rating < 3499:
        tier = 'Diamond'
    elif 3500 <= rating < 3999:
        tier = 'Master'
    elif rating >= 4000:
        tier = 'Grandmaster'

    return tier + ' tier'


def search_stats(btag):
    try:
        stats = overwatch.stats.query('pc', 'eu', str(btag))
        if stats:
            rating = stats['competitive_rank']
            tier = rankings(rating)
            answer = 'Current competitive rating \
for player {} is :\n{}, {}'.format(
                btag, str(rating), tier)
    except ValueError as e:       
        answer = 'Error. Cannot find the player {}'.format(btag)
        log.debug('ValueError, {}'.format(answer))
    except KeyError as e:
        answer = 'Current competitive rating for player {} is: Unranked.'.format(btag)
        log.debug('KeyError, {}'.format(answer))
    except Exception as e:
        answer = 'Error processing {}. Contact administrator to check logs\nRAW error message for debug: {}'.format(btag, e)
        log.error('EXCEPTION! {}'.format(answer))
    return answer


@bot.message_handler(commands=['start'])
def start(message):

    """
    The first command
    """
    log.info('Start command pushed from \
        user @{}').format(message.chat.username)
    bot.send_message(message.chat.id, '''
    This bot shows current competitive rank for a user.\n
    Just tell me a battle tag, I'll tell you rating.\n
    Currently working only for PC platform and EU region.
    ''')


@bot.message_handler(commands=['help'])
def start(message):

    """
    The help command
    """
    log.info('Help  command pushed from \
        @{}'.format(message.chat.username))
    bot.send_message(message.chat.id, '''
    For any additional info contact @Barkie
    ''')


@bot.message_handler(commands=['friends_ratings'])
def friends_ratings(message):

    """
    friends_ratings_table
    """
    # user = (message.chat.username, message.chat.id)
    # if user != ('Barkie', 3314252):
    #     answer = 'Sorry, ' + str(message.chat.username) + ', access denied for you. Bot in debug stage now.'
    #     bot.send_message(message.chat.id, answer)
    # else:
    log.info('Friends_rating command pushed from @{}'.format(message.chat.username))
    member_list = []
    try:
        log.debug('Trying to import friend list from file')
        from elabuzhane import elabuzhane
        log.debug('Friend list imported')
        for key in elabuzhane:
            member_list.append(key)
        pre_answer = 'Ok, gotcha.\nSearching ratings for players: {}'.format(
            ' '.join(sorted(member_list)))
        log.debug('Current member_list variable: {}'.format(
                member_list))
    except Exception as e:
        pre_answer = 'Cannot access players list. \
        Contact administrator to check logs'
        log.error('Some error happens \
            in importing and sorting friend list. Current \
            member_list variable: {}'.format(member_list))
    log.debug('Sending member_list for the user')
    bot.send_message(message.chat.id, pre_answer)
    rating_list = []
    for key in elabuzhane:
        log.debug('Trying to query stats from blizzard')
        log.info('Processing {} key in elabuzhane'.format(key))
        try:
            stats = overwatch.stats.query('pc', 'eu', str(elabuzhane[key]))
            if stats:
                log.debug('Stats gathered. Trying to get competitive_rank')
                rating = stats['competitive_rank']
                tier = rankings(rating)
                append_list = (
                    key, elabuzhane[key], str(rating), tier)
                rating_list.append(append_list)
                log.info('Data searched. Rating for key {}: {}, Tier: {}'.format(
                    key, str(rating), tier))
            else:
                log.error('Stats have not gathered.')
        except KeyError as e:
            log.info('Data searched. No rating for key {}'.format(
                key))
            append_list = (
                key, elabuzhane[key], '0 = No rating', 'Dno tier')
            rating_list.append(append_list)
        except Exception as e:
            log.error('Exception happens. RAW text for debug: {}'.format(e))
            append_list = (
                key, elabuzhane[key], 'Error', 'Error')
            rating_list.append(append_list)
    sorted_by_rating = sorted(rating_list, key=lambda tup: tup[2], reverse=True)
    answer = ''
    for item in sorted_by_rating:
        answer = answer + 'Current competitive rating for player {} ({}) is:\n{}, {}\n\n'.format(
            item[0], item[1], item[2], item[3])
    bot.send_message(message.chat.id, answer)
    log.info('Answer sended')


@bot.message_handler(regexp=".*?#\d{4,5}")
def btag_searcher(message):
    pre_answer = 'Ok, gotcha\nProcessing rating search for player {}'.format(
        message.text)
    bot.send_message(message.chat.id, pre_answer)
    try:
        # user = (message.chat.username, message.chat.id)
        # log.info('User {} pushed {} btag'.format(
        #     message.chat.username, message.text))
        # if user != ('Barkie', 3314252):
        #     answer = 'Sorry, ' + str(message.chat.username) + ', access denied for you. Bot in debug stage now'
        #     bot.send_message(message.chat.id, answer)
        # else:
        answer = search_stats(str(message.text))
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        answer = 'Unknown exception happens in btag_search. RAW text for debug: {}'.format(e)
        log.error('ERROR! {}'.format(answer))
        bot.send_message(message.chat.id, answer)

if __name__ == '__main__':
    bot.polling(none_stop=True)
