from cmu_112_graphics import *
from tile import *
from column import *
import time
import copy

def appStarted(app):
    # Use of mode referenced from cmu 112 graphics
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
    app.mode = "startScreen" #default screen

    if app.mode == "startSreen":
        app.fourTileButton = False
        app.sixTileButton = False
        app.eightTileButton = False

    app.gameStarted = False
    app.gameFinished = False
    app.gamePause = False

    app.tileNumPerCol = 10
    app.highRange = 401 # in increments of 5s, determines how long the games runs for

    app.score = 0
    app.level = 1
    app.colTileNum = 4 #tileNum 4, 5, 6, 7
    if app.colTileNum == 4:
        app.fourCols = True
        app.tileNumPerCol = 10
    else: 
        app.fourCols = False
    if app.colTileNum == 6:
        app.sixCols = True
        app.tileNumPerCol = 6
    else: 
        app.sixCols = False
    if app.colTileNum == 8:
        app.eightCols = True
        app.tileNumPerCol = 4
    else:
        app.eightCols = False
    
    app.timerDelay = 10 #140

    app.centerX = app.width//2
    app.centerY = app.height//2

    # background grid
    app.tileWidth = app.width//app.colTileNum 
    app.tileBarXPos = [0, app.tileWidth, app.tileWidth*2, app.tileWidth*3, app.tileWidth*4]
    app.tileBarXPos = generateColBarXPos(app)

    #app.tiles = generateTiles(app, app.tileNum) #[tile1, tile2]
    app.board = generateBoard(app)

    app.time0 = time.time()
    app.counter = 0

    app.barHeight = 100
    #app.barPos = (0, 960, 800, 1060) # harcoding height bec app.height somehow gets changed 
    app.height = 1200
    app.barPos = (0, (4*(app.height//5))-20, app.width, (4*app.height//5)+app.barHeight)


def startScreen_redrawAll(app, canvas):
    canvas.create_text(app.centerX, app.centerY, text=f"Press b to begin game")

def startScreen_keyPressed(app, event):
    if (event.key == "b"):
        app.mode = "main"

def generateColBarXPos(app):
    tileBarXPos = []
    for i in range(app.colTileNum+1):
        tileBarXPos.append(i * app.tileWidth)
    #print(tileBarXPos)
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

    # Keyboard keypresses
    elif (event.key == "d"):
        if app.fourCols:
            columnClicked(app, col=0)
        elif app.sixCols:
            columnClicked(app, col=1)
        elif app.eightCols:
            columnClicked(app, col=2)
    elif (event.key == "f"):
        if app.fourCols:
            columnClicked(app, col=1)
        elif app.sixCols:
            columnClicked(app, col=2)
        elif app.eightCols:
            columnClicked(app, col=3)
    elif (event.key == "j"):
        if app.fourCols:
            columnClicked(app, col=2)
        elif app.sixCols:
            columnClicked(app, col=3)
        elif app.eightCols:
            columnClicked(app, col=4)
    elif (event.key == "k"):
        if app.fourCols:
            columnClicked(app, col=3)
        elif app.sixCols:
            columnClicked(app, col=4)
        elif app.eightCols:
            columnClicked(app, col=5)
    elif (event.key == "l"):
        if app.sixCols:
            columnClicked(app, col=5)
        elif app.eightCols:
            columnClicked(app, col=6)
    elif (event.key == "s"):
        if app.sixCols:
            columnClicked(app, col=0)
        elif app.eightCols:
            columnClicked(app, col=1)
    elif (event.key == "a") and (app.eightCols):
        columnClicked(app, col=0)
    elif (event.key == ";") and (app.eightCols):
        columnClicked(app, col=7)
    
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