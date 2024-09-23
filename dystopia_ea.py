import matplotlib.pyplot as plt
import numpy as np

class Fighter():

    def __init__(self, strength, charisma):
        self.strength = strength
        self.charisma = charisma

    def rebel_run(self):

        rebel_loc = 0
        rebel_sigma = 4
        normal_probability = np.random.normal(rebel_loc, rebel_sigma)
        if normal_probability < 0:
            self.charisma += abs(normal_probability)
        else:
            self.strength += abs(normal_probability)

    def soldier_run(self):
        soldier_loc = 5
        soldier_sigma = 4
        normal_probability = np.random.normal(soldier_loc, soldier_sigma)
        if normal_probability < 0:
            self.charisma += abs(normal_probability)
        else:
            self.strength += abs(normal_probability)