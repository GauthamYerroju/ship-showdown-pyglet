#!/usr/bin/env python
#
#       bullet.py
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

from pyglet.sprite import Sprite
from configs import *
import math

class BulletSprite(Sprite):
	
	def __init__(self, img, **kwargs):
		super(BulletSprite, self).__init__(img, **kwargs)
		self.dx = self.dy = 0
		self.speed = BULLET_SPEED
		self.delete_flag = False
	
	def update(self, dt):
		# Regular Stuff
		self.x += self.dx * dt
		self.y += self.dy * dt
		# Out of bounds control
		if self.x <= self.width/2: self.delete_flag = True
		if self.x >= SCREEN_W - self.width/2: self.delete_flag = True
		if self.y <= self.height/2: self.delete_flag = True
		if self.y >= SCREEN_H - self.height/2: self.delete_flag = True

class Bullet(BulletSprite):
	
	def __init__(self, img, x, y, deg, **kwargs):
		super(Bullet, self).__init__(img, **kwargs)
		self.x, self.y = x, y
		self.rotation = deg
		dx = math.cos(-math.radians(deg))
		dy = math.sin(-math.radians(deg))
		self.dx = BULLET_SPEED * dx
		self.dy = BULLET_SPEED * dy
