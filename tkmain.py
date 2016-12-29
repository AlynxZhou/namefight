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

from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText



# 解析参数。
aparser = argparse.ArgumentParser(description="输入两个名字，让它们来决斗吧！")
aparser.add_argument("name1", nargs='?', help="第一个名字。", action="store")
aparser.add_argument("name2", nargs='?', help="第二个名字。", action="store")
args = aparser.parse_args()



__version__ = "0.1.1Beta"
__author__ = "请叫我喵 Alynx"



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
		# 生成对象的各种战斗力数据。
		self.numbers = {
			# 生命值。
			"HP": self.md5_count(self.md5, 0, 7) * 20,
			# 攻击力。
			"ATK": self.md5_count(self.md5, 7, 5) * 10,
			# 防御力。
			"DEF": self.md5_count(self.md5, 12, 5) * 10,
			# 速度。
			"SPD": self.md5_count(self.md5, 17, 5) * 10,
			# 运气。
			"LUK": self.md5_count(self.md5, 22, 5) * 10,
			# 命中率。
			"ACC": self.md5_count(self.md5, 27, 5) * 10
		}
		# 初始化一个内部敌人对象方便调用敌人的 hurt() 方法。
		self.enemy = None
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
		self.printer("%s 发狂了，上前咬了 %s 一口，造成了 %d 点伤害，自己受到反噬的 %d 点伤害。"%(self.NAME, self.ENEMY, number, number1))
		# 构建 dict
		case_number = {"HP": number}
		# 调用敌人的 hurt() 方法以处理敌方数据
		self.enemy.hurt(case_number)
		case_number = {"HP": number1}
		# 调用自己的 hurt() 方法来处理自身数据
		self.hurt(case_number)


	def sleep(self, number):
		"""
		催眠回血，恢复传入值大小的体力。
		"""
		self.printer("%s 给 %s 唱了安眠曲，%s 睡着了，%s 趁机恢复了 %d 点体力。"%(self.NAME, self.ENEMY, self.ENEMY, self.NAME, number))
		number = - number
		case_number = {"HP": number}
		self.hurt(case_number)


	def curse(self, number):
		"""
		诅咒，降低对方除体力外的的所有战斗力，降低的随机值不大于对方已有的值。
		"""
		self.printer("%s 诅咒了 %s，%s 的各项数值下降了。"%(self.NAME, self.ENEMY, self.ENEMY))
		# 构建含有多项数值的 dict
		case_number = {
			"ATK": self.spawn_number(number / 4,\
									 self.enemy.numbers["ATK"] * 0.7),
			"DEF": self.spawn_number(number / 4,\
									 self.enemy.numbers["DEF"] * 0.7),
			"SPD": self.spawn_number(number / 4,\
									 self.enemy.numbers["SPD"] * 0.7),
			"LUK": self.spawn_number(number / 4,\
									 self.enemy.numbers["LUK"] * 0.7),
			"ACC": self.spawn_number(number / 4,\
									 self.enemy.numbers["ACC"] * 0.7)
		}
		self.enemy.hurt(case_number)


	def pray(self, number):
		"""
		祈祷，增加自己除体力外的所有战斗力，增加的随机值不大于自己以有的值的 1.5 倍。
		"""
		self.printer("%s 向上天祈祷，%s 的各项数值上升了。"%(self.NAME, self.NAME))
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
		self.printer("%s 发怒了，把 %s 按在地上一顿暴打，%s 受到了 %d 点伤害，%s 受到了 %d 点伤害，%s 受到了 %d 点伤害，%s 挣脱了。"%(self.NAME, self.ENEMY, self.ENEMY, number, self.ENEMY, number1, self.ENEMY, number2, self.ENEMY))
		number = number + number1 + number2
		case_number = {"HP": number}
		self.enemy.hurt(case_number)


	def attrack(self, number):
		"""
		普通攻击，给予对方传入值大小的伤害。
		"""
		self.printer("%s 向 %s 发起了攻击，%s 受到了 %d 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, number))
		case_number = {"HP": number}
		self.enemy.hurt(case_number)


	def fall(self, number):
		"""
		摔倒，随机发生在自己发起攻击，但命中率与运气值都较低的情况下，自己受到不大于传入值 50% 的伤害。
		"""
		number = self.spawn_number(1, 0.5 * number)
		self.printer("%s 向 %s 发起攻击，但是被 %s 绊倒了，%s 受到了 %d 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, self.NAME, number))
		case_number = {"HP": number}
		self.hurt(case_number)


	def miss(self, number):
		"""
		未击中，随机发生在自己发起攻击，但命中率较低而运气值又较高的情况下，双方均不承受伤害。
		"""
		self.printer("%s 向 %s 发起了攻击，但是被 %s 躲开了。"%(self.NAME, self.ENEMY, self.ENEMY))


	def fight(self, hp_limit):
		"""
		实际的战斗操作。通过 dict 与匿名函数实现 switch-case 结构。
		"""
		# 利用攻方的攻击力及守方的防御力以及两方的运气，生成一个计算初始值，其保证不会一击致命。
		number = self.spawn_number(
			abs(
				abs(
					self.numbers["ATK"] - self.enemy.numbers["DEF"]
				) * abs(
					self.numbers["LUK"] - self.enemy.numbers["LUK"]
				) - self.numbers["ATK"] * random.random()
			),
			hp_limit
		)

		# 通过双方的命中率生成的随机值判断发起攻击成功还是失败。
		if self.numbers["ACC"] > int((
					self.numbers["ACC"] + self.enemy.numbers["ACC"]
				) * random.random()):
			# 可以发起攻击时随机选择攻击方式。
			case = random.choice([
				"bite",
				"angry",
				"attrack",
				"sleep",
				"curse",
				"pray"
			])
		else:
			# 攻击无法发起时减小计算值。
			number = int(number * random.random())
			# 判断运气值决定是否自己承受伤害。
			if self.numbers["LUK"] > int((
					self.numbers["LUK"] + self.enemy.numbers["LUK"]
					) * random.random()):
				case = "miss"
			else:
				case = "fall"

		# 实际调用不同战斗操作。
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



class Monitor(Fighter):
	"""
	班长类，继承 Fighter，拥有特殊的狂咬攻击。
	"""
	def __init__(self, name, enemy_name, printer=print):
		super(Monitor, self).__init__(name, enemy_name)


	def sbite(self, number):
		"""
		班长的狂咬攻击，伤害为传入基本数值的 1 到 2.6 倍。自己反噬超过传入值部分的多余伤害。
		"""
		number1 = self.spawn_number(1, 0.9 * number)
		number2 = self.spawn_number(1, 0.7 * number)
		self.printer("%s 发现 %s 思修成绩不及格，发狂了，上前狂咬了 %s 一口，造成了 %d 点伤害，又上前狂咬了 %s 一口，造成了 %d 点伤害，又上前狂咬了 %s 一口，造成了 %d 点伤害，自己受到反噬的 %d 点伤害。"%(self.NAME, self.ENEMY, self.ENEMY, self.ENEMY, self.ENEMY, number, number1, number2))
		case_number = {"HP": number + number1 + number2}
		self.enemy.hurt(case_number)
		case_number = {"HP": number1 + number2}
		self.hurt(case_number)


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
		)

		if self.numbers["ACC"] > int((
					self.numbers["ACC"] + self.enemy.numbers["ACC"]
				) * random.random()):
			case = random.choice([
				"sbite",
				"sbite",
				"sbite",
				"sbite",
				"sbite",
				"sbite",
				"sbite",
				"bite",
				"angry",
				"attrack",
				"sleep",
				"curse",
				"pray"
			])
		else:
			number = int(number * random.random())
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
		}[case](number)



class Application(Tk):
	"""
	主要的窗口程序，直接继承 tkinter 底层的 Tk 类构建。
	"""
	def __init__(self, master=None):
		"""
		窗口生成时的必要准备。
		"""
		super(Application, self).__init__(master)
		self.title("Name Fight Ver %s by %s"%(__version__, __author__))
		# 设置窗口的大小。
		# self.geometry("%dx%d"%(self.winfo_screenwidth() / 2, self.winfo_screenheight() / 2))
		# 设置窗口尺寸是否可调。
		self.resizable(width=False, height=False)
		# 自定义一个字体对象。
		self.font = Font(self, family="Monospace", size=13)
		# .grid() 布局方式对行或列占据比例的设置，weight 的总值为分母，单个 weight 的值为分子。
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=2)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=2)
		self.columnconfigure(2, weight=1)
		# 建立自己定义的对象并解析参数。
		self.create_input()
		self.create_text()
		self.parse_args(args)


	def parse_args(self, args):
		"""
		解析 argparse 生成的参数对象。
		"""
		if args.name1 != None:
			# 可以直接对 Entry() 对象使用 insert() 方法插入数据。
			self.name_input1.insert(END, args.name1)
			self.name_input1.update()
		if args.name2 != None:
			self.name_input2.insert(END, args.name2)
			self.name_input2.update()
		if (args.name1 != None) and (args.name2 != None):
			# 如果两个参数都满足就直接调用 callback() 方法去处理，不需要点击按钮。
			self.callback()


	def create_input(self):
		"""
		建立输入玩家名字的输入框和确认按钮。
		"""
		# 分别把两个输入框和自己的提示语整合进一个 Frame() 对象方便布局。
		self.input_frame1 = Frame(self)
		# 提示语，隶属于第一个 Frame，展示在这个 Frame 的第一行。
		Label(self.input_frame1,\
			  text="请输入第一个玩家的名字：",\
			  font=self.font).grid(row=0)
		# 建立隶属于第一个 Frame 的文本框对象，用于后续获取文本。
		self.name_input1 = Entry(self.input_frame1, font=self.font)
		# 在 Frame 的第二行展示。
		self.name_input1.grid(row=1)
		self.input_frame1.rowconfigure(0, weight=1)
		# 在第一行第一列展示第一个 Frame，行间距30，列间距10。
		self.input_frame1.grid(row=0, column=0, padx=30, pady=10)
		# 绑定回车作为执行键（有问题）。
		# self.name_input1.bind(sequence="<Enter>", func=self.callback)

		# 建立确定按钮，点击后执行 callback() 方法开启对战。
		self.save_button = Button(self, text="开始对战！", state="normal", command=self.callback, font=self.font)
		self.save_button.grid(row=0, column=1, padx=10, pady=10)
		# 建立第二个 Frame。
		self.input_frame2 = Frame(self)
		Label(self.input_frame2, text="请输入第二个玩家的名字：", font=self.font).grid(row=0)
		self.name_input2 = Entry(self.input_frame2, font=self.font)
		self.name_input2.grid(row=1)
		self.input_frame1.rowconfigure(0, weight=1)
		self.input_frame1.columnconfigure(0, weight=1)
		self.input_frame2.grid(row=0, column=2, padx=30, pady=10)
		# self.name_input2.bind(sequence="<Enter>", func=self.callback)


	def create_data(self):
		"""
		建立用于展示玩家数据的区域，用Label实时刷新。
		"""
		# 建立玩家1的 Frame。
		self.plr1_frame = Frame(self)
		# 建立用户1的 Label 集合用来展示数据，便于实时刷新。
		self.plr1_labels = {
			"HP": Label(self.plr1_frame,\
						text=str(self.plr1.numbers["HP"]),\
						font=self.font),
			"ATK": Label(self.plr1_frame,\
						 text=str(self.plr1.numbers["ATK"]),\
						 font=self.font),
			"DEF": Label(self.plr1_frame,\
						 text=str(self.plr1.numbers["DEF"]),\
						 font=self.font),
			"SPD": Label(self.plr1_frame,\
						 text=str(self.plr1.numbers["SPD"]),\
						 font=self.font),
			"ACC": Label(self.plr1_frame,\
						 text=str(self.plr1.numbers["ACC"]),\
						 font=self.font),
			"LUK": Label(self.plr1_frame,\
						 text=str(self.plr1.numbers["LUK"]),\
						 font=self.font)
		}
		# 显示固定不变的 Label.
		Label(self.plr1_frame,\
					  text=self.plr1_name + " 的数据",\
					  font=self.font).grid(row=0,\
										   column=0,\
										   columnspan=2,\
										   padx=30,\
										   pady=20)
		Label(self.plr1_frame,\
					  text="体力",\
					  font=self.font).grid(row=1, column=0, padx=30, pady=20)
		self.plr1_labels["HP"].grid(row=2, column=0, padx=30, pady=20)
		Label(self.plr1_frame,\
					  text="攻击",\
					  font=self.font).grid(row=3, column=0, padx=30, pady=20)
		self.plr1_labels["ATK"].grid(row=4, column=0, padx=30, pady=20)
		Label(self.plr1_frame,\
					  text="防御",\
					  font=self.font).grid(row=5, column=0, padx=30, pady=20)
		self.plr1_labels["DEF"].grid(row=6, column=0, padx=30, pady=20)
		Label(self.plr1_frame,\
					  text="速度",\
					  font=self.font).grid(row=1, column=1, padx=30, pady=20)
		self.plr1_labels["SPD"].grid(row=2, column=1, padx=30, pady=20)
		Label(self.plr1_frame,\
					  text="命中",\
					  font=self.font).grid(row=3, column=1, padx=30, pady=20)
		self.plr1_labels["ACC"].grid(row=4, column=1, padx=30, pady=20)
		Label(self.plr1_frame,\
					  text="运气",\
					  font=self.font).grid(row=5, column=1, padx=30, pady=20)
		self.plr1_labels["LUK"].grid(row=6, column=1, padx=30, pady=20)
		# self.plr1_frame.rowconfigure(0, weight=1)
		self.plr1_frame.columnconfigure(0, weight=1)
		self.plr1_frame.columnconfigure(1, weight=1)
		self.plr1_frame.grid(row=1,column=0)

		# 建立玩家2的 Frame。
		self.plr2_frame = Frame(self)
		# 建立玩家2的 Label 集合用来展示数据，便于实时刷新。
		self.plr2_labels = {
			"HP": Label(self.plr2_frame,\
						text=str(self.plr2.numbers["HP"]),\
						font=self.font),
			"ATK": Label(self.plr2_frame,\
						 text=str(self.plr2.numbers["ATK"]),\
						 font=self.font),
			"DEF": Label(self.plr2_frame,\
						 text=str(self.plr2.numbers["DEF"]),\
						 font=self.font),
			"SPD": Label(self.plr2_frame,\
						 text=str(self.plr2.numbers["SPD"]),\
						 font=self.font),
			"ACC": Label(self.plr2_frame,\
						 text=str(self.plr2.numbers["ACC"]),\
						 font=self.font),
			"LUK": Label(self.plr2_frame,\
						 text=str(self.plr2.numbers["LUK"]),\
						 font=self.font)
		}
		# 显示固定不变的 Label.
		Label(self.plr2_frame,\
					  text=self.plr2_name + " 的数据",\
					  font=self.font).grid(row=0,\
										   column=0,\
										   columnspan=2,\
										   padx=30,\
										   pady=20)
		Label(self.plr2_frame,\
					  text="体力",\
					  font=self.font).grid(row=1, column=0, padx=30, pady=20)
		self.plr2_labels["HP"].grid(row=2, column=0, padx=30, pady=20)
		Label(self.plr2_frame,\
					  text="攻击",\
					  font=self.font).grid(row=3, column=0, padx=30, pady=20)
		self.plr2_labels["ATK"].grid(row=4, column=0, padx=30, pady=20)
		Label(self.plr2_frame,\
					  text="防御",\
					  font=self.font).grid(row=5, column=0, padx=30, pady=20)
		self.plr2_labels["DEF"].grid(row=6, column=0, padx=30, pady=20)
		Label(self.plr2_frame,\
					  text="速度",\
					  font=self.font).grid(row=1, column=1, padx=30, pady=20)
		self.plr2_labels["SPD"].grid(row=2, column=1, padx=30, pady=20)
		Label(self.plr2_frame,\
					  text="命中",\
					  font=self.font).grid(row=3, column=1, padx=30, pady=20)
		self.plr2_labels["ACC"].grid(row=4, column=1, padx=30, pady=20)
		Label(self.plr2_frame,\
					  text="运气",\
					  font=self.font).grid(row=5, column=1, padx=30, pady=20)
		self.plr2_labels["LUK"].grid(row=6, column=1, padx=30, pady=20)
		# self.plr2_frame.rowconfigure(0, weight=1)
		self.plr2_frame.columnconfigure(0, weight=1)
		self.plr2_frame.columnconfigure(1, weight=1)
		self.plr2_frame.grid(row=1,column=2)


	def data_update(self, labels, fighter):
		"""
		实时更新玩家数据的方法。
		"""
		for x in labels.keys():
			labels[x].configure(text=str(fighter.numbers[x]))

	def create_text(self):
		"""
		建立文本显示区显示对战过程。
		"""
		self.text_display = ScrolledText(self, font=self.font)
		# self.text_display.bind("<KeyPress>", lambda e : "break")
		self.text_display.grid(row=1, column=1, ipadx=10, ipady=10)


	def text_print(self, str):
		"""
		将 str 输出到文本框结尾并换行。
		"""
		# tkinter 的 END 对象，指定了输入的索引为文本框末尾。
		self.text_display.insert(END, str + '\n')
		# 实时更新显示内容。
		self.text_display.update()
		# 自动滚动到文本末尾。
		self.text_display.see(END)


	def callback(self, event=None):
		"""
		点击确认之后的回调方法。
		"""
		# 获取用户名。
		self.plr1_name = self.name_input1.get()
		self.plr2_name = self.name_input2.get()
		# 检查用户名数量。
		if (self.plr1_name == '') or (self.plr2_name == ''):
			showinfo("提示", "你似乎没有把两个名字都填全哦！")
			return False
		# 开始战斗时将按钮设置为不可用。
		self.save_button["state"] = "disable"
		self.text_print(self.plr1_name + ' ' + "VS" + ' ' + self.plr2_name)
		try:
			# 进行主要的对战流程，设置输出器。
			self.main(self.text_print)
		except:
			pass
		finally:
			# 对战结束后将按钮设置为可用。
			self.save_button["state"] = "normal"
		return 0

	def main(self, printer=print, delay=0.5):
		"""
		运行主体，循环进行回合直至有输家产生。
		"""
		# 彩蛋。
		# if ("日耳曼战神" in plr1_name) or ("日耳曼战神" in plr2_name):
		# 	printer("做梦吧你，日耳曼战神永远是最强的，想打赢战神？不可能！")
		# return 1

		# 生成 Fighter 对象。
		self.plr1 = Fighter(self.plr1_name, self.plr2_name, printer)
		self.plr2 = Fighter(self.plr2_name, self.plr1_name, printer)

		# 获取敌对对象。
		self.plr1.get_enemy(self.plr2)
		self.plr2.get_enemy(self.plr1)

		# HP 补偿。
		while abs(self.plr1.numbers["HP"] - self.plr2.numbers["HP"]) > 233:
			if self.plr1.numbers["HP"] < self.plr2.numbers["HP"]:
				self.plr1.numbers["HP"] += int(abs(self.plr1.numbers["HP"] - self.plr2.numbers["HP"]) * random.random())
			elif self.plr2.numbers["HP"] < self.plr1.numbers["HP"]:
				self.plr2.numbers["HP"] += int(abs(self.plr1.numbers["HP"] - self.plr2.numbers["HP"]) * random.random())

		# 双方的数值检查，最大值 9999。
		self.plr1.check()
		self.plr2.check()

		# 计算双方 HP 总和的 1 / 2 作为计算上限保证不会一击致命。
		hp_limit = int(abs(self.plr1.numbers["HP"] + self.plr2.numbers["HP"]) / 2 * 0.5)
		# 回合计数器。
		i = 0

		# 建立玩家数据展示区域。
		self.create_data()

		printer("================================================================================")

		# 进行战斗循环。
		while ((self.plr1.numbers["HP"] > 0) and (self.plr2.numbers["HP"] > 0)):
			i += 1
			# 根据速度决定谁先攻击。
			if self.plr1.numbers["SPD"] >= self.plr2.numbers["SPD"]:
				self.plr1.check()
				self.plr2.check()
				printer("回合 #%d:"%(i))
				printer("================================================================================")
				time.sleep(delay)
				# 先手发起攻击。
				self.plr1.fight(hp_limit)
				# 更新双方实时数据。
				self.data_update(self.plr1_labels, self.plr1)
				self.data_update(self.plr2_labels, self.plr2)
				# 判断是否致命。
				if not ((self.plr1.numbers["HP"] > 0) and (self.plr2.numbers["HP"] > 0)):
					time.sleep(delay)
					printer("================================================================================")
					time.sleep(delay)
					break
				time.sleep(delay)
				printer("--------------------------------------------------------------------------------")
				time.sleep(delay)
				# 后手发起攻击。
				self.plr2.fight(hp_limit)
				self.data_update(self.plr1_labels, self.plr1)
				self.data_update(self.plr2_labels, self.plr2)

			elif self.plr1.numbers["SPD"] < self.plr2.numbers["SPD"]:
				self.plr2.check()
				self.plr1.check()
				printer("回合 #%d:"%(i))
				printer("================================================================================")
				time.sleep(delay)
				self.plr2.fight(hp_limit)
				self.data_update(self.plr1_labels, self.plr1)
				self.data_update(self.plr2_labels, self.plr2)
				if not ((self.plr1.numbers["HP"] > 0) and (self.plr2.numbers["HP"] > 0)):
					time.sleep(delay)
					printer("================================================================================")
					time.sleep(delay)
					break
				time.sleep(delay)
				printer("--------------------------------------------------------------------------------")
				time.sleep(delay)
				self.plr1.fight(hp_limit)
				self.data_update(self.plr2_labels, self.plr2)
				self.data_update(self.plr1_labels, self.plr1)

			time.sleep(delay)
			printer("================================================================================")
			time.sleep(delay)

		# 判断结果。
		if self.plr1.numbers["HP"] <= 0 and self.plr2.numbers["HP"] <= 0:
			# 输出双方最终数据
			if self.plr1.numbers["SPD"] >= self.plr2.numbers["SPD"]:
				self.plr1.check()
				self.plr2.check()
				self.data_update(self.plr1_labels, self.plr1)
				self.data_update(self.plr2_labels, self.plr2)
			elif self.plr1.numbers["SPD"] < self.plr2.numbers["SPD"]:
				self.plr2.check()
				self.plr1.check()
				self.data_update(self.plr2_labels, self.plr2)
				self.data_update(self.plr1_labels, self.plr1)
				time.sleep(delay)
				# 弹框显示平局。
			showinfo("Game Over!", "经历 %d 个回合，%s 和 %s 棋逢对手，两败俱伤。"%(i, self.plr1_name, self.plr2_name))
		elif self.plr1.numbers["HP"] <= 0 and self.plr2.numbers["HP"] > 0:
			if self.plr1.numbers["SPD"] >= self.plr2.numbers["SPD"]:
				self.plr1.check()
				self.plr2.check()
				self.data_update(self.plr2_labels, self.plr2)
				self.data_update(self.plr1_labels, self.plr1)
			elif self.plr1.numbers["SPD"] < self.plr2.numbers["SPD"]:
				self.plr2.check()
				self.plr1.check()
				self.data_update(self.plr2_labels, self.plr2)
				self.data_update(self.plr1_labels, self.plr1)
				time.sleep(delay)
			# 一号玩家失败。
			showinfo("Game Over!", "经历 %d 个回合，%s 输了，获胜者是 %s。"%(i, self.plr1_name, self.plr2_name))
		elif self.plr1.numbers["HP"] > 0 and self.plr2.numbers["HP"] <= 0:
			if self.plr1.numbers["SPD"] >= self.plr2.numbers["SPD"]:
				self.plr1.check()
				self.plr2.check()
				self.data_update(self.plr1_labels, self.plr1)
				self.data_update(self.plr2_labels, self.plr2)
			elif self.plr1.numbers["SPD"] < self.plr2.numbers["SPD"]:
				self.plr2.check()
				self.plr1.check()
				self.data_update(self.plr2_labels, self.plr2)
				self.data_update(self.plr1_labels, self.plr1)
				time.sleep(delay)
			# 二号玩家失败。
			showinfo("Game Over!", "经历 %d 个回合，%s 输了，获胜者是 %s。"%(i, self.plr2_name, self.plr1_name))
		return 0

# 运行。
if __name__ == "__main__":
	try:
		root = Application()
		# 启动程序主循环
		root.mainloop()
	except:
		print('')
		exit()
