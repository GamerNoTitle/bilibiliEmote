import requests as r
from tqdm import tqdm
import os
import sys
import json
import logging

welcome = r'''______ _ _ _        _____                _        ______                    _                 _           
| ___ (_) (_)      |  ___|              | |       |  _  \                  | |               | |          
| |_/ /_| |_ ______| |__ _ __ ___   ___ | |_ ___  | | | |_____      ___ __ | | ___   __ _  __| | ___ _ __ 
| ___ \ | | |______|  __| '_ ` _ \ / _ \| __/ _ \ | | | / _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
| |_/ / | | |      | |__| | | | | | (_) | ||  __/ | |/ / (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
\____/|_|_|_|      \____/_| |_| |_|\___/ \__\___| |___/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   

                                                                         -------- GamerNoTitle      
                                                                                                          '''
print(welcome)

def logger(log_level, log_file):
    logger = logging.getLogger()
    logger.setLevel(log_level)
    BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
    console = logging.StreamHandler() # 输出到控制台的handler
    console.setFormatter(formatter)
    console.setLevel(log_level)  # 也可以不设置，不设置就默认用logger的level
    file = logging.FileHandler(log_file, encoding='utf-8') # 输出到文件的handler
    file.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(file)
    return logger

log = logger('DEBUG', 'log.log')

try:
    sessdata = sys.argv[1]
    print(sessdata)
    os.mkdir('Emote')
except FileExistsError:
    pass
except IndexError:
    print(sys.argv)
panel = 'http://api.bilibili.com/x/emote/setting/panel?business=dynamic'
panelInformation = json.loads(r.get(
    panel, headers={'cookie': f'SESSDATA={sessdata}'}).text)
allPackages = panelInformation['data']['all_packages']
for package in allPackages:
    packageName = package['text']
    emotelist = package['emote']
    if packageName == '颜文字' or packageName == '小黄脸': continue
    if not os.path.exists(f'./Emote/{packageName}'): os.mkdir(f'./Emote/{packageName}')
    with tqdm(total=len(emotelist), desc=f'Downloading {packageName}') as bar:
        for emote in emotelist:
            if not os.path.exists(f'./Emote/{packageName}/{emote["text"]}.png'):
                with open(f'./Emote/{packageName}/{emote["text"].replace("?", "？")}.png', 'wb') as f:
                    f.write(r.get(emote['url']).content)
            bar.update(1)
print('Done!')
