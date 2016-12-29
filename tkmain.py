#!/usr/bin/env python3
#-*- coding: utf-8 -*-

### Filename: main.py
## Created by 请叫我喵 Alynx
# sxshax@gmail.com, http://alynx.xyz/


import sys
import time
import random
import hashlib
import argparse

if sys.version_info.major < 3:
	import __future__

import tkinter
import tkinter.messagebox
import tkinter.scrolledtext

aparser = argparse.ArgumentParser(description="输入两个名字，让它们来决斗吧！")
aparser.add_argument("name1", nargs='?', help="第一个名字。", action="store")
aparser.add_argument("name2", nargs='?', help="第二个名字。", action="store")
args = aparser.parse_args()


class Fighter(object):
	"""
	主要的 Fighter 类，调用这个类生成两个战斗对象。
	"""
	def __init__(self, name, enemy_name, printer=print):
		"""
		初始化 Fighter 对象，name 为此对象名字，enemy_name 为敌对对象的名字。
		"""
		self.NAME = name
		self.ENEMY = enemy_name
		self.md5 = hashlib.md5(name.encode("UTF-8")).hexdigest()
		self.numbers = {
			"HP": self.md5_count(self.md5, 0, 7) * 20,	# 生命值。
			"ATK": self.md5_count(self.md5, 7, 5) * 10,	# 攻击力。
			"DEF": self.md5_count(self.md5, 12, 5) * 10,	# 防御力。
			"SPD": self.md5_count(self.md5, 17, 5) * 10,	# 速度。
			"LUK": self.md5_count(self.md5, 22, 5) * 10,	# 运气。
			"ACC": self.md5_count(self.md5, 27, 5) * 10	# 命中率。
		}	# 生成对象的各种战斗力数据。
		self.enemy = None	# 初始化一个内部敌人对象方便调用敌人的 hurt() 方法。
		self.printer = printer

	def md5_count(self, md5, start, lenth, step=1):
		"""
		将指定起点、长度、步长的 md5 字符串切片并计算为十进制整数数据。
		"""
		summ = 0
		for x in md5[start:start + lenth:step]:
			summ += int(x, base=16)
		return int(summ)

	def spawn_number(self, mmin, mmax):
		"""
		通过给定的最小值 mmin 和最大值 mmax，生成一个不大于最大值 mmax 的随机整数，拓展了 random 中求随机数的适用范围。
		如果最小值 mmin 过大，会自动对最大值 mmax 取模保证生成数字不会过大。
		"""
		if mmin > mmax and mmax:
			mmin %= mmax
			return random.randint(int(mmin), int(mmax))
		elif mmin <= mmax and mmax:
			return random.randint(int(mmin), int(mmax))
		elif mmax == 0:
			return 0

	def get_enemy(self, enemy):
		"""
		获取敌人对象建立内部链接。
		"""
		self.enemy = enemy

	def print_item(self):
		"""
		按指定格式输出战斗力数据。
		"""
		self.printer("%s 的数据："%(self.NAME))
		self.printer("	++===========+===========+===========++")
		self.printer("	|| 体力：%4d | 攻击：%4d | 防御：%4d ||"%(self.numbers["HP"], self.numbers["ATK"], self.numbers["DEF"]))
		self.printer("	++-----------+-----------+-----------++")
		self.printer("	|| 速度：%4d | 运气：%4d | 命中：%4d ||"%(self.numbers["SPD"], self.numbers["LUK"], self.numbers["ACC"]))
		self.printer("	++===========+===========+===========++")

	def check(self):
		"""
		检查内部数据是否超限。
		"""
		for x, y in self.numbers.items():
			if y > 9999:
				self.numbers[x] = 9999

	def hurt(self, case_number):
		"""
		进行实际的内部伤害处理，case_number 应为一个 {
			计算项1: 计算数据,
			计算项2: 计算数据
		} 的 dict，如果需要增加某项值请将计算数据设置为负数。
		"""
		for x, y in case_number.items():
			try:
				self.numbers[x] -= y
			except:
				pass

	def bite(self, number):
		"""
		狂咬攻击，伤害为传入基本数值的 1 到 1.7 倍。自己反噬超过传入值部分的多余伤害。
		"""
		number1 = self.spawn_number(1, 0.7 * number)
		number += number1
		self.printer("%s 发狂了，\n上前咬了 %s 一口，\n造成了 %d 点伤害，\n自己受到反噬的 %d 点伤害。"%(self.NAME, self.ENEMY, number, number1))
		case_number = {"HP": number}	# 构建 dict
		self.enemy.hurt(case_number)	# 调用敌人的 hurt() 方法以处理敌方数据
		case_number = {"HP": number1}
		self.hurt(case_number)	# 调用自己的 hurt() 方法来处理自身数据

	def sleep(self, number):
		"""
		催眠回血，恢复传入值大小的体力。
		"""
		self.printer("%s 给 %s 唱了安眠曲，\n%s 睡着了，\n%s 趁机恢复了 %d 点体力。"%(self.NAME, self.ENEMY, self.ENEMY, self.NAME, number))
		number = - number
		case_number = {"HP": number}
		self.hurt(case_number)

	def curse(self, number):
		"""
		诅咒，降低对方除体力外的的所有战斗力，降低的随机值不大于对方已有的值。
		"""
		self.printer("%s 诅咒了 %s，\n%s 的各项数值下降了。"%(self.NAME, self.ENEMY, self.ENEMY))
		case_number = {
			"ATK": self.spawn_number(number / 4, self.enemy.numbers["ATK"] * 0.7),
			"DEF": self.spawn_number(number / 4, self.enemy.numbers["DEF"] * 0.7),
			"SPD": self.spawn_number(number / 4, self.enemy.numbers["SPD"] * 0.7),
			"LUK": self.spawn_number(number / 4, self.enemy.numbers["LUK"] * 0.7),
			"ACC": self.spawn_number(number / 4, self.enemy.numbers["ACC"] * 0.7)
		}	# 构建含有多项数值的 dict
		self.enemy.hurt(case_number)

	def pray(self, number):
		"""
		祈祷，增加自己除体力外的所有战斗力，增加的随机值不大于自己以有的值的 1.5 倍。
		"""
		self.printer("%s 向上天祈祷，\n%s 的各项数值上升了。"%(self.NAME, self.NAME))
		case_number = {
			"ATK": - self.spawn_number(number / 3, self.numbers["ATK"] * 3 / 2),
			"DEF": - self.spawn_number(number / 3, self.numbers["DEF"] * 3 / 2),
			"SPD": - self.spawn_number(number / 3, self.numbers["SPD"] * 3 / 2),
			"LUK": - self.spawn_number(number / 3, self.numbers["LUK"] * 3 / 2),
			"ACC": - self.spawn_number(number / 3, self.numbers["ACC"] * 3 / 2)
		}
		self.hurt(case_number)

	def angry(self, number):
		"""
		愤怒的三连击，第二次连击攻击数值不大于传入值的 60%，第三次连击数值不大于传入值的 30%。
		"""
		number1 = self.spawn_number(1, 0.6 * number)
		number2 = self.spawn_number(1, 0.3 * number)
		self.printer("%s 发怒了，\n把 %s 按在地上一顿暴打，\n%s 受到了 %d 点伤害，\n%s 受到了 %d 点伤害，\n%s 受到了 %d 点伤害，\n%s 挣脱了。"%(self.NAME, self.ENEMY, self.ENEMY, number, self.ENEMY, number1, self.ENEMY, number2, self.ENEMY))
		number = number + number1 + number2
		case_number = {"HP": number}
		self.enemy.hurt(case_number)

	def attrack(self, number):
		"""
		普通攻击，给予对方传入值大小的伤害。
		"""
		self.printer("%s 向 %s 发起了攻击，\n%s 受到了 %d 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, number))
		case_number = {"HP": number}
		self.enemy.hurt(case_number)

	def fall(self, number):
		"""
		摔倒，随机发生在自己发起攻击，但命中率与运气值都较低的情况下，自己受到不大于传入值 50% 的伤害。
		"""
		number = self.spawn_number(1, 0.5 * number)
		self.printer("%s 向 %s 发起攻击，\n但是被 %s 绊倒了，\n%s 受到了 %d 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, self.NAME, number))
		case_number = {"HP": number}
		self.hurt(case_number)

	def miss(self, number):
		"""
		未击中，随机发生在自己发起攻击，但命中率较低而运气值又较高的情况下，双方均不承受伤害。
		"""
		self.printer("%s 向 %s 发起了攻击，\n但是被 %s 躲开了。"%(self.NAME, self.ENEMY, self.ENEMY))

	def fight(self, hp_limit):
		"""
		实际的战斗操作。通过 dict 与匿名函数实现 switch-case 结构。
		"""
		number = self.spawn_number(
			abs(
				abs(
					self.numbers["ATK"] - self.enemy.numbers["DEF"]
				) * abs(
					self.numbers["LUK"] - self.enemy.numbers["LUK"]
				) - self.numbers["ATK"] * random.random()
			),
			hp_limit
		)	# 利用攻方的攻击力及守方的防御力以及两方的运气，生成一个计算初始值，其保证不会一击致命。

		# 通过双方的命中率生成的随机值判断发起攻击成功还是失败。
		if self.numbers["ACC"] > int((self.numbers["ACC"] + self.enemy.numbers["ACC"]) * random.random()):
			case = random.choice(["bite", "angry", "attrack", "sleep", "curse", "pray"])	# 可以发起攻击时随机选择攻击方式。
		else:
			number = int(number * random.random())	# 攻击无法发起时减小计算值。
			# 判断运气值决定是否自己承受伤害。
			if self.numbers["LUK"] > int((self.numbers["LUK"] + self.enemy.numbers["LUK"]) * random.random()):
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
		}[case](number)	# 实际调用不同战斗操作。


class Monitor(Fighter):
	def __init__(self, name, enemy_name):
		super(Monitor, self).__init__(name, enemy_name)

	def sbite(self, number):
		"""
		班长的狂咬攻击，伤害为传入基本数值的 1 到 2.6 倍。自己反噬超过传入值部分的多余伤害。
		"""
		number1 = self.spawn_number(1, 0.9 * number)
		number2 = self.spawn_number(1, 0.7 * number)
		self.printer("%s 发现 %s 思修成绩不及格，发狂了，\n上前狂咬了 %s 一口，\n造成了 %d 点伤害，\n又上前狂咬了 %s 一口，\n造成了 %d 点伤害，\n又上前狂咬了 %s 一口，\n造成了 %d 点伤害，\n自己受到反噬的 %d 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, self.ENEMY, self.ENEMY, number, number1, number2))
		case_number = {"HP": number + number1 + number2}	# 构建 dict
		self.enemy.hurt(case_number)	# 调用敌人的 hurt() 方法以处理敌方数据
		case_number = {"HP": number1 + number2}
		self.hurt(case_number)	# 调用自己的 hurt() 方法来处理自身数据

	def fight(self, hp_limit):
		"""
		班长实际的战斗操作。通过 dict 与匿名函数实现 switch-case 结构。
		"""
		number = self.spawn_number(
			abs(
				abs(
					self.numbers["ATK"] - self.enemy.numbers["DEF"]
				) * abs(
					self.numbers["LUK"] - self.enemy.numbers["LUK"]
				) - self.numbers["ATK"] * random.random()
			),
			hp_limit
		)	# 利用攻方的攻击力及守方的防御力以及两方的运气，生成一个计算初始值，其保证不会一击致命。

		# 通过双方的命中率生成的随机值判断发起攻击成功还是失败。
		if self.numbers["ACC"] > int((self.numbers["ACC"] + self.enemy.numbers["ACC"]) * random.random()):
			case = random.choice(["sbite", "sbite", "sbite", "sbite", "sbite", "sbite", "sbite", "bite", "angry", "attrack", "sleep", "curse", "pray"])	# 可以发起攻击时随机选择攻击方式。
		else:
			number = int(number * random.random())	# 攻击无法发起时减小计算值。
			# 判断运气值决定是否自己承受伤害。
			if self.numbers["LUK"] > int((self.numbers["LUK"] + self.enemy.numbers["LUK"]) * random.random()):
				case = "miss"
			else:
				case = "fall"

		{
			"sbite": lambda x: self.bite(x),
			"bite": lambda x: self.bite(x),
			"miss": lambda x: self.miss(x),
			"fall": lambda x: self.fall(x),
			"pray": lambda x: self.pray(x),
			"angry": lambda x: self.angry(x),
			"curse": lambda x: self.curse(x),
			"attrack": lambda x: self.attrack(x),
			"sleep": lambda x: self.sleep(x)
		}[case](number)	# 实际调用不同战斗操作。



class Application(tkinter.Tk):
	def __init__(self, master=None):
		super(Application, self).__init__(master)
		self.title("Name Fight")
		# self.geometry("800x600")
		self.resizable(width=True, height=True)
		# TODO(请叫我喵 Alynx): Find a way to calculate the size of the window automatically via detecting the size of screen.
		self.create_input()
		self.create_text()

	def create_input(self):
		self.input_frame1 = tkinter.Frame(self)
		tkinter.Label(self.input_frame1, text="请输入第一个玩家的名字：").grid(row=0)
		self.name_input1 = tkinter.Entry(self.input_frame1)
		self.name_input1.grid(row=1)
		self.input_frame1.grid(row=0, column=0, pady=10)
		#self.name_input1.bind(sequence="<Enter>", func=self.callback)
		self.input_frame2 = tkinter.Frame(self)
		tkinter.Label(self.input_frame2, text="请输入第二个玩家的名字：").grid(row=0)
		self.name_input2 = tkinter.Entry(self.input_frame2)
		self.name_input2.grid(row=1)
		self.input_frame2.grid(row=0, column=2, pady=10)
		#self.name_input2.bind(sequence="<Enter>", func=self.callback)
		self.save_button = tkinter.Button(self, text="开始对战！", state="normal", command=self.callback)
		self.save_button.grid(row=0, column=1, pady=10)

	def create_data(self):
		self.plr1_frame = tkinter.Frame(self)
		tkinter.Label(self.plr1_frame, text=self.plr1_name).grid(row=0)
		tkinter.Label(self.plr1_frame, text="体力：%d"%(self.plr1.numbers["HP"])).grid(row=1)
		tkinter.Label(self.plr1_frame, text="攻击：%d"%(self.plr1.numbers["ATK"])).grid(row=2)
		tkinter.Label(self.plr1_frame, text="防御：%d"%(self.plr1.numbers["DEF"])).grid(row=3)
		tkinter.Label(self.plr1_frame, text="速度：%d"%(self.plr1.numbers["SPD"])).grid(row=4)
		tkinter.Label(self.plr1_frame, text="命中：%d"%(self.plr1.numbers["ACC"])).grid(row=5)
		tkinter.Label(self.plr1_frame, text="运气：%d"%(self.plr1.numbers["LUK"])).grid(row=6)
		self.plr1_frame.grid(row=1,column=0)
		self.plr2_frame = tkinter.Frame(self)
		tkinter.Label(self.plr2_frame, text=self.plr2_name).grid(row=0)
		tkinter.Label(self.plr2_frame, text="体力：%d"%(self.plr2.numbers["HP"])).grid(row=1)
		tkinter.Label(self.plr2_frame, text="攻击：%d"%(self.plr2.numbers["ATK"])).grid(row=2)
		tkinter.Label(self.plr2_frame, text="防御：%d"%(self.plr2.numbers["DEF"])).grid(row=3)
		tkinter.Label(self.plr2_frame, text="速度：%d"%(self.plr2.numbers["SPD"])).grid(row=4)
		tkinter.Label(self.plr2_frame, text="命中：%d"%(self.plr2.numbers["ACC"])).grid(row=5)
		tkinter.Label(self.plr2_frame, text="运气：%d"%(self.plr2.numbers["LUK"])).grid(row=6)
		self.plr2_frame.grid(row=1,column=2)
		# TODO(请叫我喵 Alynx): Add two frame to display the data of fighters realtime.

	def create_text(self):
		self.text_display = tkinter.scrolledtext.ScrolledText(self)
		self.text_display.bind("<KeyPress>", lambda e : "break")
		self.text_display.grid(row=1, column=1)

	def text_print(self, str):
		self.text_display.insert(tkinter.INSERT, str + '\n')
		self.text_display.update()
		self.text_display.see(tkinter.INSERT)

	def callback(self, event=None):
		self.plr1_name = self.name_input1.get()
		self.plr2_name = self.name_input2.get()
		if (self.plr1_name == '') or (self.plr2_name == ''):
			tkinter.messagebox.showinfo("提示", "你似乎没有把两个名字都填全哦！")
			return False
		self.save_button["state"] = "disable"
		self.text_print(self.plr1_name + ' ' + "VS" + ' ' + self.plr2_name)
		self.result = self.main(self.text_print)
		tkinter.messagebox.showinfo("Game Over!", self.result)
		self.save_button["state"] = "normal"
		# TODO(请叫我喵 Alynx):
		# 1. Add a messagebox to show the winner.
		# 2. Let the button normal after one time of game finished.

	def main(self, printer=print):
		# TODO(请叫我喵 Alynx): Let this become a private method of Application?
		"""
		运行主体。如果不能从参数中获取玩家信息，就请求输入，然后循环进行回合直至有输家产生。
		"""
		# if args.name1 == None:
		# 	plr1_name = input("输入第一个玩家的名字：")
		# else:
		# 	plr1_name = args.name1
		# if args.name2 == None:
		# 	plr2_name = input("输入第二个玩家的名字：")
		# else:
		# 	plr2_name = args.name2

		# # 彩蛋。
		# if ("日耳曼战神" in plr1_name) or ("日耳曼战神" in plr2_name):
		# 	printer("做梦吧你，日耳曼战神永远是最强的，想打赢战神？不可能！")
		# return 1

		# # 颜色化玩家名称，玩家一蓝色，玩家二黄色。
		# plr1_name = "\033[34;1m" + plr1_name + "\033[0m"
		# plr2_name = "\033[33;1m" + plr2_name + "\033[0m"

		# 生成 Fighter 对象。
		self.plr1 = Fighter(self.plr1_name, self.plr2_name, printer)
		self.plr2 = Fighter(self.plr2_name, self.plr1_name, printer)

		# 获取敌对对象。
		self.plr1.get_enemy(self.plr2)
		self.plr2.get_enemy(self.plr1)

		while abs(self.plr1.numbers["HP"] - self.plr2.numbers["HP"]) > 233:
			if self.plr1.numbers["HP"] < self.plr2.numbers["HP"]:
				self.plr1.numbers["HP"] += abs(self.plr1.numbers["HP"] - self.plr2.numbers["HP"]) * random.random()
			elif self.plr2.numbers["HP"] < self.plr1.numbers["HP"]:
				self.plr2.numbers["HP"] += abs(self.plr1.numbers["HP"] - self.plr2.numbers["HP"]) * random.random()

		self.plr1.check()
		self.plr2.check()

		# 计算双方 HP 总和的 1 / 2 作为计算上限保证不会一击致命。
		hp_limit = int(abs(self.plr1.numbers["HP"] + self.plr2.numbers["HP"]) / 2 * 0.5)
		i = 0

		self.create_data()
		printer("==================================================")

		# 进行战斗循环。
		while ((self.plr1.numbers["HP"] > 0) and (self.plr2.numbers["HP"] > 0)):
			i += 1
			# 根据速度决定谁先攻击。
			if self.plr1.numbers["SPD"] >= self.plr2.numbers["SPD"]:
				self.plr1.check()
				self.plr2.check()
				printer("回合 #%d:"%(i))
				printer("==================================================")
				# # 输出双方实时数据。
				# self.plr1.print_item()
				# self.plr2.print_item()
				# printer("==================================================")
				time.sleep(0.5)
				# 先手发起攻击。
				self.plr1.fight(hp_limit)
				# 判断是否致命。
				if not ((self.plr1.numbers["HP"] > 0) and (self.plr2.numbers["HP"] > 0)):
					time.sleep(0.5)
					printer("==================================================")
					time.sleep(0.5)
					break
				time.sleep(0.5)
				printer("--------------------------------------------------")
				time.sleep(0.5)
				# 后手发起攻击。
				self.plr2.fight(hp_limit)

			elif self.plr1.numbers["SPD"] < self.plr2.numbers["SPD"]:
				self.plr2.check()
				self.plr1.check()
				printer("回合 #%d:"%(i))
				printer("==================================================")
				# self.plr2.print_item()
				# self.plr1.print_item()
				# printer("==================================================")
				time.sleep(0.5)
				self.plr2.fight(hp_limit)
				if not ((self.plr1.numbers["HP"] > 0) and (self.plr2.numbers["HP"] > 0)):
					time.sleep(0.5)
					printer("==================================================")
					time.sleep(0.5)
					break
				time.sleep(0.5)
				printer("--------------------------------------------------")
				time.sleep(0.5)
				self.plr1.fight(hp_limit)

			time.sleep(0.5)
			printer("==================================================")
			time.sleep(0.5)

		#printer("==================================================")

		# 判断结果。
		if self.plr1.numbers["HP"] <= 0 and self.plr2.numbers["HP"] <= 0:
			# 输出双方最终数据
			if self.plr1.numbers["SPD"] >= self.plr2.numbers["SPD"]:
				self.plr1.check()
				self.plr2.check()
				# self.plr1.print_item()
				# self.plr2.print_item()
			elif self.plr1.numbers["SPD"] < self.plr2.numbers["SPD"]:
				self.plr2.check()
				self.plr1.check()
				# self.plr2.print_item()
				# self.plr1.print_item()
				# printer("==================================================")
				time.sleep(0.5)
				# printer("经历 %d 个回合，%s 和 %s 棋逢对手，两败俱伤。"%(i, self.plr1_name, self.plr2_name))	# 平局。
				return "经历 %d 个回合，%s 和 %s 棋逢对手，两败俱伤。"%(i, self.plr1_name, self.plr2_name)	# 平局。
		elif self.plr1.numbers["HP"] <= 0 and self.plr2.numbers["HP"] > 0:
			if self.plr1.numbers["SPD"] >= self.plr2.numbers["SPD"]:
				self.plr1.check()
				self.plr2.check()
				# self.plr1.print_item()
				# self.plr2.print_item()
			elif self.plr1.numbers["SPD"] < self.plr2.numbers["SPD"]:
				self.plr2.check()
				self.plr1.check()
				# self.plr2.print_item()
				# self.plr1.print_item()
				# printer("==================================================")
				time.sleep(0.5)
				# printer("经历 %d 个回合，%s 输了，获胜者是 %s。"%(i, self.plr1_name, self.plr2_name))	# 一号玩家失败。
				return "经历 %d 个回合，%s 输了，获胜者是 %s。"%(i, self.plr1_name, self.plr2_name)	# 一号玩家失败。
		elif self.plr1.numbers["HP"] > 0 and self.plr2.numbers["HP"] <= 0:
			if self.plr1.numbers["SPD"] >= self.plr2.numbers["SPD"]:
				self.plr1.check()
				self.plr2.check()
				# self.plr1.print_item()
				# self.plr2.print_item()
			elif self.plr1.numbers["SPD"] < self.plr2.numbers["SPD"]:
				self.plr2.check()
				self.plr1.check()
				# self.plr2.print_item()
				# self.plr1.print_item()
				# printer("==================================================")
				time.sleep(0.5)
				# printer("经历 %d 个回合，%s 输了，获胜者是 %s。"%(i, self.plr2_name, self.plr1_name))	# 二号玩家失败。
				return "经历 %d 个回合，%s 输了，获胜者是 %s。"%(i, self.plr2_name, self.plr1_name)	# 二号玩家失败。

root = Application()
root.mainloop()

# # 运行。
# if __name__ == "__main__":
# 	try:
# 		main()
# 	except KeyboardInterrupt:
# 		print('')
# 		exit()
