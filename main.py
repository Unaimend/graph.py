#!/usr/bin/env python3
import tkinter as tk
import sys
import window as win
from model import MainModel
from controller import MainController

sys.path.append("~/Documents/dev/Projects/graph.py")

if __name__ == "__main__":
    # Addded to test TravisC
    # exit(0)

    sys.setrecursionlimit(10000)
    MODEL = MainModel()
    WINDOW = win.Window(MODEL)
    CONTROLLER = MainController(WINDOW, MODEL)
    WINDOW.run()

