from cmu_112_graphics import *
from tile import *
from column import *
import time
import copy

# make tiles show up --> done
# make tiles move down the screen when keyPressed --> done
# make recognition
# write function that turns list of counts to tile generations
# fix generate colbarxpos

def appStarted(app):
    app.mode = "startScreen"
    app.gameStarted = False
    app.score = 0
    app.level = 1
    app.colTileNum = 4 #tileNum 4, 5, 6, 7
    app.timerDelay = 10 #140
    app.gamePause = False

    # background grid
    app.tileWidth = app.width//app.colTileNum 
    app.tileBarXPos = [0, app.tileWidth, app.tileWidth*2, app.tileWidth*3, app.tileWidth*4]

    #app.tiles = generateTiles(app, app.tileNum) #[tile1, tile2]
    app.board = generateBoard(app)

    app.time0 = time.time()
    app.counter = 0

    app.barHeight = 100
    #app.barPos = (0, 960, 800, 1060) # harcoding height bec app.height somehow gets changed 
    app.height = 1200
    app.barPos = (0, (4*(app.height//5)), app.width, (4*app.height//5)+app.barHeight)

def startScreen_redrawAll(app, canvas):
    canvas.create_text(app.width//2, app.height//2, text=f"Press b to begin game")

def startScreen_keyPressed(app, event):
    if (event.key == "b"):
        app.mode = "main"

def clickButton(app, col):
    column = app.board[col]
    column.isClicked = True

def generateColBarXPos(app, colTileNum):
    tileBarXPos = []
    for i in range(colTileNum):
        tileBarXPos.append(i * app.tileWidth)
    return tileBarXPos

def generateBoard(app):
    # generates a 2d list of tiles
    board = []
    for col in range(app.colTileNum):
        columnTiles = Column(app, col)
        board.append(columnTiles)
    return board

def main_keyPressed(app, event):
    if (event.key == "r"):
        appStarted(app)
    elif (event.key == "d"):
        clickButton(app, col=0)
    elif (event.key == "f"):
        clickButton(app, col=1)
    elif (event.key == "j"):
        clickButton(app, col=2)
    elif (event.key == "k"):
        clickButton(app, col=3)
    
    elif (event.key == "b"):
        app.mode = "startScreen"
    elif (event.key == "Space"):
        app.gameStarted = True


def resetTimer(app):
    app.counter = 0
    app.time0 = 0

def gameOver():
    pass

def main_timerFired(app):
    if app.gamePause:
        app.gameStarted = False
        gameOver()
    
    if app.gameStarted:
        app.counter += 1
        for column in app.board:
            activateTilesInCurColumn(column, app.counter)
        
            if column.isClicked:
                tileClicked = column.getClickedTile()
                print(tileClicked)
                if tileClicked != None:
                    app.score += 1
                    tileClicked.state = "clicked"
                    tileClicked.color = "pink"
                    tileClicked.isActive = False
                else: #clicked, but no tile is found, stop game
                    app.gamePause = True

                column.isClicked = False

            moveAllActiveTilesInColumn(column)


def activateTilesInCurColumn(column, counter):
    # Helper for timerFired()
    #  Changes the tiles state to active in specified column based on time
    if counter in column.tiles:
            tile = column.tiles[counter]
            tile.isActive = True
            column.activeTiles.add(tile)

def moveAllActiveTilesInColumn(column):
    # Helper for timerFired()
    # moves all active tiles and update set column.activeTiles
    for tile in column.activeTiles:
            if not tile.hasReachedBottom():
                column.updatedActiveTiles.add(tile)
                tile.moveTile()
    column.activeTiles = column.updatedActiveTiles#.copy()
    column.updatedActiveTiles = set()


def drawGrid(app, canvas):
    for xPos in app.tileBarXPos:
        canvas.create_line(xPos, 0, xPos, app.height, fill='black')

def drawColumns(app, canvas):
    for column in app.board:
        column.drawColumn(app, canvas)

def main_redrawAll(app, canvas):
    (x0, y0, x1, y1) = app.barPos
    canvas.create_rectangle(x0, y0, x1, y1, fill="yellow")
    drawGrid(app, canvas)
    drawColumns(app, canvas)
    canvas.create_text(app.width//2, app.height//2, text=f"Score: {app.score}")

    if app.gamePause:
        canvas.create_text(app.width//2, (app.height//2) + 30, text=f"Bad!!!: {app.score}")
    
runApp(width=800, height=1200) # quit still runs next one, exit does not