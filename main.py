#!/usr/bin/env python3
#-*- coding: utf-8 -*-

### Filename: main.py
## Created by 请叫我喵 Alynx
# sxshax@gmail.com, http://alynx.xyz/

import time
import random
import hashlib
import argparse

aparser = argparse.ArgumentParser(description="输入两个名字，让它们来决斗吧！")
aparser.add_argument("name1", nargs='?', help="第一个名字。", action="store")
aparser.add_argument("name2", nargs='?', help="第二个名字。", action="store")
args = aparser.parse_args()

class Fighter(object):
    #global x
    def __init__(self, name, enemy_name):
        self.NAME = name
        self.ENEMY = enemy_name
        self.md5 = hashlib.md5(name.encode("UTF-8")).hexdigest()
        self.nums = {
            "HP": int(self.md5[0:7:3], base=16) / 3,
            "ATK": int(self.md5[7:12:3], base=16),
            "DEF": int(self.md5[12:17:3], base=16),
            "SPD": int(self.md5[17:22:3], base=16),
            "CHE": int(self.md5[22:27:3], base=16),
            "ACC": int(self.md5[27:32:3], base=16)
        }
        self.enemy_nums = {}

    def spawn_num(self, mmin, mmax):
        if mmin > mmax and mmax:
            mmin %= mmax
            return random.randint(int(mmin), int(mmax))
        elif mmin <= mmax and mmax:
            return random.randint(int(mmin), int(mmax))
        elif mmax == 0:
            return 0

    def print_item(self, enemy):
        self.enemy_nums = enemy.nums
        print("%s 的数据："%(self.NAME))
        print("    +------------+------------+------------+")
        print("    | 体力：%4d |"%(self.nums["HP"]), end='')
        print(" 攻击：%4d |"%(self.nums["ATK"]), end='')
        print(" 防御：%4d |"%(self.nums["DEF"]), end='\n')
        print("    +------------+------------+------------+")
        print("    | 速度：%4d |"%(self.nums["SPD"]), end='')
        print(" 运气：%4d |"%(self.nums["CHE"]), end='')
        print(" 命中：%4d |"%(self.nums["ACC"]), end='\n')
        print("    +------------+------------+------------+")

    def hurt(self, case_num):
        for x, y in case_num.items():
            try:
                self.nums[x] -= y
            except:
                pass

    def bite(self, number):
        number += self.spawn_num(1, 0.7 * number)
        print("%s 发狂了，上前咬了 %s 一口，造成了 %d 点伤害。"%(self.NAME, self.ENEMY, number))
        num = number
        case_num = {"HP": num}
        return case_num

    def sleep(self, number):
        print("%s 给 %s 唱了安眠曲，%s 睡着了，%s 趁机恢复了 %d 点体力。"%(self.NAME, self.ENEMY, self.ENEMY, self.NAME, number))
        num = - number
        case_num = {"HP": num}
        return case_num

    def curse(self, number):
        print("%s 诅咒了 %s，%s 的各项数值下降了。"%(self.NAME, self.ENEMY, self.ENEMY))
        num = number
        case_num = {
            "ATK": self.spawn_num(num, self.enemy_nums["ATK"]),
            "DEF": self.spawn_num(num, self.enemy_nums["DEF"]),
            "SPD": self.spawn_num(num, self.enemy_nums["SPD"]),
            "CHE": self.spawn_num(num, self.enemy_nums["CHE"]),
            "ACC": self.spawn_num(num, self.enemy_nums["ACC"])
        }
        return case_num

    def pray(self, number):
        print("%s 向上天祈祷，%s 的各项数值上升了。"%(self.NAME, self.NAME))
        num = number
        case_num = {
            "ATK": - self.spawn_num(num, self.nums["ATK"] * 3 / 2),
            "DEF": - self.spawn_num(num, self.nums["DEF"] * 3 / 2),
            "SPD": - self.spawn_num(num, self.nums["SPD"] * 3 / 2),
            "CHE": - self.spawn_num(num, self.nums["CHE"] * 3 / 2),
            "ACC": - self.spawn_num(num, self.nums["ACC"] * 3 / 2)
        }
        return case_num

    def angry(self, number):
        number1 = self.spawn_num(1, 0.6 * number)
        number2 = self.spawn_num(1, 0.3 * number)
        print("%s 发怒了，把 %s 按在地上一顿暴打，%s 受到了 %d 点伤害，\n%s 受到了 %d 点伤害，%s 受到了 %d 点伤害，%s 挣脱了。"%(self.NAME, self.ENEMY, self.ENEMY, number, self.ENEMY, number1, self.ENEMY, number2, self.ENEMY))
        num = number + number1 + number2
        case_num = {"HP": num}
        return case_num

    def attrack(self, number):
        print("%s 向 %s 发起了攻击，%s 受到了 %d 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, number))
        num = number
        case_num = {"HP": num}
        return case_num


    def fall(self, number):
        print("%s 向 %s 发起攻击，但是被 %s 绊倒了，%s 受到了 %d 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, self.NAME, number))
        num = number
        case_num = {"HP": num}
        return case_num

    def miss(self, number):
        print("%s 向 %s 发起攻击，但是被 %s 躲开了。"%(self.NAME, self.ENEMY, self.ENEMY))
        num = 0
        case_num = {"HP": num}
        return case_num

    def fight(self, kind, number):
        return {
            "bite": lambda x: self.bite(x),
            "miss": lambda x: self.miss(x),
            "fall": lambda x: self.fall(x),
            "pray": lambda x: self.pray(x),
            "angry": lambda x: self.angry(x),
            "curse": lambda x: self.curse(x),
            "attrack": lambda x: self.attrack(x),
            "sleep": lambda x: self.sleep(x)
        }[kind](number)

def hurt(obj, enemy, hp_limit):
    num = obj.spawn_num(
        abs(
            abs(
                obj.nums["ATK"] - enemy.nums["DEF"]
            ) * abs(
                obj.nums["CHE"] - enemy.nums["CHE"]
            ) - abs(
                obj.nums["ATK"]
            ) * random.random()
        ),
        hp_limit
    )

    if obj.nums["ACC"] > int((obj.nums["ACC"] + enemy.nums["ACC"]) * random.random()):
        fight_way = random.choice(["bite", "angry", "attrack", "sleep", "curse", "pray"])
        if not fight_way in ["sleep", "pray"]:
            enemy.hurt(obj.fight(fight_way, num))
        else:
            obj.hurt(obj.fight(fight_way, num))
    else:
        num = int(num * random.random())
        if obj.nums["CHE"] > int((obj.nums["CHE"] + enemy.nums["CHE"]) * random.random()):
            fight_way = "miss"
        else:
            fight_way = "fall"
        obj.hurt(obj.fight(fight_way, num))


def main():
    if args.name1 == None:
        plr1_name = input("输入第一个玩家的名字：")
    else:
        plr1_name = args.name1
    if args.name2 == None:
        plr2_name = input("输入第二个玩家的名字：")
    else:
        plr2_name = args.name2

    if plr1_name == "日耳曼战神" or plr2_name == "日耳曼战神":
        print("做梦吧你，日耳曼战神永远是最强的，想打赢战神？不可能！")
        exit()
    plr1 = Fighter(plr1_name, plr2_name)
    plr2 = Fighter(plr2_name, plr1_name)

    while abs(plr1.nums["HP"] - plr2.nums["HP"]) > 233:
        if plr1.nums["HP"] < plr2.nums["HP"]:
            plr1.nums["HP"] += abs(plr1.nums["HP"] - plr2.nums["HP"]) * random.random()
        elif plr2.nums["HP"] < plr1.nums["HP"]:
            plr2.nums["HP"] += abs(plr1.nums["HP"] - plr2.nums["HP"]) * random.random()

    hp_limit = int(abs(plr1.nums["HP"] + plr2.nums["HP"]) / 2 * 0.5)

    while ((plr1.nums["HP"] > 0) and (plr2.nums["HP"] > 0)):
        if plr1.nums["SPD"] > plr2.nums["SPD"]:
            print("================================================")
            time.sleep(0.5)
            plr1.print_item(plr2)
            plr2.print_item(plr1)
            print("================================================")
            time.sleep(0.5)
            hurt(plr1, plr2, hp_limit)
            if not ((plr1.nums["HP"] > 0) and (plr2.nums["HP"] > 0)):
                break
            time.sleep(0.5)
            print("------------------------------------------------")
            time.sleep(0.5)
            hurt(plr2, plr1, hp_limit)
        elif plr1.nums["SPD"] <= plr2.nums["SPD"]:
            print("================================================")
            time.sleep(0.5)
            plr2.print_item(plr1)
            plr1.print_item(plr2)
            print("================================================")
            time.sleep(0.5)
            hurt(plr2, plr1, hp_limit)
            if not ((plr1.nums["HP"] > 0) and (plr2.nums["HP"] > 0)):
                break
            time.sleep(0.5)
            print("------------------------------------------------")
            time.sleep(0.5)
            hurt(plr1, plr2, hp_limit)

    print("================================================")
    if plr1.nums["HP"] <= 0:
        print("%s 输了，获胜者是 %s。"%(plr1_name, plr2_name))
    elif plr2.nums["HP"] <= 0:
        print("%s 输了，获胜者是 %s。"%(plr2_name, plr1_name))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n', end='')
        exit()
