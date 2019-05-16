# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:41:39 2019

@author: Noah Dong
"""
import pygame

class Hero(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self._sur = surface