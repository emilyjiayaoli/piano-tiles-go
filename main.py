from cmu_112_graphics import *
from tile import *
from column import *
import time
import copy

def appStarted(app):
    # Use of mode referenced from cmu 112 graphics
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
    app.mode = "startScreen" #default screen

    app.gameStarted = False
    app.gameFinished = False
    app.gamePause = False

    app.score = 0
    app.level = 1
    app.colTileNum = 4 #tileNum 4, 5, 6, 7
    app.timerDelay = 10 #140

    app.centerX = app.width//2
    app.centerY = app.height//2

    app.tileNumPerCol = 10

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
    app.barPos = (0, (4*(app.height//5))-20, app.width, (4*app.height//5)+app.barHeight)


def startScreen_redrawAll(app, canvas):
    canvas.create_text(app.width//2, app.height//2, text=f"Press b to begin game")

def startScreen_keyPressed(app, event):
    if (event.key == "b"):
        app.mode = "main"

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
        columnClicked(app, col=0)
    elif (event.key == "f"):
        columnClicked(app, col=1)
    elif (event.key == "j"):
        columnClicked(app, col=2)
    elif (event.key == "k"):
        columnClicked(app, col=3)
    
    elif (event.key == "b"):
        app.mode = "startScreen"
    elif (event.key == "Space"):
        app.gameStarted = True

def columnClicked(app, col):
    column = app.board[col]
    column.isClicked = True

def resetTimer(app):
    app.counter = 0
    app.time0 = 0

def gameOver():
    pass

def main_timerFired(app):
    if app.gamePause:
        app.gameStarted = False
    
    if app.gameStarted:
        app.counter += 0.5
        for column in app.board:
            activateTilesInCurColumn(column, app.counter)
            moveAllActiveTilesInColumn(column)
            if column.isClicked:
                tileClicked = column.getClickedTile()
                #print(tileClicked)

                if tileClicked != None: # case 1: keypressed on tile correctly
                    app.score += 1
                    tileClicked.state = "clicked"
                    tileClicked.color = "pink"
                    tileClicked.isActive = False
                else: # case 2: pause game when keypressed incorrectly. no tile is found
                    app.gamePause = True
                column.isClicked = False
            else: # case 2: pause game when failed to click on time
                if column.isActiveTileReachedBottom(): 
                    app.gamePause = True
        if app.score == app.tileNumPerCol * app.colTileNum:
            app.gameFinished = True
    

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

def drawGamePausedPopUp(app, canvas):
    popUpWidth, popUpHeight = app.width//2, app.height//2
    canvas.create_rectangle(app.centerX-0.5*popUpWidth, app.centerY-0.5*popUpHeight,
                            app.centerX+0.5*popUpWidth, app.centerY+0.5*popUpHeight,
                            fill='pink')
    canvas.create_text(app.centerX, app.centerY + 30, text=f"You Lost!")
    canvas.create_text(app.centerX, app.centerY + 50, text=f"Score: {app.score}")

def drawGameFinishedPopUp(app, canvas):
    popUpWidth, popUpHeight = app.width//2, app.height//2
    canvas.create_rectangle(app.centerX-0.5*popUpWidth, app.centerY-0.5*popUpHeight,
                            app.centerX+0.5*popUpWidth, app.centerY+0.5*popUpHeight,
                            fill='pink')
    canvas.create_text(app.centerX, app.centerY + 30, text=f"You Won!")
    canvas.create_text(app.centerX, app.centerY + 50, text=f"Score: {app.score}")
    canvas.create_text(app.centerX, app.centerY + 70, text=f"press r to restart")

def main_redrawAll(app, canvas):
    (x0, y0, x1, y1) = app.barPos
    canvas.create_rectangle(x0, y0, x1, y1, fill="yellow")
    drawGrid(app, canvas)
    drawColumns(app, canvas)
    canvas.create_text(app.width//2, app.height//15, text=f"Score: {app.score}")

    if app.gamePause:
        drawGamePausedPopUp(app, canvas)
    elif app.gameFinished:
        drawGameFinishedPopUp(app, canvas)
        
    
runApp(width=800, height=1200) # quit still runs next one, exit does not