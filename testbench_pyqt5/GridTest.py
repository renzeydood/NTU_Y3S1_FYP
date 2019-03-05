import time

'''
Grid legends:
0 = empty
1 = block
2 = robot
5 = start
6 = end
3 = waypoint
4 = arrow
? = Undiscovered
'''

grid = []
robot = []
lastLoc = [0, 0]        #[X, Y]

def Main():
    boardInit(grid, 15, 20)
    robotInit(robot, 3, 3)
    lastLoc[0] = 2
    lastLoc[1] = 14

    placeRobot(grid, robot, lastLoc[0], lastLoc[1])

    insertBlock(grid, 9, 17)
    insertBlock(grid, 0, 17)
    insertBlock(grid, 3, 10)
    insertBlock(grid, 2, 19)
    print(grid)

    while(1):
        print("Move the robot(Use the keys 'A', 'S', 'W', 'D')")
        key = input()
        controlRobot(grid, robot, key)
        print(grid)


def boardInit(gridContainer, numGridX, numGridY):
    for y in range(numGridY):
        innerArray = []
        for x in range(numGridX):
            innerArray.append(0)
        gridContainer.append(innerArray)

def robotInit(robotContainer, sizeX, sizeY):
    for y in range(sizeY):
        innerArray = []
        for x in range(sizeX):
            innerArray.append(2)
        robotContainer.append(innerArray)

def placeRobot(gridArray, robotArray, locX, locY):
    for y in range(len(robot)):
        #grid[locY+y] = grid[locY+y] + robot[y]
        for x in range(len(robot[0])):
            gridArray[locY+y][locX+x] =  gridArray[locY+y][locX+x] + robotArray[y][x]

def removeRobot(gridArray, robotArray, locX, locY):
    for y in range(len(robot)):
        #grid[locY+y] = grid[locY+y] + robot[y]
        for x in range(len(robot[0])):
            gridArray[locY+y][locX+x] =  gridArray[locY+y][locX+x] - robotArray[y][x]

def moveRobotEast(gridArray, robotArray, noBlocks):
    print("Moving east")
    if lastLoc[0] > 11:
        print("Can't move anymore, out of bounds")
    else:
        blocks = 0
        for y in range(len(robotArray)):
            if(gridArray[lastLoc[1]+y][lastLoc[0]+3] == 1):
                print("Can't move anymore, there's a block in front")
                blocks = blocks + 1
        if blocks == 0:
            removeRobot(gridArray, robotArray, lastLoc[0], lastLoc[1])
            placeRobot(gridArray, robotArray, lastLoc[0] + noBlocks, lastLoc[1])
            lastLoc[0] = lastLoc[0] + noBlocks

def moveRobotWest(gridArray, robotArray, noBlocks):
    print("Moving west")
    if lastLoc[0] < 1:
        print("Can't move anymore, out of bounds")
    else:
        blocks = 0
        for y in range(len(robotArray)):
            if(gridArray[lastLoc[1]+y][lastLoc[0]-1] == 1):
                print("Can't move anymore, there's a block in front")
                blocks = blocks + 1
        if blocks == 0:
            removeRobot(gridArray, robotArray, lastLoc[0], lastLoc[1])
            placeRobot(gridArray, robotArray, lastLoc[0] - noBlocks, lastLoc[1])
            lastLoc[0] = lastLoc[0] - noBlocks

def moveRobotNorth(gridArray, robotArray, noBlocks):
    print("Moving north")
    if lastLoc[1] < 1:
        print("Can't move anymore, out of bounds")
    else:
        blocks = 0
        for x in range(len(robotArray[0])):
            if(gridArray[lastLoc[1]-1][lastLoc[0]+x] == 1):
                print("Can't move anymore, there's a block in front")
                blocks = blocks + 1
        if blocks == 0:
            removeRobot(gridArray, robotArray, lastLoc[0], lastLoc[1])
            placeRobot(gridArray, robotArray, lastLoc[0], lastLoc[1] - noBlocks)
            lastLoc[1] = lastLoc[1] - noBlocks

def moveRobotSouth(gridArray, robotArray, noBlocks):
    print("moving south")
    if lastLoc[1] > 16:
        print("Can't move anymore, out of bounds")
    else:
        blocks = 0
        for x in range(len(robotArray[0])):
            if(gridArray[lastLoc[1]+3][lastLoc[0]+x] == 1):
                print("Can't move anymore, there's a block in front")
                blocks = blocks + 1
        if blocks == 0:
            removeRobot(gridArray, robotArray, lastLoc[0], lastLoc[1])
            placeRobot(gridArray, robotArray, lastLoc[0], lastLoc[1] + noBlocks)
            lastLoc[1] = lastLoc[1] + noBlocks

def insertBlock(gridArray, locX, locY):
    if gridArray[locY][locX] == 0:
        gridArray[locY][locX] = 1
    else:
        print("Can't insert block")

def checkWinCondition():
    #If robot reaches the end point AND map fully discovered
    pass

def controlRobot(gridArray, robotArray, key):
    #key = input()
    if key == 'A':
        moveRobotWest(gridArray, robotArray, 1)
    elif key == 'S':
        moveRobotSouth(gridArray, robotArray, 1)
    elif key == 'W':
        moveRobotNorth(gridArray, robotArray, 1)
    elif key == 'D':
        moveRobotEast(gridArray, robotArray, 1)
    else:
        print("Please try again")


if __name__ == '__main__':
    Main()