from ursina import *

from UrsinaAchievements.achievements import create_achievement, achievement, Achievement


if __name__ == '__main__':

	app = Ursina()

	do = False

	def cond():
		global do
		return do

	create_achievement(name = 'Welcome!', condition = cond, icon = 'textures/confetti.png', sound = 'sudden',
	                   duration = 1.5, description = 'Launch the game !')

	@achievement("Blup!", "textures/bubbles.png", "sign", 1, hidden = True)
	def condition():
		return bool(held_keys["left mouse"])

	@after(1.5)
	def setdo1():
		global do
		do = True

	Sky()

	app.run()
