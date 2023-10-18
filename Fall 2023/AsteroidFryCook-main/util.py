import math

# Utility Functions

def deg2Rad(degrees):
  rad = (math.pi / 180.0) * degrees
  return rad


def getDist(x0, y0, x1, y1):
  dist = (x1 - x0)**2 + (y1 - y0)**2
  dist = math.sqrt(dist)
  return dist


def rotatePoint(xc, yc, x, y, deg):
  currentAng = math.atan2(y - yc, x - xc)
  angRad = deg2Rad(deg)
  totalAng = currentAng + angRad
  dist = getDist(xc, yc, x, y)
  xNew = xc + math.cos(totalAng) * dist
  yNew = yc + math.sin(totalAng) * dist

  return xNew, yNew