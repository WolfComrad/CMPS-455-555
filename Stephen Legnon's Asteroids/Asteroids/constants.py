# Define some colors
BLACK = (0, 0, 0)
GREY2 = (125, 125, 125)
GREY1 = (175, 175, 175)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLUE = (0, 0, 255)

colorPalette = [WHITE, GREEN, RED, ORANGE, YELLOW, CYAN, MAGENTA]
nColors = len(colorPalette)

screenWidth = 1920
screenHeight = 900

gameMidX = screenWidth/2
gameMidY = screenHeight/2

# General constants and variables defined.
# Space rock variables.
maxRockVelocity = 2
maxRockScaleFactor = 40
maxRockTypes = 3

# These rocks all have 0, 0 close to their center.
rock0 = [[[1, 1], [1, -1], [-1, -1], [-1, 1], [1, 1]]]
rock1 = [[[1, 2], [3, 1], [3, -1], [1, -2], [-1, -2],
         [-3, -1], [-3, 1], [-1, 2], [1, 2]]]
rock2 = [[[1, 1], [1, 0], [1, -1], [-2, -1], [-2, 1], [1, 1]]]

spaceRocks = rock0 + rock1 + rock2
nRockTypes = len(spaceRocks)
nAsteroids = 30

maxExplodeCount = 30
maxShootingDelay = 10


basicShip = [[3, 0], [0, 4], [5, 4], [14, 0], [5, -4], [0, -4], [3, 0]]

bulletTimeSlowFactor = 0.25