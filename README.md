# Rock-Paper-Scissors-Bomb AI Game Referee

This project implements a conversational AI bot to referee a game of **Rock-Paper-Scissors-Bomb** in Python. The bot enforces game rules, validates user inputs, tracks the state of the game, and provides dynamic responses. The game is played over 3 rounds, with each round providing detailed feedback and a final result at the end.

---

## State Model
The game state is managed using the `GameState` class, which tracks:
- **`round_count`**: The current round number (1–3).
- **`user_score`**: Total rounds won by the player.
- **`bot_score`**: Total rounds won by the bot.
- **`user_bomb_used`**: Tracks whether the user has already used the "bomb" move.
- **`bot_bomb_used`**: Tracks whether the bot has already used the "bomb" move.

This design ensures that the state persists across rounds and enforces the game rules.

---

## Design Overview
The code is structured into three main components for clarity and modularity:

### 1. Game Referee
The **`GameRefereeBot`** manages the game flow and orchestrates the interaction between the tools and the game state. It:
- Prompts the user for input.
- Generates the bot’s move in each round.
- Provides clear, structured responses about the current round and overall game results.

### 2. Validate Move Tool
The **`ValidateMoveTool`** ensures user inputs are valid. It:
- Checks if the user’s move is one of the valid choices: `rock`, `paper`, `scissors`, `bomb`.
- Enforces the rule that the "bomb" move may only be used once per game.

If the move is invalid, it provides feedback to the user without proceeding to the next round.

### 3. Resolve Round Tool
The **`ResolveRoundTool`** determines the outcome of each round. It:
- Compares the user’s move and the bot’s move according to the game rules.
- Updates the scores based on the result (win, lose, or draw).
- Tracks whether the "bomb" move was used during the round.
- Advances the round count.

---

## Game Rules
- The game is played for 3 rounds.
- Valid moves:
  - `rock`
  - `paper`
  - `scissors`
  - `bomb` (can be used only once per player)
- Winning conditions:
  - `rock` beats `scissors`
  - `paper` beats `rock`
  - `scissors` beats `paper`
  - `bomb` beats all other moves, but if both players use "bomb" in the same round, it results in a draw.
- Invalid inputs:
  - If the user enters an invalid input, the bot provides feedback, and the round must be replayed.

---

## Code Features
- **Round-by-Round Feedback**:
  - Round number, moves played, and round winner are clearly displayed.
  - Display of the current score after each round.
- **Final Results**:
  - The game ends automatically after 3 rounds.
  - The final result declares the winner (`User Wins`, `Bot Wins`) or a tie (`Draw`).
- **Bot AI**:
  - The bot’s moves include a 50% chance of using "bomb" if it is still available.
  - Otherwise, it chooses randomly from `rock`, `paper`, or `scissors`.

---

## Improvements Made in the Refactored Design
1. **Separation of Concerns**:
   - Tools are used for specific tasks (validation and resolving rounds), keeping the design modular and easy to maintain.
2. **Clean State Management**:
   - The `GameState` class tracks dynamic game data, ensuring persistent and accurate game rules.
3. **User-Focused Gameplay**:
   - Clear feedback is provided for both invalid inputs and results after each round, improving player experience.

---

## Potential Enhancements
Given more time, the following improvements could enhance the game:
1. **Smarter Bot AI**:
   - Add heuristics or probability-based decision-making to make the bot more challenging.
2. **Game Customization**:
   - Allow users to configure the number of rounds or introduce new moves into the game.
3. **Session Persistence**:
   - Save the game progress to a file (e.g., JSON format) for reloading and resuming games.
4. **Testing**:
   - Add automated unit tests to handle edge cases such as invalid inputs and simultaneous "bomb" usage.

---

## How to Play
1. **Run the game**:
   ```bash
   python rock_paper_scissors_bomb.py
   ```
2. **Follow the prompts** to enter your move in each round:
   - Valid inputs: `rock`, `paper`, `scissors`, `bomb`.
   - If you use "bomb," it can only be used *once* during the game.
3. **Game Workflow**:
   - The bot will respond with its move and the round result.
   - The game ends after 3 rounds, and the final winner is declared.

---

Thank you for playing!
