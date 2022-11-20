import time
import random
class Tile:
    def __init__(self, app, col, height):
        self.app = app
        self.column = col #column the tile is in
        if col == 0:
            self.color = 'black'
        elif col == 1:
            self.color = 'black'
        else:
            self.color = 'black'


        self.x1 = app.tileBarXPos[col]
        self.y1 = -400 #to start generating above the screen
        self.x2 = app.tileBarXPos[col+1]
        self.y2 = height-400

        #self.fired = fire #time to fire

        #self.startTime = time.time()
        self.isActive = False
        self.state = 'not clicked'

    def __repr__(self):
        col = self.column
        return f"Tile({col})"
    
    def changeActivityState(self):
        self.isActive = not self.isActive

    
    def moveTile(self, dy=10):
        if self.isActive:
            self.y1 += dy
            self.y2 += dy

    def drawTile(self, app, canvas):
        if self.isActive:
            canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color)


    def hasReachedBottom(self):
        return (self.y1 > self.app.height)
