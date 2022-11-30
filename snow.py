#!/usr/bin/env python3

import sys
import shutil
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
import random as rnd
import time
import abc
from abc import ABC, abstractmethod

def get_random_result(density: float) :
    return rnd.random() < density
            
class field :
    @abstractmethod
    def __init__(self) :
        self._field = np.empty(shape=(self.nrow, self.ncol), dtype=object)
        self._field.fill(" ")
        self._pos = np.array([0,0])
        
    def x(self) :
        return self._pos[0]

    def y(self) :
        return self._pos[1]

class snowflake(field) :
    ncol = 1
    nrow = 1
    
    def __init__(self, x, y) :
        super().__init__()
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
            
class santa(field) :
    ncol = 42
    nrow = 4
    
    _row1 = "                                   _ ,.W, "
    _row2 = " \)      \)      \)      \)       {\\'* , ;"
    _row3 = "c(/'--,  (/'--,  (/'--,  (/'--,  c_)(___,'"
    _row4_0 = "  <| |\   /| <|   <\ /|   <| |\ (_\____/__"
    _row4_1 = "  /| <|   <\ /|   /| <|   /| <\ (_\____/__"
    
    def __init__(self, x, y) :
        super().__init__()
        self._pos = np.array([x,y])
        self._stance = 0
        self.vanished = False
        
        self._field[0,:] = np.array(list(self._row1))
        self._field[1,:] = np.array(list(self._row2))
        self._field[2,:] = np.array(list(self._row3))
        self._field[3,:] = np.array(list(self._row4_0))
        
    def ride(self) :
        self._pos[0] -= 3
        self._stance = (self._stance+1) % 2
        if self._stance == 0 :
            self._field[3,:] = np.array(list(self._row4_0))
        if self._stance == 1:
            self._field[3,:] = np.array(list(self._row4_1))
        if self._pos[0] <= -self.ncol :
            self.vanished = True
        
    def get_field(self) :
        return self._field
    
class snowfield(field) :
    ncol, nrow = shutil.get_terminal_size((50,20))
    nrow -= 2
    snow_density = 0.01
    snowman_density = 0.1
    santa_prob = 0.02

    def __init__(self) :
        self._snowflakes = []
        self._santa = []
        super().__init__()
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
        nrow_sky = self.nrow - 1
        
        for row in range(nrow_sky) :
            for col in range(self.ncol) :
                self._field[row][col] = ' '

        # snow falls and old snow melds
        for flake in self._snowflakes :
            flake.fall(nrow_sky)
            if flake.melted :
                self._snowflakes.remove(flake)
            else :
                self._field[flake.y(), flake.x()] = '❄'
                
        # santa rides along
        for san in self._santa :
            san.ride()
            if san.vanished :
                self._santa.remove(san)
            else :
                santafield = san.get_field()
                rows, cols = np.shape(santafield)
                for col in range(cols) :
                    for row in range(rows) :
                        col_ = san.x() + col
                        row_ = san.y() + row
                        if col_ < len(self._field[0,:]) and col_ >= 0 and row_ < len(self._field[:,0]) and row_ >= 0 :
                            self._field[row_][col_] = santafield[row][col]

        # make some fresh snow
        for col in range(self.ncol) :
            if get_random_result(self.snow_density) :
                self._field[0][col] = '❄'
                self._snowflakes.append(snowflake(col, 0))
        
        # ask if santa wants to come
        if len(self._santa) == 0 and get_random_result(self.santa_prob) :
            if self.nrow < 6 or self.ncol < 50 :
                pass
            y_start = rnd.randint(1,self.nrow-5)
            self._santa.append(santa(self.ncol, y_start))
                
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
        time.sleep(0.5)
        sf.let_it_snow()
        print(sf)
    
    
if __name__ == "__main__" :
    main()
