from PIL import Image
import gencity
import xml.etree.ElementTree as ET
import random

class TileData:
    """Holds data about a tile in a spritesheet."""
    def __init__(self,name=None,location=None,size=None):
        self.name = name
        self.location = location
        self.size = size
        self.levelRef = None

    def setLocation(self,x,y):
        self.location=(x,y)
    
    def setSize(self,width,height):
        self.size = (width,height)

    def loadImage(self,spriteSheet:Image):
        if(self.location == None or self.size == None):
            return
        
        x = self.location[0]
        y = self.location[1]
        self.image = spriteSheet.crop(box=(x,y,x+self.size[0],y+self.size[1]))



class CityImage:
    def loadIntersection(self,intersectionPath):
        self.intersection = TileData('intersection',size=(128,64))
        self.intersection.image = Image.open(intersectionPath)
    
    def loadUp(self,upPath):
        self.up = TileData('up',size=(128,64))
        self.up.image = Image.open(upPath)

    def loadLeft(self,leftPath):
        self.left = TileData('left',size=(128,64))
        self.left.image = Image.open(leftPath)

    def loadBuildings(self,buildings,levels,rooves,imgPath,xmlPath):
        """buildings is the list of building numbers to load."""
        self.buildingList = []
        self.levelDict = {}
        self.roofList = []
        spriteSheet = Image.open(imgPath)

        tree = ET.parse(xmlPath)
        root = tree.getroot()
        for child in root: 
            currentNumber = int(child.attrib['name'][14:][:3])
            if currentNumber in buildings:
                index = buildings.index(currentNumber)
                tile = TileData(name = currentNumber)
                tile.setLocation(int(child.attrib['x']),int(child.attrib['y']))
                tile.setSize(int(child.attrib['width']),int(child.attrib['height']))
                tile.loadImage(spriteSheet)
                tile.levelRef = levels[index]

                self.buildingList.append(tile)

            if currentNumber in levels:
                tile = TileData(name = currentNumber)
                tile.setLocation(int(child.attrib['x']),int(child.attrib['y']))
                tile.setSize(int(child.attrib['width']),int(child.attrib['height']))
                tile.loadImage(spriteSheet)

                self.levelDict[str(currentNumber)] = tile
            
            if currentNumber in rooves:
                tile = TileData(name = currentNumber)
                tile.setLocation(int(child.attrib['x']),int(child.attrib['y']))
                tile.setSize(int(child.attrib['width']),int(child.attrib['height']))
                tile.loadImage(spriteSheet)

                self.roofList.append(tile)

    def createCityImage(self,imageSize,mapSize):
        """Creates a new city image of size imageSize (in pixels) and with underlying mapSize (in tiles).
        imageSize and mapSize are tuples."""
        
        # create a new image    
        city = Image.new("RGBA",imageSize)

        cityMapGen = gencity.City()
        cityMapGen.generateCity(mapSize[0],mapSize[1],numBuildings=len(self.buildingList))
        
        startPosition = (0, 0)

        # Translate the cityMap into an image
        currentMap = cityMapGen.getMap()
        for y in range(0,mapSize[1]):
            for x in range(0,mapSize[0]):
                adjustment = 0
                hasLevels = False
                hasRoof = False

                if currentMap[y][x] == '#':
                    currentTile = self.intersection
                elif currentMap[y][x] == '|':
                    currentTile = self.up
                elif currentMap[y][x] == '-':
                    currentTile = self.left
                elif type(currentMap[y][x]) == int:
                    # Place building
                    if currentMap[y][x] < len(self.buildingList):
                        currentTile = self.buildingList[currentMap[y][x]]
                        adjustment = currentTile.size[1]-101

                        numLevels = random.randint(0,5) * random.randint(0,1)
                        if numLevels > 0:
                            hasLevels = True
                            levelTile = self.levelDict[str(currentTile.levelRef)]

                        roofType = random.randint(0,len(self.roofList))
                        if roofType > 1:
                            hasRoof = True
                            roofTile = self.roofList[roofType-1]

                tile_width_half = 64
                tile_height_half = 32

                position = ((x*tile_width_half)-(y*tile_width_half)+startPosition[0],(y*tile_height_half)+(x*tile_height_half)+startPosition[1]-adjustment)
                city.alpha_composite(currentTile.image,position)

                if hasLevels:
                    currentLevelPosition = position
                    xAdjustment = (currentTile.size[0] - levelTile.size[0]) //2
                    yAdjustment = 32
                    for index in range(0,numLevels):
                        levelPosition = (currentLevelPosition[0]+xAdjustment,currentLevelPosition[1]-yAdjustment*(index+1))
                        city.alpha_composite(levelTile.image,levelPosition)

                    if hasRoof:
                        roofPosition = (currentLevelPosition[0]+xAdjustment,currentLevelPosition[1]-yAdjustment*(numLevels+1))
                        city.alpha_composite(roofTile.image,currentLevelPosition)

        city.save('city.png')



    

