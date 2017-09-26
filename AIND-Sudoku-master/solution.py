assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    
    #The loop running as long as the values dictionary keep changing
    there_are_twins = True #sentinel
    while there_are_twins:
        initial_board = values.copy() #saving copy for comparison purpose
        potential_twins = [box for box in values.keys() if len(values[box]) == 2] #collection of all boxes with two possibilties
        #naked twins collection
        naked_twins = [[box1, box2] for box1 in potential_twins for box2 in peers[box1] if set(values[box1])==set(values[box2])]
        for pair in naked_twins:
            box1 = pair[0] #key of the first twin
            box2 = pair[1] # key of the second twin
            twin_peers = set(peers[box1]) & set(peers[box2]) # intersection of their peers
            for v in values[box1]: # loop over digits of the twins
                for aPeer in twin_peers: # loop over their twins
                        values=assign_value(values, aPeer, values[aPeer].replace(v, "")) 
        if initial_board == values: #checking if the dictionary has changed
            there_are_twins=False
            
    return values
                
def cross(A, B):
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
first_diagonal =[rows[i]+cols[i] for i in range(9)]
second_diagonal =[rows[-i-1]+cols[i] for i in range(9)]
unitlist = row_units + column_units + square_units + [first_diagonal] + [second_diagonal]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers =  dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits) #replacement of dot with all digits
        elif c in all_digits:
            values.append(c) #if the value called c already in digits then append to the values of the dictionary
    assert len(values) == 81
    return dict(zip(boxes, values)) #zipping values with their keys

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes) # width = 1+length of the maximal box in terms of its choices-values
    line = '+'.join(['-'*(width*3)]*3) # +---- repeated 3 times to get the grid
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1] #selecting all values of length equal to 1
    for box in solved_values:
        digit = values[box] #fetching the value of the box
        for peer in peers[box]: #looping over peers of the box
            values = assign_value(values, peer, values[peer].replace(digit,'')) # removing the digit from values of each peer
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist: # looping over each unit
        for digit in '123456789': # looping over digits
            dplaces = [box for box in unit if digit in values[box]] #collecting keys of boxes containing the digit
            if len(dplaces) == 1: # checking if the digit fits in only one box
                values[dplaces[0]] = digit #assigning the digit to the box
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the naked twins 
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # tranform the grid into dictionary
    values = grid_values(grid)
    # Reduce the possible values for each box
    values = reduce_puzzle(values)
    # Examine each path resulting from picking up each value from all that are possible for each box
    values = search(values)
    return values
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
