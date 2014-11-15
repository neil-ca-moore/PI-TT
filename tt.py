class PlayerState:
	def __init__(self):
		self.score = 0

	def get_score(self):
		return self.score

	def scored_point(self):
		self.score += 1

class Game:
	def __init__(self, player_A_goes_first, is_doubles = False):
		self.playerA = PlayerState()
		self.playerB = PlayerState()
		self.next_player_is_A = player_A_goes_first
		if is_doubles:
			self.serves_each = 5
			self.points_to_win = 21
		else:
			self.serves_each = 2
			self.points_to_win = 11

	@classmethod
	def make_singles_game(cls, player_A_goes_first):
		return cls(player_A_goes_first, False)

	@classmethod
	def make_doubles_game(cls, player_A_goes_first):
		return cls(player_A_goes_first, True)

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

	def winning_score_check(self, candidate_winner_score, candidate_loser_score):		
		return candidate_winner_score >= self.points_to_win and candidate_winner_score >= candidate_loser_score + 2

	def has_won(self, player):
		return self.winning_score_check(player.get_score(), self.other_player(player).get_score())

	def player_scored(self, player):
		player.scored_point()
		total_points = self.total_points_scored()
		if total_points >= 2 * self.points_to_win - 1 or total_points % self.serves_each == 0:
			self.next_player_is_A = not self.next_player_is_A

	def scores(self, player):
		if self.has_won(player):
			raise "Player has already won!"
		elif self.has_won(self.other_player(player)):
			raise "Player has already lost!"
		else:
			self.player_scored(player)

	def total_points_scored(self):
		return self.playerA.get_score() + self.playerB.get_score()
