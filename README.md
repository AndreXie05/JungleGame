# Jungle Game (Dou Shou Qi)

Jungle Game, also known as *Dou Shou Qi*, is a two-player strategy board game where each player controls eight animal pieces with different ranks. The goal is either to capture all of the opponent’s pieces or to move one of your pieces into the opponent’s den.

---

## Table of Contents

- [Overview](#overview)
- [Board Layout](#board-layout)
  - [Grid](#grid)
  - [Lair](#lair)
  - [Traps](#traps)
  - [Rivers](#rivers)
- [Pieces and Their Rankings](#pieces-and-their-rankings)
- [Movement Rules](#movement-rules)
  - [Basic Movement](#basic-movement)
  - [Restrictions in Own Lair](#restrictions-in-own-lair)
  - [Movement Through Traps](#movement-through-traps)
- [Special Movement Rules](#special-movement-rules)
  - [Rivers](#rivers-special)
  - [Jumping Over Rivers](#jumping-over-rivers)
- [Capture Rules](#capture-rules)
- [Winning Conditions](#winning-conditions)
- [Requirements](#requirements)
- [Modifications](#modifications)
  - [Pieces and Sound](#pieces-and-sound)
  - [Difficulty](#difficulty)
- [Statistic analyse](#statistic-analyse)
- [Authors](#authors)

---

## Overview

Jungle Game is a competitive strategy board game where each player controls eight animal pieces with varying strengths. The objective is to either invade the opponent’s lair or eliminate all their pieces.

---

## Board Layout

### Grid

- The board consists of a **7×9 grid** of squares.

### Lair

- Each player has a “lair” located at the center of the back row on their side.
- **Note:** A piece cannot move into its own lair.

### Traps

- Three trap squares surround each lair.
- When a piece occupies an opponent’s trap, its strength is temporarily reduced to zero, making it vulnerable.

### Rivers

- Two river areas exist on the board.
- Each river covers a **2×3 rectangular region** (six squares per river) in the central part of the board.
- Only certain pieces are allowed to enter or cross the river.

---

## Pieces and Their Rankings

Each player commands eight pieces representing different animals. Their strengths are ranked from weakest to strongest:

- **Mouse (1)** – Weakest
- **Cat (2)**
- **Dog (3)**
- **Wolf (4)**
- **Leopard (5)**
- **Tiger (6)**
- **Lion (7)**
- **Elephant (8)** – Strongest

> **Note:** The Mouse has a special ability that allows it to capture the Elephant despite its lower rank.

---

## Movement Rules

### Basic Movement

- All pieces (when not restricted) move **one square at a time** either vertically or horizontally.
- **Diagonal moves are not allowed.**

### Restrictions in Own Lair

- No piece may enter its own lair.

### Movement Through Traps

- Pieces can enter both their own and the opponent’s traps.
- When in an opponent’s trap, a piece's strength becomes effectively **0**, making it vulnerable to capture.

---

## Special Movement Rules

### Rivers

- **Mouse:** Can enter and move through river squares.
- **Other Pieces:** Are not allowed to enter the river.

### Jumping Over Rivers

- **Lion and Tiger:** These pieces can jump over a river in a straight line (horizontally or vertically).
- They “leap” from one bank to the other, landing on the first available land square immediately after the river.
- **Obstruction:** If a Mouse (either enemy or friendly) is present in any river square along the jumping path, the jump cannot be executed.

---

## Capture Rules

- A piece captures an opposing piece by moving into its square.
- Capture is allowed only if the attacking piece’s rank is **equal to or higher** than the defending piece’s rank.
- **Special Rule:** The Mouse can capture the Elephant, exploiting its vulnerabilities.

- **Water Interaction:**
  - When the Mouse is in water, it cannot be captured by an enemy piece on land.
  - However, an opposing Mouse in the water can capture it.

---

## Winning Conditions

A player wins by fulfilling either of the following:

1. **Invading the Lair:** Successfully moving one of your pieces into the opponent’s lair.
2. **Eliminating All Opponent Pieces:** Capturing all the opponent’s pieces, leaving them with no legal moves.

---

## Requirements

To execute and play Jungle Game:

1. **Install Pygame:** Ensure it is installed on your terminal.
2. **Python Version:** Use **Python 3.12.3**.

**To run the game:**

- Open the file `run_game_visual.py` and execute it to launch a simple interface for game mode selection and customization.
- Alternatively, you can run from the command line using:
  ```bash
  $ python3 run_game_visual.py

---

## Modifications

As aspected we add some modifications to our code like, the images representing the pieces in the board, the sound and the difficulty the user would like to play.

### Pieces and sound
In the main interface the user has an option in the bottom left corner named "config" (configurations). There the user will have the chance to select the type of pieces he wants to use in the game and also to use sound or not. In the case of using sound, he also has the option of adapting the volume of the background music to his taste.

### Difficulty
In order to further engage the user, in the "Ai VS Player" mode, we have added the option to choose your own difficulty. If you want to learn how to play, we recommend the "Easy" or even "Medium" mode. If you are already familiar with the game and want to put your knowledge and strategic skills to the test, we have added two more modes, the "Hard" mode and the "Impossible" mode. The difference is that each one has it's own evaluate function.

---

## Statistic analyse
- To run the statistic mode simply run the comand python3 run_stats.py; in orser to change the test modes, go to game_optimized/AI/minimax_stats.py and change evaluate1 and evaluate2 equal to the modes you want for the player1 and 2 respectly.

- In order to change the number of games to study (predifined as 10), just change in the run_stats.py file when calling the function.

- The inconclusive is to prevent loops and draw is used when the rules are other's (maybe in future versions it will be possible to change the rules).

---

## Authors
André Xie -> up202407558

Duarte Gomes -> up202409386

José Sousa -> up202405046

---

# Have fun!! 
