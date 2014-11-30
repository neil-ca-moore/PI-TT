import random
import RPi.GPIO as GPIO
import time
import tt

RESET_IN = 19   -- GPIO10
DOUBLES_IN = 21 -- GPIO09
A_SCORE_IN = 11 -- GPIO17
B_SCORE_IN = 12 -- GPIO18

DOUBLES_OUT = 7   -- GPIO04
A_SERVES_OUT = 23 -- GPIO11
B_SERVES_OUT = 24 -- GPIO08

def setup_gpio:
	GPIO.setmode(GPIO.BOARD)
	
	GPIO.setup(RESET_IN, GPIO.IN)
	GPIO.setup(DOUBLES_IN, GPIO.IN)
	GPIO.setup(A_SCORE_IN, GPIO.IN)
	GPIO.setup(B_SCORE_IN, GPIO.IN)
	
	GPIO.setup(DOUBLES_OUT, GPIO.OUT)
	GPIO.setup(A_SERVES_OUT, GPIO.OUT)
	GPIO.setup(B_SERVES_OUT, GPIO.OUT)

def teardown_gpio:
	GPIO.cleanup()

def pressed(pin):
	pressed = not GPIO.input(pin)
	if pressed:
		# time.sleep(0.2) # debounce - is this needed?
		return True
	else:
		return False

def turn_on(pin):
	GPIO.output(pin, 1)

def turn_off(pin):
	GPIO.output(pin, 0)

def random_bool():
	return random.randint(0, 1)

def light_set(pin, on):
	if on:
		turn_on(pin)
	else:
		turn_off(pin)

def flash_until(pin_to_flash, pin_to_stop_on):
	while not pressed(RESET_IN):
		time.sleep(0.5)
		turn_on(pin_to_flash)
		time.sleep(0.5)
		turn_off(pin_to_flash)

def main():
	setup_gpio()

	try:
		game = Game.make_singles_game(random_bool())
		singles = True
		while True:
			if pressed(DOUBLES_IN):
				singles = not singles
			elif pressed(A_SCORE_IN):
				game.scores(game.get_A())
			elif pressed(B_SCORE_IN):
				game.scores(game.get_B())

			reset = False
			if game.has_won(game.get_A()):
				flash_until(A_SERVES_OUT, RESET_IN)
				reset = True
			elif game.has_won(game.get_B()):
				flash_until(B_SERVES_OUT, RESET_IN)
				reset = True
			elif pressed(RESET_IN):
				reset = True

			if reset:
				if singles:
					game = Game.make_singles_game(random_bool())
				else:
					game = Game.make_doubles_game(random_bool())

			light_set(DOUBLES_OUT, not singles)
			light_set(A_SERVES_OUT, game.to_serve(game.get_A()))
			light_set(B_SERVES_OUT, game.to_serve(game.get_B()))

			pass

	except:
		print "Unexpected error"

	teardown_gpio()

if __name__ == "__main__":
	main()
