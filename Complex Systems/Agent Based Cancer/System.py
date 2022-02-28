import numpy as np
import pygame
from pygame.locals import *
import matplotlib.pyplot as plt


## TODO: Showing the results dynamically on the canvas or on another window

class System:

    def __init__(self, screen):
        self.resolution = 5
        self.rows = int(screen.get_width() / self.resolution)
        self.columns = int(screen.get_height() / self.resolution)
        self.screen = screen

        y = np.arange(-int(self.rows/2), int(self.rows/2))
        x = np.arange(-int(self.columns/2), int(self.columns/2))

        self.X,self.Y = np.meshgrid(x,y)
        self.popMat = np.zeros((self.rows, self.columns))
        self.typeMat = np.zeros((self.rows, self.columns), dtype='uint8') ## 0,1,2 (core-mantle-surface)
        self.ageMat = np.zeros((self.rows, self.columns))

        self.colors = [(102, 102, 51), (0, 153, 204), (255, 153, 102), (0,0,0),(255,255,255)]
        self.penColor = self.colors[-1]  ## -1 --> white, -2 --> Black

        self.initMats()

        #self.popMat = np.random.randint(2, size=(self.rows, self.columns))

        #self.popMat[10*np.sin(X/5)+Y > 0] = 1

        # for i in range(2):
        #     centers = (np.random.randint(x[0],x[-1]), np.random.randint(y[0],y[-1]))
        #     self.popMat[(X-centers[0])**2 + (Y-centers[1])**2 <40] = 1



    def initMats(self):
        center = [0,0]
        R0 = 160
        R1= R0*3
        R2 = R1*2
        self.popMat[(self.X - center[0]) ** 2 + (self.Y - center[1]) ** 2 < R2] = 1

        self.typeMat[(self.X - center[0]) ** 2 + (self.Y - center[1]) ** 2 < R2] = 2
        self.typeMat[(self.X - center[0]) ** 2 + (self.Y - center[1]) ** 2 < R1] = 1
        self.typeMat[(self.X - center[0]) ** 2 + (self.Y - center[1]) ** 2 < R0] = 0

    def renderMatToBuffer(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.popMat[i,j] == 0:
                    color = (0,0,0)
                else:
                    color = self.colors[self.typeMat[i,j]]
                pygame.draw.rect(self.screen, color,
                                 (i * self.resolution, j * self.resolution, self.resolution-1, self.resolution-1))

    def update(self):
        self.gameOfLife()


    def mouseDrawEventLoop(self, event):
        left, middle, right = pygame.mouse.get_pressed()

        if left:
            pos = pygame.mouse.get_pos()
            i = pos[0]//self.resolution
            j = pos[1]//self.resolution
            self.popMat[i,j] = 1
            pygame.draw.rect(self.screen, self.penColor,
                             (i * self.resolution, j * self.resolution, self.resolution - 1,
                              self.resolution - 1))
        if right:
            pos = pygame.mouse.get_pos()
            i = pos[0]//self.resolution
            j = pos[1]//self.resolution
            self.popMat[i,j] = 1
            pygame.draw.rect(self.screen, self.colors[-2],
                             (i * self.resolution, j * self.resolution, self.resolution - 1,
                              self.resolution - 1))
        if middle:
            self.popMat *= 0
            self.renderMatToBuffer()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                self.penColor = self.colors[0]
            if event.key == pygame.K_1:
                self.penColor = self.colors[1]
            if event.key == pygame.K_2:
                self.penColor = self.colors[2]
            if event.key == pygame.K_w:
                self.penColor = self.colors[-1]





    def TumorGrowth(self):
        self.ageMat
        self.typeMat
        self.popMat = self.popMat




    def gameOfLife(self):   ## By using this update rule you will have the game of life simulation
        mat1 = np.roll(np.roll(self.popMat, -1, axis=0), -1, axis=1)
        mat2 = np.roll(self.popMat, -1, axis=0)
        mat3 = np.roll(np.roll(self.popMat, -1, axis=0), 1, axis=1)
        mat4 = np.roll(self.popMat, 1, axis=1)
        mat5 = np.roll(np.roll(self.popMat, 1, axis=0), 1, axis=1)
        mat6 = np.roll(self.popMat, 1, axis=0)
        mat7 = np.roll(np.roll(self.popMat, 1, axis=0), -1, axis=1)
        mat8 = np.roll(self.popMat, -1, axis=1)

        result = mat1 + mat2 + mat3 + mat4 + mat5 + mat6 + mat7 + mat8

        self.popMat[(result == 2) + (result == 3)] *= 1
        self.popMat[(result == 3)] = 1
        self.popMat[(result != 2) * (result != 3)] = 0  ## !((result==2)+(result==3))

        self.renderMatToBuffer()





