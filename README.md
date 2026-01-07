# Rock-Paper-Scissors-Bomb AI Game Referee

This project implements a conversational AI bot for a **Rock-Paper-Scissors-Bomb** game using **Google ADK**. The bot enforces rules, tracks state, and provides meaningful feedback to the user for a 3-round game.

---

## State Model
The game state is encapsulated in the `GameState` class, which ensures the state persists across rounds. The state tracks:
- **`round_count`**: The current round number (1–3).
- **`user_score`**: Total rounds won by the user.
- **`bot_score`**: Total rounds won by the bot.
- **`user_bomb_used`**: A boolean indicating if the user has used their "bomb" move.
- **`bot_bomb_used`**: A boolean indicating if the bot has used its "bomb" move.

The state is serialized to and from a dictionary using `to_dict` and `from_dict`, ensuring easy integration with tools. This separation enables clean state management and tool interaction.

---

## Agent and Tool Design
The solution follows Google's ADK model with a clean separation of functionality:
1. **Agent (`GameRefereeBot`)**:
   - Orchestrates the game flow, manages the state, and generates user-friendly responses.
   - Handles intent understanding, tool execution, and response generation.
   - Manages round-by-round dynamics, including validating inputs, resolving rounds, and ending the game gracefully.

2. **Tools**:
   - **`ValidateMoveTool`**:
     - Validates the user's move.
     - Ensures invalid moves (e.g., empty or unsupported inputs) are rejected with clear feedback.
     - Enforces that the "bomb" move can only be used once per game.
   - **`ResolveRoundTool`**:
     - Determines the winner of the round based on the game's rules.
     - Updates game scores and tracks bomb usage.
     - Advances the round number.

This design ensures strict state manipulation rules via tools and promotes modularity.

---

## Tradeoffs
### Design Choices
1. **Tool Abstraction**:
   - Validation (`ValidateMoveTool`) and logic resolution (`ResolveRoundTool`) were implemented as separate tools to achieve modularity.
   - This added slight overhead in communication between the agent and tools but improved extensibility and maintainability.
2. **CLI Simplicity**:
   - The command-line interface (CLI) was chosen over more complex UI frameworks to align with the scope and technical constraints (e.g., no long-running servers or databases).

### Tradeoffs
- **AI Bot Intelligence**:
  - The bot's move generation relies on a 50% chance of using a "bomb" if available, followed by a random selection. This is simple but less strategic.
  - A smarter move simulation (e.g., estimating user behavior based on prior moves) was deprioritized in favor of simplicity.
- **High Configurability vs. Minimalism**:
  - The game logic was hardcoded for the "best of 3" format and specific rules, ensuring clarity but sacrificing flexibility for other configurations (e.g., adjustable rounds).

---

## Potential Improvements
With more time, the following enhancements could be made:
1. **AI Strategy**:
   - Implement a more intelligent bot strategy for move selection, potentially using heuristics or weighted probabilities to provide more engaging gameplay.
2. **State Persistence**:
   - Add support for saving and loading game progress in-memory (e.g., using JSON files), while still avoiding external databases per the constraints.
3. **Comprehensive Testing**:
   - Add unit tests and integration tests to ensure edge-case handling (e.g., invalid inputs, simultaneous bombs).
4. **User Behavior Analysis**:
   - Track user moves across rounds to predict future moves, which would make the bot seem more adaptive and "intelligent."
5. **Dynamic Configuration**:
   - Allow users to set custom game configurations, such as the number of rounds or move probability for the bot.
6. **Enhanced Responses**:
   - Improve response generation with richer language and optional humor (e.g., playful responses to invalid inputs).

---

## How to Play
1. Run the game:
   ```bash
   python rock_paper_scissors_bomb_game.py
   ```
2. Follow the prompts to input your moves (`rock`, `paper`, `scissors`, `bomb`).
3. The game provides:
   - Round-by-round outcomes with round number, moves played, and the winner.
   - Final results (user wins, bot wins, or a draw).

Thank you for playing!
