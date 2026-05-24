# 🧠 Memory Survival

An intense, endless tactical recall game built with **Pygame**. Players are challenged to memorize a shifting grid of equipment cards under strict time constraints before resolving procedurally generated multi-hazard survival emergencies.

The game features dynamic layout scaling, automated text wrapping, and an integrated audio synthesizer engine that scales intensity alongside your round progression.

---

## 🎮 Key Features

* **Infinite Procedural Rounds:** No pre-baked levels. The game dynamically selects environmental hazards and builds completely unique crisis prompts in real time.
* **Adaptive Difficulty Scale:** As you advance, card grid density ramps up from a 3x2 matrix (6 items) all the way up to a frantic 4x3 layout (12 items), while memorization windows contract down to a tense 5 seconds.
* **Flexible Input Verification:** The internal system console accepts any one valid solution to the active crisis. Input matching strictly neutralizes capitalizations, trailing pads, and spacing errors automatically.
* **Immersive Home Menu & UI:** Built-in interactive home dashboard containing a comprehensive instruction manual panel alongside a global audio toggle button.
* **Zero Asset Audio Engine:** Generates synthesized background low-tension synth tracking arrays, warnings, clock ticks, and pass/fail alert tones entirely on-the-fly using mathematical audio frequencies. (No heavy `.mp3` or `.wav` dependencies required).

---

## 🛠️ Installation & Setup

### Prerequisites
Make sure you have Python 3.10+ installed on your operating system.

### 1. Clone or Create your Project Directory
```bash
mkdir MemorySurvival
cd MemorySurvival
```

### 2. Install Dependencies
Install the latest stable distribution of Pygame:
```bash
pip install pygame
```

### 3. Add the Asset Art
Place your preferred backdrop image asset inside the root game directory named exactly:
* `background.jfif` *(The game will automatically default to a high-contrast dark space background fallback if this file is not found).*

### 4. Deploy your Game Script
Save your game source code as `survivor.py` in the root folder.

### 5. Execute Code
Launch the simulator directly via your console interface terminal:
```bash
python survivor.py
```

---

## 🕹️ Instructional Manual

1. **Memorize the Grid:** Analyze item distribution matrices immediately upon round startup before your countdown timer hits `00`.
2. **Interpret the Crisis:** Once time drops to zero, read the emergency message prompt carefully.
3. **Deploy a Response Tool:** Type precisely **ONE** tool name from memory into the command console box and hit `Enter`. 
4. **Learn on Failure:** If you guess incorrectly, the console frame flashes red and exposes the valid tool combinations you missed. Press `Spacebar` to advance onto the final evaluation scoreboard.

---

## 🏗️ System Architecture & Code Execution Flow

The software pattern operates entirely on a single-file core state machine matrix logic structure to preserve processing thresholds:

* **State Manager Routing Matrix:** Controls active windows flawlessly between `MENU`, `HOW_TO`, and `PLAYING` states based on interactive mouse collision points.
* **`render_wrapped_text()` Engine:** Protects font rendering boundaries. Long generated sentence structures automatically split into pixel-measured rows to prevent screen cutting across all monitor display scales.
* **`generate_dynamic_round()` Module:** Harvests data pools, constructs random emergency strings using string splitting parameters, and translates tool objects to raw index keys.