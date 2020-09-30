#!/usr/bin/env python3
from paint import paint
import sys
from time import sleep
import numpy as np
"""
# Sample format to answer pattern questions 
# assuming the pattern would be frag0:
..*
**.
.**
#############################################
# Reread the instructions for assignment 1: make sure
# that you have the version with due date SUNDAY.
# Every student submits their own assignment.
* Delete the names and ccids below, and put
# the names and ccids of all members of your group, including you. 
# name                         ccid
Nguyen Vu                    nhvu
Cameron Hildebrandt          childebr
Sandy Huang                  sandy6
Susan Trang                  ngocthao
Alex Chan                    achan2

#############################################
# Your answer to question 1-a:
The pattern that needs unbounded grid for the whole simulation is referred to as "glider" since the gliding "group oscillates and moves 
itself upon the board in cyclic movement. For its tendency to move forever, the board needs to be unbounded.


#############################################
# Your answer to question 1-b:
The pattern is simply referred as "Gosper Glider Gun", which is a finte pattern with unbounded growth. It allows for the generation of "gliding" group to form and leaves a trail of still lifes, and creates unbounded growth of cells.


#############################################
# Your answer to question 2:
- num_nbrs in life-np.py is combined with next_state function to generate a numpy array instead of a string. While num_nbrs is used to check the states of neighbors,
next_state in life-np.py contains double for loops to keep track of that.
- An infinite grid is implemented in life.py by checking for cells that have one open space before bumping into the guards or to the right then pushes
the guard rows or column away from the cells.
- Because num_brs checks the states of 8 neighbors of each cells, with num_nbrs we do not have to do extra work of testing the bounds if any cells on the leftmost/ rightmost/ 
top/ bottom of the board


#############################################
# Follow the assignment 1 instructions and
# make the changes requested in question 3.
# Then come back and fill in the answer to
# question 3-c:
After 255 iterations, the alive cells that we got are at positions [0,10],[1,8],[1,9],[1,10] and [4,9].


#############################################
"""
"""
based on life-np.py from course repo
"""


PTS = '.*#'
DEAD, ALIVE, WALL = 0, 1, 2
DCH, ACH, GCH = PTS[DEAD], PTS[ALIVE], PTS[WALL]


def point(r, c, cols): return c + r*cols

"""
board functions
  * represent board as 2-dimensional array
"""


def get_board():
    B = []
    print(sys.argv[1])
    with open(sys.argv[1]) as f:
        for line in f:
            B.append(line.rstrip().replace(' ', ''))
        rows, cols = len(B), len(B[0])
        for j in range(1, rows):
            assert(len(B[j]) == cols)
        return B, rows, cols


def convert_board(B, r, c):  # from string to numpy array
    A = np.zeros((r, c), dtype=np.int8)
    for j in range(r):
        for k in range(c):
            if B[j][k] == ACH:
                A[j, k] = ALIVE
    return A


def expand_grid(A, r, c, t):  # add t empty rows and columns on each side
    N = np.zeros((r+2*t, c+2*t), dtype=np.int8)
    for j in range(r):
        for k in range(c):
            if A[j][k] == ALIVE:
                N[j+t, k+t] = ALIVE
    return N, r+2*t, c+2*t


def print_array(A, r, c):
    print('')
    for j in range(r):
        out = ''
        for k in range(c):
            out += ACH if A[j, k] == ALIVE else DCH
        print(out)


def show_array(A, r, c):
    for j in range(r):
        line = ''
        for k in range(c):
            line += str(A[j, k])
        print(line)
    print('')


""" 
Conway's next-state formula
"""


def next_state(A, r, c):
    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            num = 0
            if j > 0 and k > 0 and A[j-1, k-1] == ALIVE:
                num += 1
            if j > 0 and A[j-1, k] == ALIVE:
                num += 1
            if j > 0 and k < c-1 and A[j-1, k+1] == ALIVE:
                num += 1
            if k > 0 and A[j, k-1] == ALIVE:
                num += 1
            if j > 0 and k < c-1 and A[j, k+1] == ALIVE:
                num += 1
            if j < r-1 and k > 0 and A[j+1, k-1] == ALIVE:
                num += 1
            if j < r-1 and A[j+1, k] == ALIVE:
                num += 1
            if j < r-1 and k < c-1 and A[j+1, k+1] == ALIVE:
                num += 1
            if A[j, k] == ALIVE:
                if num > 1 and num < 4:
                    N[j, k] = ALIVE
                else:
                    N[j, k] = DEAD
                    changed = True
            else:
                if num == 3:
                    N[j, k] = ALIVE
                    changed = True
                else:
                    N[j, k] = DEAD
    return N, changed


#############################################
""" 
Provide your code for the function 
next_state2 that (for the usual bounded
rectangular grid) calls the function num_nbrs2,
and delete the raise error statement:
"""


def next_state2(A,r,c):
    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            nbrs = num_nbrs2(A, r, c, j, k)   
            if A[j,k] == ALIVE:
                if nbrs > 1 and nbrs < 4:
                    N[j,k] = ALIVE
                else:
                    N[j,k] = DEAD
                    changed = True
            else:
                if nbrs == 3:
                    N[j,k] = ALIVE
                    changed = True
                else: 
                    N[j,k] = DEAD
    
    return N, changed

#############################################


#############################################
""" 
Provide your code for the function 
num_nbrs2 here and delete the raise error
statement:
"""


def num_nbrs2(A, r, c, j, k):
    num = 0
    if j > 0 and k > 0 and A[j-1, k-1] == ALIVE:
        num += 1
    if j > 0 and A[j-1, k] == ALIVE:
        num += 1
    if j > 0 and k < c-1 and A[j-1, k+1] == ALIVE:
        num += 1
    if k > 0 and A[j, k-1] == ALIVE:
        num += 1
    if j > 0 and k < c-1 and A[j, k+1] == ALIVE:
        num += 1
    if j < r-1 and k > 0 and A[j+1, k-1] == ALIVE:
        num += 1
    if j < r-1 and A[j+1, k] == ALIVE:
        num += 1
    if j < r-1 and k < c-1 and A[j+1, k+1] == ALIVE:
        num += 1

    return num

#############################################


#############################################
""" 
Provide your code for the function 
next_state_torus here and delete the raise 
error statement:
"""


def next_state_torus(A, r, c):
    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            nbrs = num_nbrs_torus(A, r, c, j, k)
            if A[j,k] == ALIVE:
                if nbrs > 1 and nbrs < 4:
                    N[j,k] = ALIVE
                else:
                    N[j,k] = DEAD
                    changed = True
            else:
                if nbrs == 3:
                    N[j,k] = ALIVE
                    changed = True
                else: 
                    N[j,k] = DEAD
    
    return N, changed
#############################################


#############################################
""" 
Provide your code for the function 
num_nbrs_torus here and delete the raise 
error statement:
"""


def num_nbrs_torus(A, r, c, j, k):
    num = 0

    if A[(j-1)%r, (k-1)%c] == ALIVE:
        num += 1
    if A[(j-1)%r, k] == ALIVE:
        num += 1
    if A[(j-1)%r, (k+1)%c] == ALIVE:
        num += 1
    if A[j, (k-1)%c] == ALIVE:
        num += 1
    if A[j, (k+1)%c] == ALIVE:
        num += 1
    if A[(j+1)%r, (k-1)%c] == ALIVE:
        num += 1
    if A[(j+1)%r, k] == ALIVE:
        num += 1
    if  A[(j+1)%r, (k+1)%c] == ALIVE:
        num += 1

    return num


#############################################


"""
input, output
"""

pause = 0.2

#############################################
""" 
Modify interact as necessary to run the code:
"""
#############################################


def interact(max_itn):
    itn = 0
    B, r, c = get_board()
    print(B)
    X = convert_board(B, r, c)
    A, r, c = expand_grid(X, r, c,0)
    print_array(A, r, c)
    while itn <= max_itn:
        sleep(pause)
        newA, delta = next_state_torus(A, r, c)
        if not delta:
            break
        itn += 1
        A = newA
        print_array(A, r, c)
    print('\niterations', itn)


def main():
    interact(255)


if __name__ == '__main__':
    main()
