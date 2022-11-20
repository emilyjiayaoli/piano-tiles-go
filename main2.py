from cmu_112_graphics import *
from tile import *
import time

# make tiles show up
# make tiles move down the screen when keyPressed
# make recognition

def appStarted(app):
    app.rowTileNum = 4 #tileNum 4, 5, 6, 7

    app.timerDelay = 140
    app.play = []

    # background grid
    app.tileWidth = app.width//app.tileNum 
    app.tileBarXPos = [0, app.tileWidth, app.tileWidth*2, app.tileWidth*3, app.tileWidth*4]
    #app.tileBarXPose = generateTileBarXPos(app, app.tileNum) #
    app.tiles = generateTiles(app, app.tileNum) #[tile1, tile2]

def generateTileBarXPos(app, rowTileNum):
    tileBarXPos = []
    for i in range(rowTileNum):
        tileBarXPos.append(i * app.tileWidth)
    return tileBarXPos

# def generateTiles(app, rowTileNum):
#     # generates a list of tile objects according to tileNum
#     tiles = []
#     for l in range(rowTileNum):
#         tile = Tile(app, tileNum=l)
#         tiles.append(tile)
#     return tiles 

def generateTiles(app, rowTileNum, numTilesInEachCol=8):
    # generates a 2d list of tiles
    tiles = []
    for col in range(rowTileNum): #each column of piano tiles
        colTiles = []
        for t in range(numTilesInEachCol):
            tile = Tile(app, col=col) #
            colTiles.append(tile)
        tiles.append(colTiles)
    return tiles 

def keyPressed(app, event):
    if (event.key == "r"):
        appStarted(app)
    #elif (event.key = )

def timerFired(app):
    #tile = app.tiles[random.randint(0, len(app.tiles)-1)]
    #for tile in app.tiles:
    ind = 0
    # while len(app.tile) > 0:
    #     ind += 1
    #     tile = app.tiles[ind]
    #     # rand = random.randint(0, 10)
    #     # if rand == 10 and tile.hasReachedBottom():
    #     #     tile.changeActivityState()
    #     if tile.isActive and not tile.hasReachedBottom():
    #         tile.moveTile()

    for tile in app.tiles:
        if tile.isActive and not tile.hasReachedBottom():
            tile.moveTile()

def drawGrid(app, canvas):
    for xPos in app.tileBarXPos:
        canvas.create_line(xPos, 0, xPos, app.height, fill='black')

def getRandomHeight(self):
        options = len(self.heightOptions)-1
        height = self.heightOptions[random.randint(0, options)]
        return height
        
def redrawAll(app, canvas):
    drawGrid(app, canvas)

    for tile in app.tiles:
        if not tile.hasReachedBottom():
            tile.drawTile(app, canvas)
    canvas.create_text(200,  50,
                       text='Keyboard Shortcut Demo', fill='black')

runApp(width=1200, height=800) # quit still runs next one, exit does not