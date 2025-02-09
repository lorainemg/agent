# Agent Simulation

This project simulates agents interacting within a dynamic environment, modeled as a discrete NxM grid. The environment contains various elements such as obstacles, dirt, children, a barnyard, and house robots (agents). The simulation operates in discrete time steps, with both agents and the environment undergoing changes over time.

## Table of Contents

- [Introduction](#introduction)
- [Environment Elements](#environment-elements)
- [Simulation Dynamics](#simulation-dynamics)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

The simulation aims to model the interactions between agents and a changing environment. The environment is fully observable, meaning all information about it is known to the agents. Changes in the environment occur at regular intervals, and agents perform actions in turn, modifying the environment accordingly.

## Environment Elements

The environment consists of the following elements:

- **Obstacles**: Occupy a single cell in the grid. Children can push obstacles one cell at a time.
- **Dirt**: Can appear in any empty cell, either initially or as a result of children's actions.
- **Children**: Move within the environment and can push obstacles, creating dirt in the process.
- **Barnyard**: A designated area within the grid.
- **House Robots (Agents)**: Tasked with cleaning dirt and managing the environment.

## Simulation Dynamics

- **Time Steps**: The simulation progresses in discrete time units. Each unit comprises two phases:
  1. **Agent Actions**: Each agent performs one action, modifying the environment.
  2. **Environment Changes**: The environment may change randomly every `t` time units, where `t` is a known parameter.

## Objectives

The goal of the Robot is to keep the house clean. It is known that if the house reaches 60% dirty boxes the Robot is fired and the simulation immediately ceases. If the Robot places all the children in the pen and 100% of the boxes are clean, the simulation also stops. These are called the final states.

The objective of this project is to program the behavior of the robot for each turn, as well as the possible variations of the environment.

## Installation

To set up the project locally:

1. **Clone the Repository**:

```bash
   git clone https://github.com/lorainemg/agent.git
   cd agent
```
2. Ensure Python 3.x is Installed: The simulation is implemented in Python.

## Usage
1. Navigate to the Source Directory:

```bash
cd src
```

2. Run the Simulation:

```bash
python simulation.py
```

3. Configuration: Modify the configuration parameters in the script to adjust the environment size (NxM), time interval t, and other settings as needed

## Reports

For more details, there's a full [report](https://github.com/lorainemg/agent/blob/main/doc/report.pdf) available.
