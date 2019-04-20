#!/home/matt/anaconda3/bin/python3.7
# encoding: utf-8
"""
Spawning lot of sine waves to multiple processes.
From the command line, run the script with -i flag.

Call quit() to stop the workers and quit the program.

"""
import time
import multiprocessing
from random import uniform
from pyo import Server, SineLoop

class Group(multiprocessing.Process):
    def __init__(self, num_of_sines):
        super(Group, self).__init__()
        self.daemon = True
        self._terminated = False
        self.num_of_sines = num_of_sines

    def run(self):
        # All code that should run on a separated
        # core must be created in the run() method.

        self.server = Server(sr=48000, nchnls=2, buffersize=2048, duplex=0, audio='jack', jackname='pyo')
        # self.server.deactivateMidi()
        self.server.setOutputDevice(0)
        self.server.boot()
        self.server.start()

        # self.server = Server()
        # self.server.deactivateMidi()
        # self.server.boot().start()

        freqs = [uniform(400,800) for i in range(self.num_of_sines)]
        self.oscs = SineLoop(freq=freqs, feedback=0.1, mul=.005).out()

        # Keeps the process alive...
        while not self._terminated:
            time.sleep(0.001)

        self.server.stop()

    def stop(self):
        self._terminated = True

if __name__ == '__main__':
    # Starts four processes playing 500 oscillators each.
    jobs = [Group(500) for i in range(4)]
    [job.start() for job in jobs]

    def quit():
        "Stops the workers and quit the program."
        [job.stop() for job in jobs]
        exit()