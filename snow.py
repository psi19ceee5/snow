#!/usr/bin/env python3

import sys
import shutil
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
import random as rnd
import time

def get_random_result(density: float) :
    return rnd.random() < density

class snowflake :
    def __init__(self, x, y) :
        self.melted = False
        self._pos = np.array([x, y])

    def x(self) :
        return self._pos[0]

    def y(self) :
        return self._pos[1]

    def fall(self, ymax) :
        self._pos += np.array([0, 1])
        if self._pos[1] + 1 > ymax :
            self.melted = True
    

class snowfield :
    ncol, nrow = shutil.get_terminal_size((50,20))
    snow_density = 0.01
    snowman_density = 0.1

    def __init__(self) :
        self._snowflakes = []
        self._field = np.empty(shape=(self.nrow, self.ncol), dtype=object)
        self._field.fill(" ")
        for row in range(self.nrow - 1) :
            for col in range(self.ncol) :
                if get_random_result(self.snow_density) :
                    self._field[row][col] = '❄'
                    self._snowflakes.append(snowflake(col, row))
        for col in range(self.ncol) :
            if get_random_result(self.snowman_density) :
                self._field[self.nrow - 1][col] = '☃'
            else :
                self._field[self.nrow - 1][col] = '_'

    def let_it_snow(self) :
        for row in range(self.nrow - 1) :
            for col in range(self.ncol) :
                self._field[row][col] = ' '
        
        for flake in self._snowflakes :
            flake.fall(self.nrow - 2)
            if flake.melted :
                self._snowflakes.remove(flake)
            self._field[flake.y(), flake.x()] = '❄'

        for col in range(self.ncol) :
            if get_random_result(self.snow_density) :
                self._field[0][col] = '❄'
                self._snowflakes.append(snowflake(col, 0))

        print(len(self._snowflakes))
                
    def __str__(self) :
        print("\033[" + str(self.nrow + 3) + "A")
        for row in range(self.nrow) :
            for col in range(self.ncol) :
                print(self._field[row][col], end='')
            print('')
        return ' '
                               

def main() :
    sf = snowfield()
    print(sf)

    while True :
        time.sleep(1)
        sf.let_it_snow()
        print(sf)
    
    
if __name__ == "__main__" :
    main()
