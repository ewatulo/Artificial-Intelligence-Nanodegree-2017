# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint Propagation is applied in the naked twins problem in the following way:
1. First, the naked twins are identified which means that two boxes having identical pair of choices (only 2 possible values) are found.
2. In order to narrow down possible solutions the following constraint is applied: none of the other boxes belonging to the naked twin pair's unit (being intersection of the twins' peers) can have either of the two values as choices. Thus, the two values are eliminated from possible solutions of the peers-boxes of the twins of their unit. 
3. After the above process, some boxes are solved (left with only one choice), while some may still have multiple values and thus, may create another naked twins pairs what leads to another iteration of the problem
4. Application (with iteration) of eliminate(), only_choice() and naked_twins() constitutes the constraint propagation part of the sudoku solver algorithm 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Constraint propagation is used in the diagonal sudoku problem as follows:
1. First, boxes belonging to the two diagonal units are identified. 
2. Then, in each of the methods: eliminate(), only_choice() and naked_twins() we take into account all the units, namely: rows, columns, squares and the two diagonals, thus we expand the space of conditions that must be considered while deciding upon a solution for a given box


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

