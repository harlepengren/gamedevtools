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

        # Place a starting intersection in the upper third of the map
        currX = self.width // 3 
        currY = self.height // 3
        self.cityMap[currY][currX] = '#'

        # Generate roads in all directions
        self.newRoad((currX,currY),'u')
        self.newRoad((currX,currY),'d')
        self.newRoad((currX,currY),'l')
        self.newRoad((currX,currY),'r')

        # Currently the final checkCheck is commented out, because it is resulting in unpredicatble results.
        #self.finalCheck()


    def newIntersection(self,currentPosition,direction):
        """This function decides whether to create a new intersection, straight road, or stop."""

        prob = random.randint(0,10)

        currX = currentPosition[0]
        currY = currentPosition[1]

        # 30% probability of a new intersection, 40% probabiloity of a straight road, 30% probability that the road just ends
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
        """Creates a new road in direction. Direction can be 'u','d','l','r'."""
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

        # Originally, this was intended as a random road length. However, this created
        # unpredictable results. Therefore, we changed to a constant.
        randRoad = 5
        for index in range(1,randRoad):
            currX = index*vector[0] + currentPosition[0]
            currY = index*vector[1] + currentPosition[1]

            # If we are outside the width of the map, simply return
            if currX >= self.width or currX <0 or currY >= self.height or currY <0:
                return

            if self.cityMap[currY][currX] == None:
                self.cityMap[currY][currX] = directionChar
        
        # Move to the next spot
        currX = currentPosition[0]+vector[0]*(randRoad)
        currY = currentPosition[1]+vector[1]*(randRoad)
        if currX >= self.width or currX <0 or currY >= self.height or currY <0:
                return

        # Call newIntersection to determine whether we should create a new intersection or not.
        if self.cityMap[currY][currX] == None:
            self.newIntersection((currX,currY),direction)
        
    def finalCheck(self):
        """This method walks through the map to determine whether we should create any intersections. For example if
        we have to different directions of road right next to each other."""
        for y in range(1,self.height-1):
            for x in range(1,self.width-1):
                # if there is a road to the left or right and a road to the up or down, add an intersection
                if self.cityMap[y][x] not in ['#',None]:
                    if (self.cityMap[y-1][x] in ['-','|']) or (self.cityMap[y+1][x] in ['-','|']) and \
                        (self.cityMap[y][x-1] in ['-','|']) or (self.cityMap[y][x+1] in ['-','|']):
                        self.cityMap[y][x] = "#"

    def getMap(self):
        return self.cityMap     
        