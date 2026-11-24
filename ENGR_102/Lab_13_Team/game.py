# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Kennyson Le
# Adila Hansbhai
# Kingston Jackson
# Tevya Birnbaum
# Section: 567
# Assignment: Lab 9 Team
# Date: 11 12 2026
#

import renderer
import pygame

screen = pygame.display.set_mode((1600, 900), pygame.OPENGL)
vertices, triangles = renderer.load_model("./models/cube.obj")
renderer.render(screen, vertices, triangles, (240, 140, 40))
pygame.display.flip()
# renderer.render()