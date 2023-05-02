# Flock Simulation

An implementation of the boids algorithm in pygame to simulate the movement of birds in a flock.

![image](https://user-images.githubusercontent.com/90102914/230254148-dd3704bb-389d-4d7e-83b3-e6a8ebf73c7b.png)

* Red circles represent birds that use the boids algorithm to flock with each other.
* Blue circles represent obstacles in their environment, like a tree or a cliff.
* Green circles represent rogue birds that do not follow the boids algorithm but can influence other birds that do.

The flock of birds mostly follow a simple set of rules
* Find the average position of nearby birds to locate which position they are to travel to be in sync with the other birds.
* Moving away from nearby birds to ensure no collision/bumping occurs.
* Finding average velocity of the birds to ensure other birds don't go too fast or too slow when compared to its fellow flockmates.
* Avoiding the edges of the screen.
* Capping the speed limit of the birds to ensure birds don't go too fast.

Other functionalities included
* Avoiding obstacles present in the screen.