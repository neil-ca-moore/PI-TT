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

	def A_to_serve(self):
		return self.next_player_is_A

	def B_to_serve(self):
		return not self.A_to_serve()

	@classmethod
	def have_won(cls, candidate_winner_score, candidate_loser_score):		
		return candidate_winner_score >= cls.POINTS_TO_WIN and candidate_winner_score >= candidate_loser_score + 2

	def A_has_won(self):
		return Game.have_won(self.playerA.get_score(), self.playerB.get_score())

	def B_has_won(self):
		return Game.have_won(self.playerB.get_score(), self.playerA.get_score())

	def A_scores(self):
		self.player_scored(self.playerA)

	def B_scores(self):
		self.player_scored(self.playerB)

	def total_points_scored(self):
		return self.playerA.get_score() + self.playerB.get_score()

	def player_scored(self, player):
		player.scored_point()
		total_points = self.total_points_scored()
		if total_points >= 2 * self.POINTS_TO_WIN - 1 or total_points % self.SERVES_EACH == 0:
			self.next_player_is_A = not self.next_player_is_A
