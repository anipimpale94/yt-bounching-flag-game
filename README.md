# chaos-balls

A Simulation of balls bouncing around in a circular ring, inspired by a [Numberphile video](https://youtu.be/6z4qRhpBIyA) on chaotic systems. The simulation demonstates how chaos and complexity arises from something as simple as balls bouncing in a ring. Written in python3, pygame, and designed with a modular Object-Oriented architecture.

## Requirements

- [python 3.9](https://www.python.org/downloads/release/python-397/)

Install these packages using pip:

- pygame. preferably version 2.0.1

```
pip install pygame -V 2.0.1
```

## Run

Simply run the chaos_balls.py file either by double clicking it or running the following command in the terminal
~~~
python3 chaos_balls.py
~~~

## Features

To Add/Remove balls and manipulate their properties, i.e velocity, position, etc you can do so by opening chaos_balls.py in a text editor and follow the instructions around line 150. Will make this more user friendly in the future but for now just mess around with the source code.

### Architecture

The project follows a modular structure:
- `game_object.py`: Defines the `GameObject` abstract base class.
- `ball.py`: Contains the `Balls` class which implements `GameObject`.
- `chaos_balls.py`: The main entry point and game loop.
- `utils.py`: Helper functions for math and physics.

### Example Usage

First we will create the object:

```python
redball_test = Balls(name="test", color=(255, 0, 0), radius=8, thicc=0, posx=200, posy=300)
```

Arguments for `Balls` class:

- `name`: name of the ball (str)
- `color`: (r,g,b) tuple
- `radius`: float or int
- `thicc`: outline thickness (0 for solid)
- `posx`, `posy`: initial position
- `sound`: (optional) collision sound file in audio/ folder

## Controls

- Spacebar: Pause/Resume
- TAB: Start game from intro screen
- T: Toggle trail

That's about it!
