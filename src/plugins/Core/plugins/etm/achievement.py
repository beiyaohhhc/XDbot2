from .. import _messenger
from . import economy
from . import exp
import json
import time
from . import data

ACHIEVEMENTS = {
    "什么欧皇": {
        "name": "什么欧皇",
        "condition": "在二十面骰子中获得 10 个「大失败」",
        "need_progress": 10,
        "award": {
            "vi": 5,
            "exp": 3
        }
    },
    "特性！特性": {
        "name": "特性！特性",
        "condition": "在二十面骰子中掷出 -1",
        "need_progress": 1,
        "award": {
            "vi": 5,
            "exp": 6
        }
    },
    "+0！": {
        "name": "+0！",
        "condition": "在每日签到中获得0vi",
        "need_progress": 1,
        "award": {
            "vi": 10,
            "exp": 12
        }
    },
    "我爱数学": {
        "name": "我爱数学",
        "condition": "在速算中正确完成15次",
        "need_progress": 15,
        "award": {
            "vi": 12,
            "exp": 15
        }
    }
}


def get_user_achievement(user_id):
    try:
        return data.achi_user_data[user_id]
    except KeyError:
        return []


def change_user_achievement(user_id, _data):
    data.achi_user_data[user_id] = _data


def unlck(name, user_id):
    user_achievement = get_user_achievement(user_id)
    if name in ACHIEVEMENTS.keys() and name not in user_achievement:
        user_achievement.append(name)
        economy.add_vi(user_id, ACHIEVEMENTS[name]["award"]["vi"])
        exp.add_exp(user_id, ACHIEVEMENTS[name]["award"]["exp"])
        change_user_achievement(user_id, user_achievement)
        _messenger.send_message((
            f"成就已解锁：{ACHIEVEMENTS[name]['name']}\n"
            f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"),
            receive=user_id)


def get_unlck_progress(name, user_id):
    user_data = data.achi_unlock_progress
    try:
        return user_data[user_id][name]
    except KeyError:
        return None


def increase_unlock_progress(name, user_id, count=1):
    try:
        data.achi_unlock_progress[user_id][name] += count
    except KeyError:
        try:
            data.achi_unlock_progress[user_id][name] = count
        except KeyError:
            data.achi_unlock_progress[user_id] = {name: count}
    if data.achi_unlock_progress[user_id][name] >= ACHIEVEMENTS[name]["need_progress"]:
        unlck(name, user_id)
