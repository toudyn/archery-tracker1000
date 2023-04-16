# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 21:01:45 2022

@author: jerem
"""

import tkinter as tk
from tkinter import Canvas
import pandas as pd

class ArcheryVisualizer():
    
    def __init__(self, filename):
        self.canvas_x = 600
        self.canvas_y = 600
        self.canvas_scale = 8

        self.root = tk.Tk()
        self.root.title('Archery Visualizer')

        self.canvas = None
        self.target_line = None
        
        self.shots = dict()
        self.shots_df = None
        self.sessions = None
        self.current_session = None
        self.read_shots(filename)

        self.shot_markings = []
        
        self.current_session_text = tk.StringVar()
        self.update_session_counter()
        
        self.add_documentation()
        self.add_session_counter()
        self.set_up_canvas()

    def run(self):
        self.root.bind("<Key>", self.handle_keypress)
        self.root.mainloop()
    
    def handle_keypress(self, event):
        """
        Handles keypresses for keys actually used in the app.
        """
        if event.char == 'f':
            self.increment_session()
            self.update_target_face()
        elif event.char == 'd':
            self.decrement_session()
            self.update_target_face()
    
    def read_shots(self, filename):
        self.shots_df = pd.read_csv(filename)
        self.sessions = sorted(list(set(self.shots_df['date'])))
        for session in self.sessions:
            if self.current_session is None:
                self.current_session = session
            self.shots[session] = []
            for i, row in self.shots_df[self.shots_df['date']==session].iterrows():
                self.shots[session].append((row['x'], row['y']))
        

    def update_session_counter(self):
        self.current_session_text.set(f'Current session: {self.current_session}')

    def increment_session(self):
        """
        Increments to the next session if there is one.
        """
        i = self.sessions.index(self.current_session)
        if i < len(self.sessions) - 1:
            self.current_session = self.sessions[i+1]

            self.update_session_counter()

    def decrement_session(self):
        """
        Decrements the current session by 1 if there is a preceding one.
        """
        
        i = self.sessions.index(self.current_session)
        if i > 0:
            self.current_session = self.sessions[i-1]
    
        self.update_session_counter()

    def add_session_counter(self):
        txt = tk.StringVar()
        label_round = tk.Label(self.root, textvar = self.current_session_text)
        label_round.grid(row=1, column=2)

    def add_documentation(self):
        txt = tk.StringVar()
        label_doc = tk.Label(self.root, textvar = txt)
        documentation = """
        f - next session
        d - previous session
        """
        txt.set(documentation)
        label_doc.grid(row=1, column=1)

    def set_up_canvas(self):
        """
        Sets up canvas which holds the target
        """
        self.canvas = Canvas(self.root,
                             width=self.canvas_x,
                             height=self.canvas_y)
        self.canvas.configure(bg='slate gray')
        self.canvas.grid(column=1, columnspan=2)
        self.draw_target()

    def draw_circle(self, radius, fill=None):
        """
        Used for helping in setting up the target face
        """
        center_x = self.canvas_x/2
        center_y = self.canvas_y/2
        self.canvas.create_oval(center_x-radius,
                                center_y-radius,
                                center_x+radius,
                                center_y+radius, fill=fill)

    def draw_target(self):
        """
        Draws a target face - dimensions are for FITA 60cm face
        """
        circles = [(0, 'white'),
                   (3, 'white'),
                   (6, 'grey29'),
                   (9, 'grey29'),
                   (12, 'royal blue'),
                   (15, 'royal blue'),
                   (18, 'firebrick1'),
                   (21, 'firebrick1'),
                   (24, 'gold'),
                   (27, 'gold'),
                   (28.5, 'gold')]

        for circle in circles:
            radius_from_outside = circle[0]
            color = circle[1]
            self.draw_circle((30-radius_from_outside)*self.canvas_scale,
                             fill=color)

    def draw_shot(self, x, y, fill='black'):
        """
        Draws a single shot on the target face to denote a hit.
        """
        shot_radius = 3
        self.shot_markings.append(self.canvas.create_oval(x-shot_radius,
                                                          y-shot_radius,
                                                          x+shot_radius,
                                                          y+shot_radius,
                                                          fill = fill))

    def draw_shots(self):
        """
        Draws all shots for the current round and the current shot.
        """
        for shot in self.shots[self.current_session]:
            self.draw_shot(shot[0], shot[1])

    def erase_shots(self):
        """
        Erases all shots on the target face.
        """
        for mark in self.shot_markings:
            self.canvas.delete(mark)
    
    def update_target_face(self):
        self.erase_shots()
        self.draw_shots()
        
AV = ArcheryVisualizer('shots.csv')
AV.run()
