import random
import RPi.GPIO as GPIO
import time
import tt

RESET_IN = 1
DOUBLES_IN = 2
A_SCORE_IN = 3
B_SCORE_IN = 4

DOUBLES_OUT = 5
A_SERVES_OUT = 6
B_SERVES_OUT = 7

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

def main():
	setup_gpio()

	try:
		game = Game.make_singles_game(random_bool())
		singles = True
		while True:
			if pressed(RESET_IN):
				if singles:
					game = Game.make_singles_game(random_bool())
				else:
					game = Game.make_doubles_game(random_bool())
			elif pressed(DOUBLES_IN):
				singles = not singles
			elif pressed(A_SCORE_IN):
				game.scores(game.get_A())
			elif pressed(B_SCORE_IN):
				game.scores(game.get_B())

			light_set(DOUBLES_OUT, not singles)
			light_set(A_SERVES_OUT, game.to_serve(game.get_A()))
			light_set(B_SERVES_OUT, game.to_serve(game.get_B()))

			pass

	except:
		print "Unexpected error"

	teardown_gpio()

if __name__ == "__main__":
	main()