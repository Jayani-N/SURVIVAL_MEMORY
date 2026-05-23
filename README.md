# 🧠 Memory Survival Game

A Python Tkinter-based memory challenge game where players must remember a set of objects shown for a few seconds and then use the correct object to survive dangerous situations.

---

# 🎮 Game Concept

The game works in two phases:

## Phase 1: Observation
A set of random objects is displayed on the screen for a limited time.

Example:

- 🔑 Key
- 🧯 Fire Extinguisher
- 🪢 Rope
- 🔦 Flashlight
- 🔨 Hammer

The player must quickly observe and remember them.

---

## Phase 2: Survival Situation

After the timer ends, a scenario appears.

Example:

> 🔥 Fire starts spreading across the room.  
> The door is locked.  
> What will you use to escape?

The player types the object they think is correct.

---

# ✨ Features

- Modern Tkinter GUI
- Countdown timer
- Progress bar animation
- Multiple survival scenarios
- Lives system
- Score tracking
- Restart functionality
- Keyboard support using Enter key
- Emoji-based object visualization
- Randomized object order

---

# 🛠 Technologies Used

- Python 3
- Tkinter
- ttk
- random module

---

# 📂 Project Structure

```bash
memory-survival-game/
│
├── main.py
├── README.md
```

---

# ▶️ How to Run

## 1. Install Python

Download Python from:

https://www.python.org/downloads/

---

## 2. Run the Game

Open terminal or command prompt inside the project folder.

```bash
python main.py
```

---

# 🎯 Game Rules

- Observe the displayed objects carefully.
- After the timer ends, answer the situation using one of the remembered objects.
- Correct answer → +1 score
- Wrong answer → lose 1 life
- Game ends when:
  - All rounds are completed
  - Lives become 0

---

# ❤️ Example Gameplay

## Objects Displayed

```text
🔑 Key
🧯 Fire Extinguisher
🪢 Rope
🔦 Flashlight
🔨 Hammer
```

## Situation

```text
🔥 Fire starts spreading across the room.
The door is locked.
What will you use to escape?
```

## Player Input

```text
fire extinguisher
```

---

# ⚙️ Customization

You can easily add:

- More rounds
- More objects
- Difficulty levels
- Sound effects
- Background music
- Image-based objects
- Animated transitions
- Multiplayer mode
- Database leaderboard

---

# 🧩 Adding New Rounds

Inside the `ROUNDS` list:

```python
{
    "objects": [
        "🪓 Axe",
        "🔦 Flashlight",
        "🪢 Rope"
    ],

    "question": (
        "🌲 You are trapped inside a forest at night.\n"
        "Wild animals are nearby.\n"
        "What will you use?"
    ),

    "correct_answers": [
        "flashlight"
    ]
}
```

---

# ⌨️ Keyboard Controls

| Key | Action |
|-----|--------|
| Enter | Submit Answer |

---

# 🏆 Ending Types

| Score | Result |
|------|------|
| Full Score | 🏆 PERFECT MEMORY MASTER |
| Medium Score | 🎯 GOOD SURVIVOR |
| Low Score | 💀 BETTER LUCK NEXT TIME |

---

# 🚀 Future Improvements

- Difficulty scaling
- AI-generated scenarios
- Animated object cards
- Mobile support
- Voice input
- Story mode
- Save progress feature

---

# 📜 License

This project is free to use and modify for learning purposes.

---

# Tech Stack

Developed using Python and Tkinter.