import time
from tile import *
from helper import *
import random

def getRandomizedTiles(tileNum=10, colAmt=4, highRange=401):
        result = []
        for col in range(colAmt):
            # refered https://pynative.com/python-random-randrange/
            columnResult = sorted(random.sample(range(1, highRange, 10), tileNum))
            result.append(columnResult)
        return result


class Column:
    def __init__(self, app, colNumber):
        self.app = app
        self.colNumber = colNumber #0, 1, 2, 4
        self.tileNumPerCol = app.tileNumPerCol ##arbitrary
        self.heightOptions = [app.height//8, app.height//5, app.height//2]
        #self.tiles = self.generateColumnTiles()

        self.colx0, self.colx1 = self.getXColPos()
        # cols
        self.tileListAllCols = getRandomizedTiles(tileNum=self.tileNumPerCol, colAmt=app.colTileNum, highRange=app.highRange)
        #self.tileListAllCols = self.getRandomizedTiles(self.tileNum)


        self.tiles = self.getTiles(app, self.tileListAllCols[colNumber], colNumber)

        self.activeTiles = set()
        self.updatedActiveTiles = set()

        self.isClicked = False
            

    def getTiles(self, app, tileList, colNumber, height=200):
        tiles = {}
        for num in tileList:
            tile = Tile(app, colNumber, height)
            tiles[num] = tile
        return tiles

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

    def isActiveTileReachedBottom(self):
        for tile in self.activeTiles:
            if tile.hasReachedBottom():
                print("reached bttom")
                tile.color = 'red'
                tile.isActive = False
                return True
        return False

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

#self.tiles = {  200: Tile(self.app, self.colNumber, height=200), 
            #                 300: Tile(self.app, self.colNumber, height=200),
            #                 450: Tile(self.app, self.colNumber, height=200),
            #                 550: Tile(self.app, self.colNumber, height=200),
            #                 650: Tile(self.app, self.colNumber, height=200)
            # }