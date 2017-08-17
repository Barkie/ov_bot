# -*- coding: utf-8 -*-

import logging



logging_mode = logging.DEBUG
log = logging.getLogger('OV_BOT')
log.setLevel(logging_mode)
fh = logging.FileHandler('/home/admin/all_bot_log.txt')
fh.setLevel(logging_mode)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(name)3s][%(levelname)s][%(message)s]')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
log.addHandler(fh)
log.addHandler(ch)
if logging_mode == 10:
    log.info('Current log mode is DEBUG --> file, INFO --> console')
elif logging_mode == 20:
    log.info('Current log mode is INFO --> file, INFO --> console')
else:
    pass
