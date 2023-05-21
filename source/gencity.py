"""Module generates a city map."""

from numpy import ndarray
import random

class City:
    # b: blank tile
    # #: intersaction
    # o: roundabout
    # -: horizontal road
    # |: vertical road
    TILE_TYPES = ["b","#","o","-","|"]

    def generateCity(self,width,height):
        """Create a map of size width x height."""
        self.width = width
        self.height = height

        self.cityMap = ndarray((width,height),dtype='O')

        # Place a starting intersection
        currX = self.width // 2 #random.randint(0,width-1)
        currY = self.height //2 #random.randint(0,height-1)
        self.cityMap[currY][currX] = '#'

        # Generate roads in all directions
        self.newRoad((currX,currY),'u')
        self.newRoad((currX,currY),'d')
        self.newRoad((currX,currY),'l')
        self.newRoad((currX,currY),'r')

        #self.finalCheck()


    def newIntersection(self,currentPosition,direction):
        prob = random.randint(0,10)
        print("Trying intersection ({},{})".format(currentPosition[0],currentPosition[1]))

        currX = currentPosition[0]
        #if currX > self.width or currX < 0:
        #    return

        currY = currentPosition[1]
        #if currY > self.height or currY < 0:
        #    return

        if prob < 3:
            # New intersection
            self.cityMap[currY][currX] = '#'

            # start a road in every direction except where we came from
            if (direction != 'u'):
                self.newRoad((currX,currY),'u')
            if (direction != 'd'):
                self.newRoad((currX,currY),'d')
            if (direction != 'l'):
                self.newRoad((currX,currY),'l')
            if (direction != 'r'):
                self.newRoad((currX,currY),'r')
        elif prob > 6:
            # Keep going
            if direction == 'u' or direction == 'd':
                self.cityMap[currentPosition[1]][currentPosition[0]] = '|'
            else:
                self.cityMap[currentPosition[1]][currentPosition[0]] = '-'

            self.newRoad((currX,currY),direction)
        else:
            # else - blank - stop
            self.cityMap[currentPosition[1]][currentPosition[0]] = 'b'


    def newRoad(self,currentPosition, direction):
        """Direction can be 'u','d','l','r'."""
        if direction == 'u':
            vector = (0,-1)
            directionChar = '|'
        elif direction == 'd':
            vector = (0,1)
            directionChar = '|'
        elif direction == 'l':
            vector = (-1,0)
            directionChar = '-'
        else:
            vector = (1,0)
            directionChar = '-'

        randRoad = 5 #random.randint(5,10)
        for index in range(1,randRoad):
            currX = index*vector[0] + currentPosition[0]
            currY = index*vector[1] + currentPosition[1]

            if currX >= self.width or currX <0 or currY >= self.height or currY <0:
                return

            if self.cityMap[currY][currX] == None:
                self.cityMap[currY][currX] = directionChar
        
        currX = currentPosition[0]+vector[0]*(randRoad)
        currY = currentPosition[1]+vector[1]*(randRoad)
        if currX >= self.width or currX <0 or currY >= self.height or currY <0:
                return

        if self.cityMap[currY][currX] == None:
            self.newIntersection((currX,currY),direction)
        
    def finalCheck(self):
        # run through map and see if we need to add any intersections
        for y in range(1,self.height-1):
            for x in range(1,self.width-1):
                # if there is a road to the left or right and a road to the up or down, add an intersection
                if self.cityMap[y][x] not in ['#',None]:
                    if (self.cityMap[y-1][x] in ['-','|']) or (self.cityMap[y+1][x] in ['-','|']) and \
                        (self.cityMap[y][x-1] in ['-','|']) or (self.cityMap[y][x+1] in ['-','|']):
                        self.cityMap[y][x] = "#"     
        