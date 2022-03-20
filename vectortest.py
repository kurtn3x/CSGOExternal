from classes.Vector import Vector
from math import *
radian = 57.295779513082

LocalPlayer = Vector(-960.534931, 2287.459473, -56.383827)
Target = Vector(-420.307464, 2007.2907715, -61.84017844)
delta = Vector(LocalPlayer.x - Target.x, LocalPlayer.y - Target.y,  LocalPlayer.z - Target.z)
hyp = sqrt(delta.x * delta.x + delta.y * delta.y + delta.z * delta.z)
pitch = asin(delta.x / delta.z) * radian
print(pitch)