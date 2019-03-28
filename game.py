# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:12:39 2019

@author: Paul Jasek
"""

import cv2
import numpy as np
import random

class Block(object):
    def __init__(self, x, y, w, h, c):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
    
    def render(self, image):
        cv2.rectangle(image,
                      (round(self.x - self.w/2), round(self.y - self.h/2)),
                      (round(self.x + self.w/2) - 1, round(self.y + self.h/2) - 1),
                      self.c,
                      thickness=-1)

class Game(object):
    def __init__(self, config, W=10, H=10):
        self.W = W
        self.H = H
        self.config = config
        self.action_size = 3
    
    def new_random_game(self):
        self.player = Block(self.W/2 + 0.5, self.H - 1, 1, 2, (0,0,0))
        self.blocks = []
        self.time = 0
        self.terminal = False
        return self.render(), 0, 0, self.terminal
    
    def act(self, action):
        assert not self.terminal
        
        reward = 0
        
        self.time += 1
        if action == 1:
            if self.player.x - 1 >= 0:
                self.player.x -= 1
        if action == 2:
            if self.player.x + 1 <= self.W:
                self.player.x += 1
        
        for i in range(len(self.blocks) - 1, -1, -1):
            block = self.blocks[i]
            block.y += 1
            if abs(block.x - self.player.x) < (block.w/2 + self.player.w/2) \
                and abs(block.y - self.player.y) < (block.h/2 + self.player.h/2):
                    self.terminal = True
                    reward = -1
            elif block.y - block.h/2 >= self.H:
                self.blocks.pop(i)
        
        if self.time % (1 + int(5*np.exp(-self.time/200))) == 0:
            self.blocks.append(Block(random.randint(1,self.W) - 0.5, 0.5, 1, 1, (1, 0, 0)))
        
        
        return self.render(), reward, self.terminal
        
    
    def render(self):
        image = np.ones((self.W, self.H, 3))
        self.player.render(image)
        for block in self.blocks:
            block.render(image)
        
        return image

if __name__ == '__main__':
    UP = 2490368
    DOWN = 2621440
    LEFT = 2424832
    RIGHT = 2555904
    
    game = Game(None)
    screen, reward, action, terminal = game.new_random_game()
    
    while True:
        cv2.imshow('test', cv2.resize(screen, (500, 500), interpolation=cv2.INTER_NEAREST))
        if game.terminal:
            break
    
        key = cv2.waitKey(100)
        
        action = 0
        if key == LEFT:
            action = 1
        elif key == RIGHT:
            action = 2
        else:
            action = 0
            
        screen, reward, terminal = game.act(action)
        
        
    cv2.waitKey(0)
    cv2.destroyAllWindows()