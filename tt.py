class PlayerState:
	def __init__(self):
		self.score = 0

	def get_score(self):
		return self.score

	def scored_point(self):
		self.score += 1

class Game:
	SERVES_EACH = 2
	POINTS_TO_WIN = 11

	def __init__(self, player_A_goes_first):
		self.playerA = PlayerState()
		self.playerB = PlayerState()
		self.next_player_is_A = player_A_goes_first

	def get_A(self):
		return self.playerA

	def get_B(self):
		return self.playerB

	def other_player(self, player):
		if player == self.playerA:
			return self.playerB
		else:
			return self.playerA

	def to_serve(self, player):
		if player == self.get_A():
			return self.next_player_is_A
		else:
			return not self.next_player_is_A

	@classmethod
	def have_won(cls, candidate_winner_score, candidate_loser_score):		
		return candidate_winner_score >= cls.POINTS_TO_WIN and candidate_winner_score >= candidate_loser_score + 2

	def has_won(self, player):
		return Game.have_won(player.get_score(), self.other_player(player).get_score())

	def player_scored(self, player):
		player.scored_point()
		total_points = self.total_points_scored()
		if total_points >= 2 * self.POINTS_TO_WIN - 1 or total_points % self.SERVES_EACH == 0:
			self.next_player_is_A = not self.next_player_is_A

	def scores(self, player):
		self.player_scored(player)

	def total_points_scored(self):
		return self.playerA.get_score() + self.playerB.get_score()
