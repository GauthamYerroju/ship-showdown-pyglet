#!/usr/bin/env python
#
#       ship.py
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
from pyglet.text import Label
from pyglet import resource
from pyglet.image import load as load_image
from pyglet.window import key
from bullet import Bullet
from configs import *
import math

class ShipSprite(Sprite):
	
	def __init__(self, img, color=(255, 255, 255), **kwargs):
		super(ShipSprite, self).__init__(img, **kwargs)
		self.dx = self.dy = 0
		self.accel, self.decel = ACCEL, DECEL
		self.color = color
	
	def update(self, dt):
		# Regular Stuff
		self.x += self.dx * dt
		self.y += self.dy * dt
		# Deceleration Control
		if self.dx > 0: self.dx -= self.decel
		if self.dx < 0: self.dx += self.decel
		if self.dy > 0: self.dy -= self.decel
		if self.dy < 0: self.dy += self.decel
		# Bounce Control
		if self.x <= self.width/2:
			self.x = self.width/2
			self.dx = -self.dx
		if self.x >= SCREEN_W - self.width/2:
			self.x = SCREEN_W - self.width/2
			self.dx = -self.dx
		if self.y <= self.height/2:
			self.y = self.height/2
			self.dy = -self.dy
		if self.y >= SCREEN_H - self.height/2:
			self.y = SCREEN_H - self.height/2
			self.dy = -self.dy

class HUD(Label):
	
	def __init__(self, ship=None, **kwargs):
		super(HUD, self).__init__(**kwargs)
		self.ship = ship
		self.name = ship.name
		self.anchor_x = 'center'
		self.anchor_y = 'bottom'
		self.font_name = 'Arial'
		self.font_size = 16
		self.draw_health()
	
	def update(self):
		self.update_position()
	
	def update_position(self):
		self.x = self.ship.x
		self.y = self.ship.y + self.ship.height/2 + 10
	
	def draw_health(self):
		self.text = "%i" % self.ship.hp
		if self.ship.hp > 60: self.color = (255, 255, 255, 255)
		elif self.ship.hp > 40: self.color = (255, 255, 128, 255)
		elif self.ship.hp > 20: self.color = (255, 128, 0, 255)
		elif self.ship.hp > 0: self.color = (255, 64, 0, 255)
		else: self.color = (255, 0, 0, 255)


class Ship(ShipSprite, key.KeyStateHandler):
	
	global bullets
	global graphics_batch
	
	def __init__(self, sp1, controls, accel, decel, color, auto=False, **kwargs):
		img = load_pic(sp1)
		img.anchor_x = img.width/2
		img.anchor_y = img.height/2
		super(Ship, self).__init__(img, **kwargs)
		self.opponent = None
		self.keys = controls
		self.accel = accel
		self.decel = decel
		self.color = color
		self.hp = 100
		self.name = 'Player'
		self.hud = HUD(ship=self, **kwargs)
		self.bullet_timeout = 0
		self.set_facing()
		self.destroyed = False
		self.auto = auto
		self.auto_move = [False, False, False, False]
	
	def update(self, dt):
		if self.destroyed and self.opacity > 0:
			self.scale += self.scale/8
			self.opacity -= self.opacity/4
			if self.opacity < 5: self.opacity = 0
			super(Ship, self).update(dt)
			print self.opacity
			return
		# AI Update
		if self.auto: self.update_ai()
		# Directional Movement
		if self[self.keys[0]] or self.auto_move[0]:
			if self.dx > -MAX_SPEED: self.dx -= self.accel
		elif self[self.keys[2]] or self.auto_move[2]:
			if self.dx < MAX_SPEED: self.dx += self.accel
		if self[self.keys[1]] or self.auto_move[1]:
			if self.dy < MAX_SPEED: self.dy += self.accel
		elif self[self.keys[3]] or self.auto_move[3]:
			if self.dy > -MAX_SPEED: self.dy -= self.accel
		# Bullet fire
		if self.bullet_timeout > 0: self.bullet_timeout -= dt * FPS
		if (self[self.keys[4]] or self.auto) and self.bullet_timeout <= 0:
			self.spawn_bullet()
			self.bullet_timeout = BULLET_TIMEOUT
		# Superclass method call
		super(Ship, self).update(dt)
		# Face towards opponent
		self.set_facing()
		# Update HUD
		self.hud.update()
	
	def speed_x(self):
		return self.dx
	
	def speed_y(self):
		return self.dy
	
	def update_ai(self):
		if self.opponent == None:
			return
		if self.dy >= 0:
			self.auto_move[3] = False
			self.auto_move[1] = True
		else:
			self.auto_move[1] = False
			self.auto_move[3] = True
		dist_x = self.opponent.x - self.x
		if dist_x < 2*self.width:
			print 'try moving'
			if self.dx >= 0:
				'fffff'
				self.auto_move[0] = False
				self.auto_move[2] = True
			else:
				self.auto_move[2] = False
				self.auto_move[0] = True
	
	def set_facing(self):
		if self.opponent != None:
			x1, x2 = self.x, self.opponent.x
			if (x1 < x2) and self.rotation != 0:
				self.rotation = 0
				print 'Faced right'
			elif (x1 > x2) and self.rotation != 180:
				self.rotation = 180
				print 'Faced left'
	
	def spawn_bullet(self):
		x, y = self.position
		deg = self.rotation
		bp = load_pic('bullet.png')
		if deg == 0: x += self.width/2 + bp.width
		else: x -= self.width/2 + bp.width
		b = Bullet(bp, x, y, deg, batch=graphics_batch)
		snd_bullet.play()
		b.color = self.color
		bullets.append(b)
	
	def set_health(self, val):
		if val < 0: val = 0
		self.hp = val
		self.hud.draw_health()
		self.destroyed = val == 0
		if self.destroyed: self.hud.text = 'BOOM!'
	
	def ouch(self, val):
		self.set_health(self.hp - val)
	
	def bounce(self, ship):
		x_diff = self.x - ship.x
		x_sign = get_sign(x_diff)
		new_dx = math.fabs(self.dx) * x_sign
		self.dx = new_dx
		y_diff = self.y - ship.y
		y_sign = get_sign(y_diff)
		new_dy = math.fabs(self.dy) * y_sign
		self.dy = new_dy
	
	def delete(self):
		super(Ship, self).delete()
		self.hud.delete()
