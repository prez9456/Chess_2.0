#User Input and displaying current game state object
import pygame as p
from chess import *
from ChessEngnie import *

#if error uncomment line below
#p.init()
background = (255,255,255)
blue = (46, 86, 233)
yellow = (255,255,0)
width = height = 512
dimension = 8
sqSize = height // dimension
maxFPS = 60
images = {}

#Global dictionary of images
def loadImages():
    pieces = ['wP','wR','wN','wB','wQ','wK','bP','bR','bN','bB','bQ','bK']
    #Access an image
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sqSize, sqSize))

def main():
    #start of screen
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    p.display.set_caption('Some type of chess game, idk sue me')

    #fill background
    screen.fill(background)
    gs = GameState()
    validMoves = gs.getAllMoves()
    moveMade = False
    animate = False
    loadImages()
    
    running = True
    #keeps track of last click
    sqSelected = () 
    #keeps track of play clicks
    playerClicks = []
    gameOver = False
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                #location of mouse (x,y)
                    location = p.mouse.get_pos()
                    col = location[0] // sqSize
                    row = location[1] // sqSize
                    #if same square is clicked again, it is a un select
                    if sqSelected == (row, col):
                            sqSelected == ()
                            playerClick = []
                    else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                    #after 2nd click
                    if len(playerClicks) == 2:
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True                                #reset user clicks
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif event.type == p.KEYDOWN:
                if event.key == p.K_r:
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.getAllMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteTurn:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen,'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen,'Stalemate')
        clock.tick(maxFPS)
        p.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteTurn else 'b'):
            s = p.Surface((sqSize, sqSize))
            s.set_alpha(100)
            s.fill(blue)
            screen.blit(s, (c*sqSize, r*sqSize))
            s.fill(yellow)
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*sqSize, move.endRow*sqSize))

#visuals for the game
def drawGameState(screen, gs, validMoves, sqSelected):
    #draws squares
    drawBoard(screen)
    highlightSquares(screen,gs,validMoves,sqSelected)
    #draw pieces
    drawPieces(screen, gs.board)

#draws the board
def drawBoard(screen):
    colors = [p.Color(229, 174, 134), p.Color(172, 112, 61)]
    for r in range(dimension):
        for c in range(dimension):
           color = colors[((r+c) % 2)]
           p.draw.rect(screen, color, p.Rect(c*sqSize, r*sqSize, sqSize, sqSize))
    return;

#draws pieces after board is loade
def drawPieces(screen, board):
   for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece],p.Rect(c*sqSize, r*sqSize, sqSize, sqSize))

#animate moves
def animateMove(move, screen, board, clock):
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 60
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r,c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)

        endSquare = p.Rect(move.endCol*sqSize, move.endRow*sqSize,sqSize,sqSize)

        if move.pieceCaptured != '--':
            screen.blit(images[move.pieceCaptured],endSquare)

        p.display.flip()
        clock.tick(60)

def drawText(scree, text):
    font = p.font.SysFont("Helvitca",32,True,False)
    textObject = font.render(text,0,p.color('Gray'))
    textLocation = p.Rect(0,0,width,height).move(width/2 - textObject.get_width()/2, height/2 - textObject.get_height()/2)
    scree.blit(textObject, textLocation)
    textObject = font.render(text,0,p.color('Black'))
    screen.blit(textObject,textLocation.move(2,2))


if __name__ == "__main__":
    main()