# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 21:01:45 2022

@author: jerem
"""

import tkinter as tk
from tkinter import Canvas
import pandas as pd

class ArcheryScorer():
    
    def __init__(self):
        self.canvas_x = 600
        self.canvas_y = 600
        self.canvas_scale = 8

        self.root = tk.Tk()
        self.root.title('Archery Scorer')

        self.canvas = None
        self.target_line = None
        
        self.shots = {1:[]}
        self.current_round = 1
        self.current_shot = None
        self.shot_markings = []
        
        self.current_round_text = tk.StringVar()
        self.update_round_counter()
        
        self.add_documentation()
        self.add_round_counter()
        self.set_up_canvas()
        self.set_up_target_line()

    def run(self):
        self.root.bind("<Key>", self.handle_keypress)
        self.root.mainloop()
    
    def handle_keypress(self, event):
        """
        Handles keypresses for keys actually used in the app.
        """
        if event.char == 'f':
            self.save_current_shot()
            self.update_target_face()
        elif event.char == 'd':
            self.delete_last_shot()
            self.update_target_face()
        elif event.char == 'r':
            self.increment_round()
            self.update_target_face()
        elif event.char =='e':
            self.decrement_round()
            self.update_target_face()
        elif event.char == 's':
            self.save_shots()
    
    def save_shots(self):
        rounds = []
        shots = []
        x = []
        y = []
        for shot_round in self.shots:
            for i, shot in enumerate(self.shots[shot_round]):
                rounds.append(shot_round)
                shots.append(i+1)
                x.append(shot[0])
                y.append(shot[1])
        df = pd.DataFrame()
        df['date'] = []
        df['round'] = rounds
        df['shot'] = shots
        df['x'] = x
        df['y'] = y
        df['x_face'] = self.canvas_x
        df['y_face'] = self.canvas_y
        df['scale'] = self.canvas_scale
        df.to_csv('out.csv', index=False)

    def update_round_counter(self):
        self.current_round_text.set(f'Current round: {self.current_round}')

    def increment_round(self):
        """
        Increments the current round by 1 as long as there are saved shots
        or the next round already exists (in case saved shots are all deleted).
        Adds entry in the shots dict for new round if necessary.
        """
        if len(self.shots[self.current_round]) > 0 or (self.current_round+1 in self.shots):
            self.current_round += 1
            if self.current_round not in self.shots:
                self.shots[self.current_round] = []
            self.current_shot = None
            self.update_round_counter()
    
    def decrement_round(self):
        """
        Decrements the current round by 1 if that does not take the current
        round below 1.
        """
        if self.current_round > 1:
            self.current_round -= 1
            self.current_shots = None
            self.update_round_counter()
        
    def save_current_shot(self):
        if self.current_shot:
            self.shots[self.current_round].append(self.current_shot)
        self.current_shot = None

    def delete_last_shot(self):
        if len(self.shots[self.current_round]) > 0:
            self.shots[self.current_round].pop()
    
    def add_round_counter(self):
        txt = tk.StringVar()
        label_round = tk.Label(self.root, textvar = self.current_round_text)
        label_round.grid(row=1, column=2)

    def add_documentation(self):
        txt = tk.StringVar()
        label_doc = tk.Label(self.root, textvar = txt)
        documentation = """
        f - save shot
        d - delete previous shot
        r - next round
        e - previous round
        s - save
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
        
        self.canvas.bind('<Motion>', self.canvas_motion)
        self.canvas.bind('<Leave>', self.canvas_leave)
        self.canvas.bind("<Button-1>", self.canvas_click)

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

    def set_up_target_line(self):
        """
        Sets up a line that will join the center of the target face to the
        current pointer on the canvas - initializes to be invisible in the
        center of the target
        """
        self.target_line = self.canvas.create_line(self.canvas_x/2,
                                                   self.canvas_y/2,
                                                   self.canvas_x/2,
                                                   self.canvas_y/2,
                                                   width=2,
                                                   fill='SeaGreen1')
    def reset_target_line(self):
        """
        Makes the target line invisible by setting bounding box to the center
        of the target face
        """
        self.canvas.coords(self.target_line,
                           self.canvas_x/2,
                           self.canvas_y/2,
                           self.canvas_x/2,
                           self.canvas_y/2)
    
    def update_target_line(self, x, y):
        """
        Updates the target line to go from the center of the target face to
        the x and y positions provided
        """
        center_x = self.canvas_x/2
        center_y = self.canvas_y/2
        self.canvas.coords(self.target_line, x, y, center_x, center_y)
    
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
        for shot in self.shots[self.current_round]:
            self.draw_shot(shot[0], shot[1])
        
        if self.current_shot:
            self.draw_shot(self.current_shot[0],
                           self.current_shot[1],
                           fill='SeaGreen3')

    def erase_shots(self):
        """
        Erases all shots on the target face.
        """
        for mark in self.shot_markings:
            self.canvas.delete(mark)
    
    def update_target_face(self):
        self.erase_shots()
        self.draw_shots()
    
    def canvas_motion(self, event):
        """
        Tracks position of pointer over the target face on the canvas.
        This updates the target_line graphic
        """
        x, y = event.x, event.y
        self.update_target_line(x, y)
    
    def canvas_leave(self, event):
        """
        Tracks when the pointer is no longer over the target face on the
        canvas. Used to reset the target line graphic to be at the center
        of the target face.
        """
        self.reset_target_line()
    
    def canvas_click(self, event):
        """
        Tracks a click on the target face on the canvas. Used to designate
        a shot location before saving.
        """
        x, y = event.x, event.y
        self.current_shot = (x, y)
        self.update_target_face()
        
AS = ArcheryScorer()
AS.run()
