# 🌲 Wandering in the Woods

An **educational simulation game** designed to teach **problem-solving, spatial reasoning, and probability** to K-8 students through interactive wandering in a grid-based forest.

Built using **Pygame** for an engaging graphical experience.

---

## 🚀 Features

### ✅ Version 1.0.0
- 🎮 **Graphical Interface** – Built with Pygame for an interactive experience.
- 🏫 **Three Difficulty Levels**
  - **K-2:** Simple mechanics for younger students.
  - **3-5:** Customizable grid sizes, player placement, and movement tracking.
  - **6-8:** Advanced mechanics with statistics and wandering mode selection.
- 🎭 **2-4 Players** – Players are placed manually on the grid.
- 🔄 **Random Movement Simulation** – Players wander randomly within the forest.
- 📊 **Run Statistics Tracking** – Records longest run, shortest run, and average run.

---

## 📦 Installation

### Prerequisites
- Python 3.0+
- Pygame
- Pygame_menu

### Clone the Repository
```bash
git clone https://github.com/AaronMatayka/WanderingWoodsGame.git
cd WanderingWoodsGame
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Game
```bash
python simulation.py
```

---

## 🛠️ Building an Executable
To build a standalone executable using **PyInstaller**, run the following command:
```bash
pyinstaller -w -F --add-data "./music.wav;." --add-data "./happy.png;." --log-level=WARN simulation.py --target-architecture universal2
```
This will generate an executable file that can be distributed without requiring Python.

---

## 🕹️ How to Play
1. Choose a difficulty level (K-2, 3-5, or 6-8).
2. Set up the grid and place 2-4 players.
3. Players move randomly based on their respective rules.
4. Track movement statistics after each run.

---

## 🏆 Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit changes and push.
4. Submit a pull request.

---

## 📬 Contact
Maintainers:
- **Aaron Matayka**  
  GitHub: [AaronMatayka](https://github.com/AaronMatayka)  
- **Andrew Matayka**  
  GitHub: [AndrewMatayka](https://github.com/AndrewMatayka)  

---

Happy Wandering! 🌲✨
