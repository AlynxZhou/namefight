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
    def __init__(self, name, enemy_name):
        self.NAME = name
        self.ENEMY = enemy_name
        self.md5 = hashlib.md5(name.encode("UTF-8")).hexdigest()
        self.numbers = {
            "HP": self.md5_count(self.md5, 0, 7) * 20,
            "ATK": self.md5_count(self.md5, 7, 5) * 10,
            "DEF": self.md5_count(self.md5, 12, 5) * 10,
            "SPD": self.md5_count(self.md5, 17, 5) * 10,
            "CHE": self.md5_count(self.md5, 22, 5) * 10,
            "ACC": self.md5_count(self.md5, 27, 5) * 10
        }
        self.enemy = None

    def md5_count(self, md5, start, lenth, step=1):
        summ = 0
        for x in md5[start:start + lenth:step]:
            summ += int(x, base=16)
        return int(summ)

    def spawn_number(self, mmin, mmax):
        if mmin > mmax and mmax:
            mmin %= mmax
            return random.randint(int(mmin), int(mmax))
        elif mmin <= mmax and mmax:
            return random.randint(int(mmin), int(mmax))
        elif mmax == 0:
            return 0

    def get_enemy(self, enemy):
        self.enemy = enemy

    def print_item(self):
        print("%s 的数据："%(self.NAME))
        print("    ++============+============+============++")
        print("    || 体力：%4d | 攻击：%4d | 防御：%4d ||"%(self.numbers["HP"], self.numbers["ATK"], self.numbers["DEF"]))
        print("    ++------------+------------+------------++")
        print("    || 速度：%4d | 运气：%4d | 命中：%4d ||"%(self.numbers["SPD"], self.numbers["CHE"], self.numbers["ACC"]))
        print("    ++============+============+============++")

    def hurt(self, case_number):
        for x, y in case_number.items():
            try:
                self.numbers[x] -= y
            except:
                pass

    def bite(self, number):
        number1 = self.spawn_number(1, 0.7 * number)
        number += number1
        print("%s 发狂了，上前咬了 %s 一口，\n造成了 \033[31;1m%d\033[0m 点伤害，自己受到反噬的 %d 点伤害。"%(self.NAME, self.ENEMY, number, number1))
        case_number = {"HP": number}
        self.enemy.hurt(case_number)
        case_number = {"HP": number1}
        self.hurt(case_number)

    def sleep(self, number):
        print("%s 给 %s 唱了安眠曲，%s 睡着了，\n%s 趁机恢复了 \033[31;1m%d\033[0m 点体力。"%(self.NAME, self.ENEMY, self.ENEMY, self.NAME, number))
        number = - number
        case_number = {"HP": number}
        self.hurt(case_number)

    def curse(self, number):
        print("%s 诅咒了 %s，%s 的各项数值下降了。"%(self.NAME, self.ENEMY, self.ENEMY))
        case_number = {
            "ATK": self.spawn_number(number, self.enemy.numbers["ATK"]),
            "DEF": self.spawn_number(number, self.enemy.numbers["DEF"]),
            "SPD": self.spawn_number(number, self.enemy.numbers["SPD"]),
            "CHE": self.spawn_number(number, self.enemy.numbers["CHE"]),
            "ACC": self.spawn_number(number, self.enemy.numbers["ACC"])
        }
        self.enemy.hurt(case_number)

    def pray(self, number):
        print("%s 向上天祈祷，%s 的各项数值上升了。"%(self.NAME, self.NAME))
        case_number = {
            "ATK": - self.spawn_number(number, self.numbers["ATK"] * 3 / 2),
            "DEF": - self.spawn_number(number, self.numbers["DEF"] * 3 / 2),
            "SPD": - self.spawn_number(number, self.numbers["SPD"] * 3 / 2),
            "CHE": - self.spawn_number(number, self.numbers["CHE"] * 3 / 2),
            "ACC": - self.spawn_number(number, self.numbers["ACC"] * 3 / 2)
        }
        self.hurt(case_number)

    def angry(self, number):
        number1 = self.spawn_number(1, 0.6 * number)
        number2 = self.spawn_number(1, 0.3 * number)
        print("%s 发怒了，把 %s 按在地上一顿暴打，\n%s 受到了 \033[31;1m%d\033[0m 点伤害，%s 受到了 \033[31;1m%d\033[0m 点伤害，\n%s 受到了 \033[31;1m%d\033[0m 点伤害，%s 挣脱了。"%(self.NAME, self.ENEMY, self.ENEMY, number, self.ENEMY, number1, self.ENEMY, number2, self.ENEMY))
        number = number + number1 + number2
        case_number = {"HP": number}
        self.enemy.hurt(case_number)

    def attrack(self, number):
        print("%s 向 %s 发起了攻击，%s 受到了 \033[31;1m%d\033[0m 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, number))
        case_number = {"HP": number}
        self.enemy.hurt(case_number)

    def fall(self, number):
        number = self.spawn_number(1, 0.7 * number)
        print("%s 向 %s 发起攻击，但是被 %s 绊倒了，\n%s 受到了 \033[31;1m%d\033[0m 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, self.NAME, number))
        case_number = {"HP": number}
        self.hurt(case_number)

    def miss(self, number):
        print("%s 向 %s 发起攻击，但是被 %s 躲开了。"%(self.NAME, self.ENEMY, self.ENEMY))

    def fight(self, hp_limit):
        number = self.spawn_number(
            abs(
                abs(
                    self.numbers["ATK"] - self.enemy.numbers["DEF"]
                ) * abs(
                    self.numbers["CHE"] - self.enemy.numbers["CHE"]
                ) - abs(
                    self.numbers["ATK"]
                ) * random.random()
            ),
            hp_limit
        )

        if self.numbers["ACC"] > int((self.numbers["ACC"] + self.enemy.numbers["ACC"]) * random.random()):
            case = random.choice(["bite", "angry", "attrack", "sleep", "curse", "pray"])
        else:
            number = int(number * random.random())
            if self.numbers["CHE"] > int((self.numbers["CHE"] + self.enemy.numbers["CHE"]) * random.random()):
                case = "miss"
            else:
                case = "fall"

        {
            "bite": lambda x: self.bite(x),
            "miss": lambda x: self.miss(x),
            "fall": lambda x: self.fall(x),
            "pray": lambda x: self.pray(x),
            "angry": lambda x: self.angry(x),
            "curse": lambda x: self.curse(x),
            "attrack": lambda x: self.attrack(x),
            "sleep": lambda x: self.sleep(x)
        }[case](number)


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

    plr1_name = "\033[34;1m" + plr1_name + "\033[0m"
    plr2_name = "\033[33;1m" + plr2_name + "\033[0m"

    plr1 = Fighter(plr1_name, plr2_name)
    plr2 = Fighter(plr2_name, plr1_name)

    plr1.get_enemy(plr2)
    plr2.get_enemy(plr1)

    while abs(plr1.numbers["HP"] - plr2.numbers["HP"]) > 233:
        if plr1.numbers["HP"] < plr2.numbers["HP"]:
            plr1.numbers["HP"] += abs(plr1.numbers["HP"] - plr2.numbers["HP"]) * random.random()
        elif plr2.numbers["HP"] < plr1.numbers["HP"]:
            plr2.numbers["HP"] += abs(plr1.numbers["HP"] - plr2.numbers["HP"]) * random.random()

    hp_limit = int(abs(plr1.numbers["HP"] + plr2.numbers["HP"]) / 2 * 0.5)

    while ((plr1.numbers["HP"] > 0) and (plr2.numbers["HP"] > 0)):
        if plr1.numbers["SPD"] >= plr2.numbers["SPD"]:
            print("================================================")
            plr1.print_item()
            plr2.print_item()
            print("================================================")
            time.sleep(0.5)
            plr1.fight(hp_limit)
            if not ((plr1.numbers["HP"] > 0) and (plr2.numbers["HP"] > 0)):
                time.sleep(0.5)
                print("================================================")
                time.sleep(0.5)
                break
            time.sleep(0.5)
            print("------------------------------------------------")
            time.sleep(0.5)
            plr2.fight(hp_limit)

        elif plr1.numbers["SPD"] < plr2.numbers["SPD"]:
            print("================================================")
            plr2.print_item()
            plr1.print_item()
            print("================================================")
            time.sleep(0.5)
            plr2.fight(hp_limit)
            if not ((plr1.numbers["HP"] > 0) and (plr2.numbers["HP"] > 0)):
                time.sleep(0.5)
                print("================================================")
                time.sleep(0.5)
                break
            time.sleep(0.5)
            print("------------------------------------------------")
            time.sleep(0.5)
            plr1.fight(hp_limit)

        time.sleep(0.5)
        print("================================================")
        time.sleep(0.5)

    print("================================================")

    if plr1.numbers["HP"] <= 0 and plr2.numbers["HP"] <= 0:
        if plr1.numbers["SPD"] >= plr2.numbers["SPD"]:
            plr1.print_item()
            plr2.print_item()
        elif plr1.numbers["SPD"] < plr2.numbers["SPD"]:
            plr2.print_item()
            plr1.print_item()
        print("================================================")
        time.sleep(0.5)
        print("%s 和 %s 棋逢对手，两败俱伤。"%(plr1_name, plr2_name))
        time.sleep(0.5)
        print("================================================")
    elif plr1.numbers["HP"] <= 0 and plr2.numbers["HP"] > 0:
        if plr1.numbers["SPD"] >= plr2.numbers["SPD"]:
            plr1.print_item()
            plr2.print_item()
        elif plr1.numbers["SPD"] < plr2.numbers["SPD"]:
            plr2.print_item()
            plr1.print_item()
        print("================================================")
        time.sleep(0.5)
        print("%s 输了，获胜者是 %s。"%(plr1_name, plr2_name))
        time.sleep(0.5)
        print("================================================")
    elif plr1.numbers["HP"] > 0 and plr2.numbers["HP"] <= 0:
        if plr1.numbers["SPD"] >= plr2.numbers["SPD"]:
            plr1.print_item()
            plr2.print_item()
        elif plr1.numbers["SPD"] < plr2.numbers["SPD"]:
            plr2.print_item()
            plr1.print_item()
        print("================================================")
        time.sleep(0.5)
        print("%s 输了，获胜者是 %s。"%(plr2_name, plr1_name))
        time.sleep(0.5)
        print("================================================")

    exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n', end='')
        exit()
