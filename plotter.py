import threading
import matplotlib.pyplot as plt
from time import sleep, time

class Plotter():
    def __init__(self):
        self.fig, self.axs = plt.subplots(4, 1)
        self.y = [[], [], [], []]
        self.x = [[], [], [], []]

    def add(self, x, y, n=0):
        self.x[n] = x
        self.y[n] = y

    def update_plot(self):
        for n in range(4):
            self.axs[n].plot(self.x[n], self.y[n])
            self.axs[n].set_xlim(4, 100)
            #self.axs[n].set_yscale('log')
        plt.pause(0.01)
        [self.axs[n].cla() for n in range(4)]

        

