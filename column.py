import time
from tile import *
from helper import *

class Column:
    def __init__(self, app, colNumber):
        self.app = app
        self.colNumber = colNumber #0, 1, 2, 4
        self.tileNum = 8 ##arbitrary
        self.heightOptions = [app.height//8, app.height//5, app.height//2]
        #self.tiles = self.generateColumnTiles()

        self.colx0, self.colx1 = self.getXColPos()

        if colNumber == 0:
            self.tiles = {  10: Tile(self.app, self.colNumber, height=100), 
                            50: Tile(self.app, self.colNumber, height=100),
                            102: Tile(self.app, self.colNumber, height=100),
                            170: Tile(self.app, self.colNumber, height=100),
                            200: Tile(self.app, self.colNumber, height=100)
            }
        elif colNumber == 1:
            self.tiles = {  2: Tile(self.app, self.colNumber, height=100), 
                            44: Tile(self.app, self.colNumber, height=100),
                            143: Tile(self.app, self.colNumber, height=100),
                            50: Tile(self.app, self.colNumber, height=100),
                            250: Tile(self.app, self.colNumber, height=100)
            }
        elif colNumber == 2:
            self.tiles = {  10: Tile(self.app, self.colNumber, height=100), 
                            30: Tile(self.app, self.colNumber, height=100),
                            110: Tile(self.app, self.colNumber, height=100),
                            180: Tile(self.app, self.colNumber, height=100),
                            230: Tile(self.app, self.colNumber, height=100)
            }
        elif colNumber == 3:
            self.tiles = {  20: Tile(self.app, self.colNumber, height=100), 
                            49: Tile(self.app, self.colNumber, height=100),
                            15: Tile(self.app, self.colNumber, height=100),
                            370: Tile(self.app, self.colNumber, height=100),
                            270: Tile(self.app, self.colNumber, height=100)
            }

        self.activeTiles = set()
        self.updatedActiveTiles = set()

        self.isClicked = False

    def getRandomHeight(self):
        options = len(self.heightOptions)-1
        height = self.heightOptions[random.randint(0, options)]
        return height

    # def generateColumnTiles(self, tileNum=8):
    #     tiles = []
    #     tileFireTimes = [1,5,8,9,10,20,35,40]
    #     for i in range(tileNum):
    #         randomHeight = getRandomHeight(self.heightOptions)
    #         tile = Tile(self.app, self.colNumber, height=randomHeight, fire=tileFireTimes[i]) #deleted fire 
    #         tiles.append(tile)
    #     return tiles

    def addNewTile(self):
        randomHeight = self.getRandomHeight()
        newTile = Tile(self.app, self.colNumber, height=randomHeight)
        self.tiles.append(newTile)
    
    
    def drawColumn(self, app, canvas):
        for t in self.tiles:
            tile = self.tiles[t]
            tile.drawTile(app, canvas)

    def getXColPos(self):
        colPos = (self.app.tileBarXPos[self.colNumber], self.app.tileBarXPos[self.colNumber + 1])
        return colPos

    def getClickedTile(self):
    #returns None if click is triggered but nothing is actually clicked
        for tile in self.activeTiles:
            if tile.state != "clicked":
                tilePos = (tile.x1, tile.y1, tile.x2, tile.y2)
                # colXPos = (self.colx0,  self.colx1)
                # colPosX1, colPosX2 = self.app.barPos[]
                colPos = (self.colx0, self.app.barPos[1], self.colx1, self.app.barPos[3])
                if isOverLap(tilePos, colPos):
                    return tile
        return None

def getRandomHeight(L):
        options = len(L)-1
        height = L[random.randint(0, options)]
        return height




# self.tiles = [{  1: Tile(self.app, self.colNumber, height=20), 
#                         5: Tile(self.app, self.colNumber, height=20),
#                         10: Tile(self.app, self.colNumber, height=20),
#                         17: Tile(self.app, self.colNumber, height=20)
#         }, {  1: Tile(self.app, self.colNumber, height=20), 
#                         5: Tile(self.app, self.colNumber, height=20),
#                         10: Tile(self.app, self.colNumber, height=20),
#                         17: Tile(self.app, self.colNumber, height=20)
#         }, {  1: Tile(self.app, self.colNumber, height=20), 
#                         5: Tile(self.app, self.colNumber, height=20),
#                         10: Tile(self.app, self.colNumber, height=20),
#                         17: Tile(self.app, self.colNumber, height=20)
#         }, {  1: Tile(self.app, self.colNumber, height=20), 
#                         5: Tile(self.app, self.colNumber, height=20),
#                         10: Tile(self.app, self.colNumber, height=20),
#                         17: Tile(self.app, self.colNumber, height=20)
#         }]