import threading
import matplotlib.pyplot as plt
from time import sleep, time

class Plotter():
    def __init__(self):
        self.fig, self.axs = plt.subplots(4, 1)
        self.y = [[], [], [], []]
        self.x = [[], [], [], []]
        self.propeties = [{}, {}, {}, {}]
        [self.set_properties(n) for n in range(4)]

    def add(self, x, y, n=0):
        self.x[n] = x
        self.y[n] = y

    def set_properties(self, channel=0, **kwargs):
        self.propeties[channel]['title'] = kwargs.get('title', "")
        self.propeties[channel]['x_label'] = kwargs.get('x_label', "")
        self.propeties[channel]['y_label'] = kwargs.get('y_label', "")
        self.propeties[channel]['x_lim'] = kwargs.get('x_lim', (0, 100))
        self.propeties[channel]['y_lim'] = kwargs.get('y_lim', (None, None))

    def update_plot(self):
        for n in range(4):
            prop = self.propeties[n]
            self.axs[n].semilogy(self.x[n], self.y[n])
            self.axs[n].set_title(prop['title'])
            self.axs[n].set_xlabel(prop['x_label'])
            self.axs[n].set_ylabel(prop['y_label'])
            self.axs[n].set_xlim(prop['x_lim'])
            self.axs[n].set_ylim(prop['y_lim'])
        plt.pause(0.01)
        [self.axs[n].cla() for n in range(4)]

        

