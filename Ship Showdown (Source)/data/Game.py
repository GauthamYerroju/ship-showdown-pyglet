#!/usr/bin/env python
#
#       Game_Base.py
#       
#       Copyright 2009 Xion <Xion@UNREAL-093C4E1B>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from pyglet.window import Window
from pyglet.font import load as load_font
from pyglet.clock import ClockDisplay

class Game(Window):
	
	def __init__(self, scene=None, *args, **kwargs):
		super(Game, self).__init__(*args, **kwargs)
		self.fps_display = ClockDisplay(font=load_font('Arial', 24))
		self.scene = scene
		self.on_enter()
	
	def on_enter(self):
		pass
	
	def update(self, dt):
		if self.scene == None: return
		self.scene.update(dt)
	
	def on_draw(self):
		self.clear()
		self.fps_display.draw()
		if self.scene == None: return
		self.scene.on_draw()
	
	def change_scene(self, new_scene):
		if self.scene != None:
			self.scene.on_exit()
			for h in self.scene.event_handlers:
				self.remove_handlers(h)
		self.scene = new_scene
		if new_scene != None:
			self.scene.on_enter()
			for h in self.scene.event_handlers:
				self.push_handlers(h)
