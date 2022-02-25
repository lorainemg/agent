# Simulation Agents

The environment in which the agents interact is discrete and has the shape of an NxM rectangle. It is complete information, therefore all the information about it is known. The environment can vary randomly every `t` units of time, the value of t is known.

Actions performed by agents occur in turns. In one turn, the agents carry out their actions, only one for each agent, and modify the environment without it changing. In the next, the atmosphere may vary. In a unit of time, the agent's turn and the environment change turn occur.

## Description of the elements of the environment

The elements that can exist in the environment are obstacles, dirt, children, the barnyard and the agents that are called House Robots. The characteristics of the environment elements are specified below:

- **Obstacles:** These occupy a single space in the environment. They can be moved, by pushing them, by the children, a single square.

- **Dirt:** the dirt is for each space in the environment. It can only appear on cells that were previously empty. This either appears in the initial state or is created by the children.

- **Corral:** the corral occupies adjacent squares in a number equal to the total number of children present in the environment. The pen cannot move. Only one child can coexist in a corral box. In a space of the corral, that is empty, a robot can enter.

- **Child:** Children occupy only one space. They in the turn of the environment move, if possible, and randomly, to one of the adjacent squares. If that square is occupied by an obstacle, it is pushed by the child, if there is more than one obstacle in the direction, then they all move. If the obstacle is in a position where it cannot be pushed and the child tries to push it, then the obstacle does not move and the child occupies the same position.

  Children are responsible for the appearance of dirt. If in a 3 by 3 grid there is only one boy, then after he moves randomly, one of the squares of the previous grid that is empty may have been soiled. If there are two children, up to 3 can get dirty. If there are three or more children, up to 6 can get dirty. If the child does not move, the decision was made that no dirt is generated.

  The children, when they are in a square of the corral, do not move or dirty and if a child is captured by a House Robot, they do not move or dirty either.

- **House Robot:** The House Robot is in charge of cleaning and controlling the children. The Robot moves to one of the adjacent squares, whichever you decide. It only moves one square if it does not carry a child. If you carry a child you can move up to two consecutive squares. You can also perform the actions of cleaning and carrying children. If he moves to a dirty space, on the next turn he can decide to clean or move. If he moves to a space where a child is, he immediately charges that child. At that time, Robot and child coexist in the box.

  If he moves to a space in the pen that is empty, and picks up a child, he can decide whether to leave this space or continue moving. The Robot can leave the child it is carrying in any space. At that moment, the movement of the Robot stops in the turn, and Robot and child coexist until the next turn, in the same square.

## Objectives

The goal of the Robot is to keep the house clean. It is known that if the house reaches 60% dirty boxes the Robot is fired and the simulation immediately ceases. If the Robot places all the children in the pen and 100% of the boxes are clean, the simulation also stops. These are called the final states.

The objective of this project is to program the behavior of the robot for each turn, as well as the possible variations of the environment.