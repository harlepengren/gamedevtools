from PIL import Image
import gencity
import os

# Load the spritesheet
intersection = Image.open(os.getcwd() + "/kenney_isometric-city/PNG/cityTiles_089.png")
intersection = intersection.convert("RGBA")
up = Image.open(os.getcwd() + "/kenney_isometric-city/PNG/cityTiles_081.png")
up = up.convert("RGBA")
left = Image.open(os.getcwd() + "/kenney_isometric-city/PNG/cityTiles_073.png")
left = left.convert("RGBA")

# create a new image
city = Image.new("RGBA",(2048,2048))

mapSize = 20
cityMap = gen2.City()
cityMap.generateCity(mapSize,mapSize)
startPosition = (1024,1024)
tile_width = 132
tile_width_half = 64
tile_height = 101
tile_height_half = 32

for y in range(0,mapSize):
    for x in range(0,mapSize):
        position = ((x*tile_width_half)-(y*tile_width_half)+startPosition[0],(y*tile_height_half)+(x*tile_height_half)+startPosition[1])

        if cityMap.cityMap[y][x] == '#':
            city.alpha_composite(intersection,position)
        elif cityMap.cityMap[y][x] == '|':
            city.alpha_composite(up,position)
            pass
        elif cityMap.cityMap[y][x] == '-':
            city.alpha_composite(left,position)

city.save('city.png')