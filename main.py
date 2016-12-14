#!/usr/bin/env python3
#-*- coding: utf-8 -*-

### Filename: main.py
## Created by 请叫我喵 Alynx
# sxshax@gmail.com, http://alynx.xyz/

import time
import random

x = 1000

class Fighter(object):
    global x
    def __init__(self, name, enemy_name):
        self.NAME = name
        self.ENEMY = enemy_name
        self.nums = {
            "HP": int(random.random() * x),
            "ATK": int(random.random() * x),
            "DEF": int(random.random() * x),
            "SPD": int(random.random() * x),
            "CHE": int(random.random() * x),
            "ACC": int(random.random() * x),
        }

    def print_item(self):
        print("%s 的数据："%(self.NAME))
        print(" +------------+------------+------------+")
        print(" | 体力：%4d |"%(self.nums["HP"]), end='')
        print(" 攻击：%4d |"%(self.nums["ATK"]), end='')
        print(" 防御：%4d |"%(self.nums["DEF"]), end='\n')
        print(" +------------+------------+------------+")
        print(" | 速度：%4d |"%(self.nums["SPD"]), end='')
        print(" 运气：%4d |"%(self.nums["CHE"]), end='')
        print(" 命中：%4d |"%(self.nums["ACC"]), end='\n')
        print(" +------------+------------+------------+")

    def hurt(self, case, number):
        self.nums[case] -= number

    def bite(self, number):
        print("%s 发狂了，上前咬了 %s 一口，造成了 %d 点伤害。"%(self.NAME, self.ENEMY, number))
        num = number
        return num

    def angry(self, number):
        number1 = number * random.random()
        number2 = number * random.random()
        print("%s 发怒了，把 %s 按在地上一顿爆打，%s 受到了 %d 点伤害，\n%s 受到了 %d 点伤害，%s 受到了 %d 点伤害，%s 挣脱了。"%(self.NAME, self.ENEMY, self.ENEMY, number, self.ENEMY, number1, self.ENEMY, number2, self.ENEMY))
        num = number + number1 + number2
        return num

    def attrack(self, number):
        print("%s 向 %s 发起了攻击，%s 受到了 %d 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, number))
        num = number
        return num

    def fall(self, number):
        if random.random() >= 0.5:
            print("%s 向 %s 发起攻击，但是被 %s 绊倒了，%s 受到了 %d 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, self.NAME, number))
            num = number
        else:
            print("%s 向 %s 发起攻击，但是被 %s 躲开了。"%(self.NAME, self.ENEMY, self.ENEMY))
            num = 0
        return num

    def fight(self, kind, number):
        return {
            "bite": lambda x: self.bite(x),
            #"fall": lambda x, y: self.fall(x, y),
            "angry": lambda x: self.angry(x),
            "attrack": lambda x: self.attrack(x),
        }[kind](number)

def hurt(obj, enemy):
    num = int(abs(obj.nums["ATK"] - enemy.nums["DEF"]) * abs(obj.nums["CHE"] - enemy.nums["CHE"]) / 300)
    while num > 777:
        num = num - 777 * random.random()

    if obj.nums["ACC"] > random.random() * x:
        kind = random.choice(["bite", "angry", "attrack"])
        fin_hurt = obj.fight(kind, num)
        enemy.hurt("HP", fin_hurt)
    else:
        num = int(num * random.random() * 20 + 20)
        if num > 500:
            num = random.random() * 333
        obj.hurt("HP", obj.fall(num))


def main():
    plr1_name = input("输入第一个玩家的名字：")
    plr2_name = input("输入第二个玩家的名字：")
    plr1 = Fighter(plr1_name, plr2_name)
    plr2 = Fighter(plr2_name, plr1_name)
    while abs(plr1.nums["HP"] - plr2.nums["HP"]) > 233:
        if plr1.nums["HP"] < plr2.nums["HP"]:
            plr1.nums["HP"] += abs(plr1.nums["HP"] - plr2.nums["HP"]) * random.random()
        elif plr2.nums["HP"] < plr1.nums["HP"]:
            plr2.nums["HP"] += abs(plr1.nums["HP"] - plr2.nums["HP"]) * random.random()

    while (plr1.nums["HP"] > 0) and (plr2.nums["HP"] > 0):
        print("==============================================")
        time.sleep(1)
        plr1.print_item()
        plr2.print_item()
        print("==============================================")
        time.sleep(1)
        if plr1.nums["SPD"] > plr2.nums["SPD"]:
            hurt(plr1, plr2)
            if not (plr1.nums["HP"] > 0) and (plr2.nums["HP"] > 0):
                break
            time.sleep(0.5)
            print("----------------------------------------------")
            time.sleep(0.5)
            hurt(plr2, plr1)
            time.sleep(1)
        elif plr1.nums["SPD"] < plr2.nums["SPD"]:
            hurt(plr2, plr1)
            if not (plr1.nums["HP"] > 0) and (plr2.nums["HP"] > 0):
                break
            time.sleep(0.5)
            print("----------------------------------------------")
            time.sleep(0.5)
            hurt(plr1, plr2)

    print("==============================================")
    if plr1.nums["HP"] <= 0:
        print("%s 输了，获胜者是 %s。"%(plr1_name, plr2_name))
    elif plr2.nums["HP"] <= 0:
        print("%s 输了，获胜者是 %s。"%(plr2_name, plr1_name))

if __name__ == "__main__":
    main()
