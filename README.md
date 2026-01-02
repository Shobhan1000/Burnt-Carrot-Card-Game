# Burnt Carrot Card Game

A Python implementation of the **Burnt Carrot** card game with a graphical interface built using `tkinter`.  
The game simulates a real-life card experience, including hidden cards, timed decisions, and a computer opponent.

This project focuses on **game logic, state management, and UI interaction timing**, rather than advanced graphics.

---

## Gameplay Overview

- Standard **52-card deck**
- Player vs Computer
- Players start with hidden cards, with limited opportunities to peek
- Cards are placed into a shared middle pile
- Special rules (such as the **7 rule**) affect gameplay strategy
- The goal is to get rid of all your cards first

---

## Key Design Decisions

### Deck & Middle Pile Management
- The game uses a standard 52-card deck.
- When the deck runs out, it is **reshuffled from the middle pile**, while preserving the current middle card.
- This allows the game to continue indefinitely without disrupting gameplay.

### Card Visibility Logic
- Players can view **two cards at the start**.
- Once viewed, cards return to a hidden state to mirror real-life gameplay.

### Middle Card Mechanics
- When a card is placed in the middle:
  - Both players may discard any **known card of the same rank**.
- Playing a **7** allows the player to peek at another card immediately.

### Timed Player Interaction
- Uses `tkinter.Toplevel` popups with countdown timers.
- Players have **10 seconds** to act before the game automatically continues.
- Prevents UI freezing and keeps gameplay smooth.

### Computer Player Logic
- The computer opponent behaves **semi-randomly**:
  - 50% chance to swap a card vs place one in the middle.
- The computer follows the same rules as the player, including handling 7s and discards.

---

## Technologies Used

- **Python**
- **tkinter** (GUI)
- Object-oriented design for cards, players, and game state management

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Shobhan1000/Burnt-Carrot-Card-Game.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Burnt-Carrot-Card-Game
   ```

3. Run the game:
   ```bash
   python main.py
   ```

---

## Future Improvements
- Smarter computer AI with memory of revealed cards
- Replace text-based buttons with card images
- Save and load game state
- Local or online multiplayer support
- Animations and sound effects
- Refactor code into clearer modules for scalability and testing

---

### Notes
This project was built to practice:
- Game logic implementation
- UI timing and interaction handling
- Managing hidden state in turn-based games
