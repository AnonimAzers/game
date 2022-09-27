import os
import time
import colorama
import random
from colorama import Fore, Back, Style

colorama.init()
clear = lambda: os.system('cls')

clear()

enemyes_data = {
	"волк" : [150, 7, 100],
	"лиса" : [120, 17, 110],
	"ежик" : [60, 5, 30],
	"медведь" : [500, 32, 1000]
}



game_events = {
	"Что вы будете делать?" : ["Пойти на охоту", "Найти материалы", "Построить дом", "Пойти поспать"],
	"Вас кто-то потревожил..." : ["Выйти посмотреть", "Остаться в укрытии"],
	"Перед вами стоит": ["Пойти в атаку", "Попытаться убежать"],
	"К вам пришел торговец, хотите посмотреть его ассортимент?" : ["Да", "Нет"],
	"К вашему убежищу подошел медведь!" : ["Атаковать", "Спрятаться"]

}

class pPlayerData:
	max_health = 100
	health = 100
	power = 10
	money = 25
	max_stamina = 100
	stamina = 100
	progress = 0
	materials = 100
	need_to_next = 100

trader_assortiment = [["Прокачать меч", 100], ["Прокачать хп", 100], ["Прокачать выносливость",100]]

class GameFuncs:
	def PrintPlayerInfo():
		print(Fore.RED + "\t"*12 + f"ХП {pPlayerData.health}")
		print(Fore.RED + "\t"*12 + f"Сила атаки {pPlayerData.power}")
		print(Fore.GREEN + "\t"*12 + f"Выносливость {pPlayerData.stamina}")
		print(Fore.GREEN + "\t"*12 + f"Прогресс постройки {pPlayerData.progress}")
		print(Fore.YELLOW + "\t"*12 + f"Деньги {pPlayerData.money}")
		print(Fore.CYAN + "\t"*12 + f"Материалы {pPlayerData.materials}")
		print(Fore.CYAN + "\t"*12 + f"Нужно для дома {pPlayerData.need_to_next}")
		print(Fore.WHITE)

	def PrintTypingText(text):
		for word in text:
			print(word, end='', flush=True)
			time.sleep(0.04)
		print()

	def StartGameText():
		GameFuncs.PrintTypingText("Вы просыпаетесь...")
		GameFuncs.PrintTypingText("Вам светит яркое солнце в лицо")
		GameFuncs.PrintTypingText("Оглядевшись по сторонам, вы видите густой лес")

	def PrintChoiseSreen(id):
		for i, choise in enumerate(game_events[list(game_events)[id]]):
			print(f"[{i+1}] {choise}")
		return (input("Вы решили (введите число): "))		

	def PlayGameDo():
		return GameFuncs.PrintChoiseSreen(0)

	def Fight(enemy_id):
		enemy = list(enemyes_data)[enemy_id]

		enemy_health = enemyes_data[enemy][0]
		enemy_attack = enemyes_data[enemy][1]
		enemy_chanse_leave = enemyes_data[enemy][2]

		while True:
			clear()
			GameFuncs.PrintPlayerInfo()
			print(f"Перед вами стоит {enemy} | ХП: {enemy_health}")
			choise = GameFuncs.PrintChoiseSreen(2)
			if choise == '1':
				enemy_health -= pPlayerData.power
				pPlayerData.health -= enemy_attack
				if pPlayerData.health <= 0:
					print("Вы умерли!")
					exit()
				if enemy_health <= 0:
					pPlayerData.money += int(enemyes_data[enemy][2])
					print(f"Вы заработали {int(enemyes_data[enemy][2])}")
					return
			if choise == '2':
				pPlayerData.money += int(enemyes_data[enemy][2]*((enemyes_data[enemy][0]-enemy_health)/enemyes_data[enemy][0]))
				print(f"Вы заработали {int(enemyes_data[enemy][2]*((enemyes_data[enemy][0]-enemy_health)/enemyes_data[enemy][0]))}")
				return


	def Trader():
		while True:
			clear()
			GameFuncs.PrintPlayerInfo()
			print("Перед вами ассортимент продавца")
			for assortiment in trader_assortiment:
				print(f"{assortiment[0]}: {assortiment[1]}")
			choise = int(input("Вы решили купить (0 для выхода): "))
			if choise == 0:
				print("Вы решили закончить торговлю с продавцом")
				input()
				return
			if choise == 1:
				if money >= 500:
					pPlayerData.money("Вы прокачали силу!")
					pPlayerData.power += 10
					pPlayerData.money -= 500
				else:
					print("Вам не хватило денег!")
			if choise == 2:
				if pPlayerData.money >= 500:
					print("Вы прокачали хп!")
					pPlayerData.max_health += 10
					pPlayerData.money -= 500
				else:
					print("Вам не хватило денег!")		
			if choise == 2:
				if pPlayerData.money >= 500:
					print("Вы прокачали выносливость!")
					pPlayerData.max_stamina += 10
					pPlayerData.money -= 500
				else:
					print("Вам не хватило денег!")
			input()

GameFuncs.PrintPlayerInfo()
GameFuncs.StartGameText()

while pPlayerData.progress <= 100:
	clear()
	GameFuncs.PrintPlayerInfo()
	choise = GameFuncs.PlayGameDo()
	if choise == '1':
		enemy_id = random.randint(0, 2)
		GameFuncs.Fight(enemy_id)
	if choise == '2':
		if pPlayerData.stamina >= 10:
			find = random.randint(2, 60)
			print(f"Вы пошли в лес и собрали {find} материалов")
			print(f"Ваша выносливость упала на 10%")
			pPlayerData.stamina -= 25
			pPlayerData.materials += find
		else:
			print("Не хватает энергии!")
	if choise == '3':
		if pPlayerData.materials >= pPlayerData.need_to_next:
			print(f"Вы потратили {pPlayerData.need_to_next}")
			pPlayerData.progress += 10
			pPlayerData.materials -= pPlayerData.need_to_next
			pPlayerData.need_to_next += pPlayerData.progress/100*900
		else:
			print("Вам не хватает материалов!")
	if choise == '4':
		print("Вы выспались и восстановили свою статистику")
		pPlayerData.health = pPlayerData.max_health
		pPlayerData.stamina = pPlayerData.max_stamina
		if pPlayerData.progress >= 25:
			if random.randint(0,50) > 40:
				print(list(game_events)[3])
				if GameFuncs.PrintChoiseSreen(3) == '1':
					GameFuncs.Trader()
				else:
					print("Вам пока не хочется торговаться")
		elif pPlayerData.progress >= 75:
			if random.randint(0, 60) > 45:
				print(list(game_events)[4])
				if GameFuncs.PrintChoiseSreen(4) == '1':
					GameFuncs.Fight(3)
				else:
					print("Вы смогли убежать, но ваш дом был поломан!")
					pPlayerData.progress -= 25
	input()
print("Вы прошли игру, ура!")





