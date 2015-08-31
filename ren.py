# -*- coding: utf-8 -*-
import os

l = os.listdir('music3/')
for music in l:
	print music.encode('utf8').replace('副本', 'f')
	os.rename('e:\\sketch2music\\jsDrawLine\\music3\\'+music, \
	'e:\\sketch2music\\jsDrawLine\\music3\\'+music.replace(u'副本'.encode('utf8'), 'f'))
