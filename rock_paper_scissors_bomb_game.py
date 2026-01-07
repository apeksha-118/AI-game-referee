from googleadk import ADKAgent, ADKTool, ADKState, ADKResponse
import random

# Game rules
VALID_MOVES = ["rock", "paper", "scissors", "bomb"]
WINNING_RULES = {
    "rock": ["scissors"],
    "paper": ["rock"],
    "scissors": ["paper"],
    "bomb": VALID_MOVES  # Bomb beats everything, including another bomb
}


# GameState: Persistent State of the Game

class GameState(ADKState):
    def __init__(self):
        self.round_count = 1
        self.user_score = 0
        self.bot_score = 0
        self.user_bomb_used = False
        self.bot_bomb_used = False

    def to_dict(self):
        return {
            "round_count": self.round_count,
            "user_score": self.user_score,
            "bot_score": self.bot_score,
            "user_bomb_used": self.user_bomb_used,
            "bot_bomb_used": self.bot_bomb_used
        }

    @staticmethod
    def from_dict(state_dict):
        state = GameState()
        state.round_count = state_dict.get("round_count", 1)
        state.user_score = state_dict.get("user_score", 0)
        state.bot_score = state_dict.get("bot_score", 0)
        state.user_bomb_used = state_dict.get("user_bomb_used", False)
        state.bot_bomb_used = state_dict.get("bot_bomb_used", False)
        return state



# Game Tools for Validation and Resolution

# Tool: Validate Move
class ValidateMoveTool(ADKTool):
    def run(self, input_data, state):
        move = input_data.get("move", "").lower()
        if move not in VALID_MOVES:
            return {"valid": False, "message": "Invalid move. Valid moves are: rock, paper, scissors, bomb."}
        if move == "bomb" and state.user_bomb_used:
            return {"valid": False, "message": "You have already used your bomb. Choose another move."}
        return {"valid": True, "move": move}

# Tool: Resolve Round (Determine Winner and State Updates)
class ResolveRoundTool(ADKTool):
    def run(self, input_data, state):
        user_move = input_data["user_move"]
        bot_move = input_data["bot_move"]

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

        return {"result": result, "state": state.to_dict()}



# Game Referee Bot

class GameRefereeBot(ADKAgent):
    def __init__(self):
        super().__init__()
        self.state = GameState()
        self.add_tool("validate_move", ValidateMoveTool())
        self.add_tool("resolve_round", ResolveRoundTool())

    def generate_bot_move(self):
        """Generate the bot's move based on rules and randomization."""
        if not self.state.bot_bomb_used and random.random() < 0.5:
            return "bomb"
        return random.choice(["rock", "paper", "scissors"])

    def respond_to_user(self, input_text):
        # Output: Explain the rules initially
        if self.state.round_count == 1:
            return ADKResponse("Welcome to Rock-Paper-Scissors-Bomb! Best of 3 rounds. "
                               "Valid moves: rock, paper, scissors, bomb. "
                               "Bomb can be used only once per game. Let's begin!")

        # Output: If the game is over
        if self.state.round_count > 3:
            if self.state.user_score > self.state.bot_score:
                return ADKResponse(f"Game over! You WIN the game with a score of {self.state.user_score}-{self.state.bot_score}.")
            elif self.state.user_score < self.state.bot_score:
                return ADKResponse(f"Game over! The BOT wins the game with a score of {self.state.bot_score}-{self.state.user_score}.")
            else:
                return ADKResponse(f"Game over! It's a DRAW with a score of {self.state.user_score}-{self.state.bot_score}.")

        # Step 1: Validate the user's move
        validation_response = self.run_tool("validate_move", {"move": input_text}, self.state)
        if not validation_response["valid"]:
            return ADKResponse(validation_response["message"])

        user_move = validation_response["move"]

        # Step 2: Generate the bot's move
        bot_move = self.generate_bot_move()

        # Step 3: Resolve the round
        resolve_response = self.run_tool("resolve_round", {"user_move": user_move, "bot_move": bot_move}, self.state)
        self.state = GameState.from_dict(resolve_response["state"])  # Update the state

        # Output the result of this round
        return ADKResponse(f"{resolve_response['result']}\n"
                           f"Current Score: You {self.state.user_score} - {self.state.bot_score} Bot")



# Main: Game Loop

if __name__ == "__main__":
    bot = GameRefereeBot()

    # Start conversation
    print(bot.respond_to_user(None).message)  # Print the welcome message

    while bot.state.round_count <= 3:
        user_input = input(f"Round {bot.state.round_count}, enter your move: ")
        response = bot.respond_to_user(user_input)
        print(response.message)

    print("\nThank you for playing!")