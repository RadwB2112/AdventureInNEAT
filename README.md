# <p align="center"> 🚀 Realistic Ship Simulator with AI & NEAT 🚀  </p> 


**Adventure in NEAT / Space** is an experimental and interactive project where a spaceship learns how to **land safely on a platform** using **neuroevolution**!  

---  
## <p align="center"> Project Overview </p>
This project is a **realistic 2D spaceship simulator** powered by **real physics** and **neuroevolution (NEAT)**.  
I implemented **continuous physics**, including thrust, rotation, gravity, drag, and realistic black hole attraction, combined with **AI-driven neural networks** to evolve autonomous ships that learn to navigate and land safely.  

The project spans **~1500 lines of code** and was built to simulate real-life physics as closely as possible while providing an **AI training environment** with **hands-on control**.  
It’s also a **remake of an older version**, where you could only manually navigate the ship through blank space with nothing else. This remake allows exploration of **neuroevolution** and interactive AI learning.

> please note that some parts of the code contain comments and words in Romanian, mostly because I started this project as a kid and it was easier to understand the code that way.  

## <p align="center"> Features  </p> 

- **AI Learning with NEAT:** Ships evolve over generations to land safely using fitness-based rewards.
- **Manual Control Mode:** Navigate the ship yourself with smooth thrust and rotation physics.
- **Realistic Physics:** Continuous thrust, rotation, gravity, drag, and black hole attraction.
- **Interactive Black Holes:** Pull and rotate ships realistically, affecting both AI and manual gameplay.
- **Collision Detection:** Hand-coded collisions between ships and platforms for accurate physics.
- **Dynamic Reload System:**  
  - Press **`R` once** → reset your ship in manual mode or reset black hole positions.  
  - Press **`R` twice** → reload the entire project with new changes (works only in menu and pause).
- **Pause and Navigation:**  
  - Press **`4`** → pause the game.  
  - Press **`Space`** → move between pages in menu.  
  - In **Set black holes mode** (function: set_obstacles) :  
    - **`T`** → go to NEAT train mode.  
    - **`Space`** → go to manual navigation mode.  
    - **`B`** → show best genome’s landing path (after training).
- **Genome Fitness System:** Rewards are designed to encourage realistic AI behavior and landing:  
  ```text  
  DEAD_SHIP = 10             # ship died
  ONLY_UP_SHIP = 20          # penalize ships that just go up slowly
  SURVIVE_SHIP = 0.1         # small reward for surviving
  OVER_PLATFORM_SHIP = 5     # reward for being above platform
  LOW_VERT_SPEED_SHIP = 20   # reward for low vertical speed when above platform
  DONT_MOVE_SHIP = 15        # penalize ships that don’t move
  LAND_SHIP = 500            # reward for successfully landing
  BLACKHOLE_DIE_SHIP = 20    # penalty for dying in a black hole
  OUT_OF_SCREEN_SHIP = 30    # penalty for going out of screen
  INSIDE_BHS_SHIP = 0.2      # small penalty for being inside the radius of the black hole 
- **Dynamic Background with Stars:**  
  - **Normal stars**: Two colors, appear and disappear randomly to simulate a twinkling sky.  
  - **Falling stars**: Two categories — bright white shooting stars and meteorites — adding a **realistic space environment** while ships navigate and train.  


## <p align="center"> Technologies Used </p>  
  ```text
- Python 3.11.5 
- Pygame – Graphics, physics, and input handling
- NEAT-Python – Neuroevolution for AI-controlled ships
- Object-Oriented Programming (OOP) – Modular classes for stars, ships, platforms, and black holes
- Git – Version control for project management
```  

## <p align="center"> Installation & Running </p>

1. **Clone the repository**
```bash
git clone https://github.com/RadwB2112/AdventureInNEAT | cd AdventureInNEAT
```
2. **Install all the packages**
```bash
pip install -r requirements.txt
```
3. **Run and enjoy the game**
```bash
python main.py
```

## <p align="center"> Customization & Configuration </p>

This project is designed to be **highly configurable**. You can experiment with AI, ship, and environment parameters by only changing some values.

### NEAT Configuration
- Edit **`config_neat.txt`** to modify:
  - Population size
  - Number of generations
  - Mutation rates
  - Crossover probability
- This allows you to influence **how fast AI evolves** and the **complexity of neural networks**.

### Ship Parameters
- Ship physics parameters are defined in the **ship class**:
  - Thrust, acceleration, rotation speed
  - Gravity and drag factors
- Adjust these values to see how AI behavior changes or for **manual navigation testing**.

### Environment / Obstacles
- Black hole positions, size, and attraction strength can be edited in **set_obstacles**.
- Falling stars, meteorites, and platform positions can also be customized.

> **Tip:** After making changes, use the **double `R` reload function in MENU** to apply them without restarting the project.

