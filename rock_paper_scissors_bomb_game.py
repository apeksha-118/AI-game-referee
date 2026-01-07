import random

# Game rules
VALID_MOVES = ["rock", "paper", "scissors", "bomb"]
WINNING_RULES = {
    "rock": ["scissors"],
    "paper": ["rock"],
    "scissors": ["paper"],
    "bomb": VALID_MOVES  # Bomb beats everything, including another bomb
}

#-----------------------------------------------
# Game State
#-----------------------------------------------
class GameState:
    def __init__(self):
        self.round_count = 1
        self.user_score = 0
        self.bot_score = 0
        self.user_bomb_used = False
        self.bot_bomb_used = False

#-----------------------------------------------
# Tools for Validation and Resolution
#-----------------------------------------------
class ValidateMoveTool:
    @staticmethod
    def validate(move, user_bomb_used):
        move = move.lower()
        if move not in VALID_MOVES:
            return False, "Invalid move. Valid moves are: rock, paper, scissors, bomb."
        if move == "bomb" and user_bomb_used:
            return False, "You have already used your bomb. Choose another move."
        return True, move

class ResolveRoundTool:
    @staticmethod
    def resolve(user_move, bot_move, state):
        # Determine the outcome of the round
        if user_move == bot_move:
            result = f"Round {state.round_count}: It's a DRAW! Both played {user_move}."
        elif bot_move in WINNING_RULES[user_move]:
            state.user_score += 1
            result = f"Round {state.round_count}: You WIN! {user_move} beats {bot_move}."
        else:
            state.bot_score += 1
            result = f"Round {state.round_count}: You LOSE! {bot_move} beats {user_move}."

        # Track bomb usage
        if user_move == "bomb":
            state.user_bomb_used = True
        if bot_move == "bomb":
            state.bot_bomb_used = True

        # Update round count
        state.round_count += 1

        return result

#-----------------------------------------------
# Game Referee Bot
#-----------------------------------------------
class GameRefereeBot:
    def __init__(self):
        self.state = GameState()

    def generate_bot_move(self):
        """Generate the bot's move based on rules and randomization."""
        if not self.state.bot_bomb_used and random.random() < 0.5:
            return "bomb"
        return random.choice(["rock", "paper", "scissors"])

    def respond_to_user(self, user_input):
        # Output: Explain the rules initially
        if self.state.round_count == 1:
            return "Welcome to Rock-Paper-Scissors-Bomb! Best of 3 rounds. " \
                   "Valid moves: rock, paper, scissors, bomb. " \
                   "Bomb can be used only once per game. Let's begin!"

        # Output: If the game is over
        if self.state.round_count > 3:
            if self.state.user_score > self.state.bot_score:
                return f"Game over! You WIN the game with a score of {self.state.user_score}-{self.state.bot_score}."
            elif self.state.user_score < self.state.bot_score:
                return f"Game over! The BOT wins the game with a score of {self.state.bot_score}-{self.state.user_score}."
            else:
                return f"Game over! It's a DRAW with a score of {self.state.user_score}-{self.state.bot_score}."

        # Validate the user's move
        is_valid, message = ValidateMoveTool.validate(user_input, self.state.user_bomb_used)
        if not is_valid:
            return message

        user_move = message  # The validated move
        bot_move = self.generate_bot_move()

        # Resolve the round
        result = ResolveRoundTool.resolve(user_move, bot_move, self.state)

        # Output the result of this round
        return f"{result}\nCurrent Score: You {self.state.user_score} - {self.state.bot_score} Bot"

#-----------------------------------------------
# Main: Game Loop
#-----------------------------------------------
if __name__ == "__main__":
    bot = GameRefereeBot()

    # Start conversation
    print(bot.respond_to_user(None))  # Print the welcome message

    while bot.state.round_count <= 3:
        user_input = input(f"Round {bot.state.round_count}, enter your move: ")
        response = bot.respond_to_user(user_input)
        print(response)

    print("\nThank you for playing!")