from PIL import Image
import gencity

class CityImage:
    def loadIntersection(self,intersectionPath):
        self.intersection = Image.open(intersectionPath)
        self.intersection = self.intersection.convert("RGBA")
    
    def loadUp(self,upPath):
        self.up = Image.open(upPath)
        self.up = self.up.convert("RGBA")

    def loadLeft(self,leftPath):
        self.left = Image.open(leftPath)
        self.left = self.left.convert("RGBA")

    def createCityImage(self,imageSize,mapSize):
        """Creates a new city image of size imageSize (in pixels) and with underlying mapSize (in tiles).
        imageSize and mapSize are tuples."""
        
        # create a new image    
        city = Image.new("RGBA",imageSize)

        cityMapGen = gencity.City()
        cityMapGen.generateCity(mapSize[0],mapSize[1])
        
        # Start in top 1/3 of the map
        startPosition = (0, 0)

        # Currently, these are hardcoded
        tile_width_half = 64
        tile_height_half = 32

        # Translate the cityMap into an image
        currentMap = cityMapGen.getMap()
        for y in range(0,mapSize[1]):
            for x in range(0,mapSize[0]):
                position = ((x*tile_width_half)-(y*tile_width_half)+startPosition[0],(y*tile_height_half)+(x*tile_height_half)+startPosition[1])

                if currentMap[y][x] == '#':
                    city.alpha_composite(self.intersection,position)
                elif currentMap[y][x] == '|':
                    city.alpha_composite(self.up,position)
                elif currentMap[y][x] == '-':
                    city.alpha_composite(self.left,position)

        city.save('city.png')