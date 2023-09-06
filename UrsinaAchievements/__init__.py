from ursina import *

from UrsinaAchievements.achievements import create_achievement, achievement, delete_achievement,\
	was_achievement_triggered, Achievement


if __name__ == '__main__':

	app = Ursina()

	# --- Classic way to make achievements (deprecated) ---

	do = False

	def cond():
		global do
		return do

	create_achievement(name = 'Welcome!', condition = cond, icon = 'textures/confetti.png', sound = 'sudden',
	                   duration = 1.5, description = 'Launch the game !')


	# --- Newer way to make achievements ---

	@achievement("Blup!", "textures/bubbles.png", "sign", 1, hidden = True)
	def condition():
		return bool(held_keys["left mouse"])

	@after(1.5)
	def setdo1():
		global do
		do = True


	# --- Deleting an achievement ---
	@achievement("Useless achievement")
	def useless_achievement():
		return False

	delete_achievement("Useless achievement")


	# --- Getting whether an achievement was triggered ---
	print(was_achievement_triggered("Welcome!"))


	# Setting up Ursina
	Sky()
	app.run()
