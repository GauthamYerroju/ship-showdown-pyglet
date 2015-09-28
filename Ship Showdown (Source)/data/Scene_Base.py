#!/usr/bin/env python
#
#       Scene_Base.py
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

class Scene_Base(object):
	
	def __init__(self, *args, **kwargs):
		super(Scene_Base, self).__init__(*args, **kwargs)
		self.event_handlers = []
	
	def push_handlers(self, handler):
		self.event_handlers.append(handler)
	
	def on_enter(self):
		pass
	
	def update(self, dt):
		pass
	
	def on_draw(self):
		pass
	
	def on_exit(self):
		pass
