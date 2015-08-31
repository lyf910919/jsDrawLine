import sys
import cv2
import numpy as np
from math import *

class StrokePoint:
	def __init__(self, x, y, t):
		self.x = x
		self.y = y
		self.t = t

	def show(self):
		print self.x, self.y, self.t

class Segment:
	def __init__(self, a, b):
		self.begin = a
		self.end = b
		self.length = sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2))
		self.time = fabs(b.t - a.t)

def getCurvature(points):
	x, y = [], []
	for i in range(len(points)):
		x.append(points[i].x)
		y.append(points[i].y)
	x, y = np.array(x), np.array(y)
	dx_dt = np.gradient(x)
	dy_dt = np.gradient(y)
	invalid = []
	for i in range(len(dx_dt)):
		if dx_dt[i] == 0 and dy_dt[i] == 0:
			invalid.append(i)
	dx_dt = np.delete(dx_dt, invalid)
	dy_dt = np.delete(dy_dt, invalid)
	xdd = np.gradient(dx_dt / np.sqrt(dx_dt**2 + dy_dt**2))
	ydd = np.gradient(dy_dt / np.sqrt(dx_dt**2 + dy_dt**2))
	dd = np.sqrt(xdd**2 + ydd**2)
	corner = filter(lambda i: dd[i] > 0.3, range(len(dd)))
	dx_dt2 = np.gradient(dx_dt)
	dy_dt2 = np.gradient(dy_dt)
	denominator = (dx_dt**2 + dy_dt**2)**1.5
	curvature = np.abs(dx_dt2 * dy_dt - dy_dt2 * dx_dt) / denominator
	curvature[denominator == 0] = 0
	return curvature, corner

def getVelocityAndAcceration(points):
	x, y, t = [], [], []
	for i in range(len(points)):
		x.append(points[i].x)
		y.append(points[i].y)
		t.append(points[i].t)
	x, y, t = np.array(x), np.array(y), np.array(t)
	dx_dt = np.gradient(x) / np.gradient(t)
	dx_dt[np.gradient(t) == 0] = 0
	dy_dt = np.gradient(y) / np.gradient(t)
	dy_dt[np.gradient(t) == 0] = 0
	dx_dt2 = np.gradient(dx_dt) / np.gradient(t)
	dx_dt2[np.gradient(t) == 0] = 0
	dy_dt2 = np.gradient(dy_dt) / np.gradient(t)
	dy_dt2[np.gradient(t) == 0] = 0
	denominator = (dx_dt**2 + dy_dt**2)**1.5
	curvature = np.abs(dx_dt2 * dy_dt - dy_dt2 * dx_dt) / denominator
	curvature[denominator == 0] = 0
	return dx_dt, dy_dt, dx_dt2, dy_dt2, curvature


def getFeature(points):
	#get all segment
	segments = []
	for i in range(1, len(points)):
		segments.append(Segment(points[i-1], points[i]))

	#get total length and time
	length, time = 0, 0
	for i in range(len(segments)):
		length += segments[i].length
		time += segments[i].time


	#get curvature
	curvature = getCurvature(points)

	#get velocity and acceration
	dx_dt, dy_dt, dx_dt2, dy_dt2, curvature2 = getVelocityAndAcceration(points)
	velocity = np.sqrt(dx_dt**2 + dy_dt**2)
	acceration = np.sqrt(dx_dt2**2 + dy_dt2**2)


	# print 'length: ', length
	# print 'time: ', time / 1000.0
	# print 'velocity: ', float(length) / time
	# print 'velocity2: ', velocity.mean()
	# print 'acceration: ', acceration.mean()
	# print 'curvature: ', curvature.max(), curvature.mean(), curvature.min()
	# print 'curvature2: ', curvature2.max(), curvature2.mean(), curvature2.min()
	# print 'curvature > 1: ', len(curvature[curvature > 1.5])
	# print 'curvature2 > 1: ', len(curvature2[curvature2 > 1.5])
	# print 'curvatureSum / length: ', curvature.sum() / length

	#get feature vector
	feature = []
	feature.append(float(length) / time)
	feature.append(acceration.mean())
	feature.append(curvature2.mean())
	feature += [np.percentile(velocity, 25), np.percentile(velocity, 50), \
	np.percentile(velocity, 75)]
	feature += [np.percentile(acceration, 25), np.percentile(acceration, 50), \
	np.percentile(acceration, 75)]
	feature += [np.percentile(curvature2, 25), np.percentile(curvature2, 50), \
	np.percentile(curvature2, 75)]
	#approximation of number of corner points
	feature.append(len(curvature2[curvature2 > 1.5]))

	#map points on image
	# src = cv2.imread(sys.argv[2], 1)
	# for i in range(len(curvature)):
	# 	cv2.circle(src, (points[i].x, points[i].y), 2, (0,255,0), -1)
	# 	if curvature[i] > 0.8:
	# 		cv2.circle(src, (points[i].x, points[i].y), 2, (0,0,255), -1)

	# cv2.namedWindow("points", cv2.WINDOW_NORMAL)
	# cv2.imshow("points", src)
	# cv2.waitKey(0)
	return np.array(feature)

def getSegFeature(points):
	xy = [[points[i].x, points[i].y] for i in range(len(points))]
	xy = np.array(xy)
	approx = cv2.approxPolyDP(xy, 10, False)
	approx = np.array([[approx[i][0][0], approx[i][0][1]] for i in range(len(approx))])
	# print approx, len(approx)
	ind = []
	j = 0
	for i in range(len(approx)):
		query = list(approx[i])
		while j < len(xy):
			if list(xy[j]) == query:
				ind.append(j)
				break
			j += 1
	time = [points[i].t for i in ind]
	time = np.array(time)
	# print time, len(time)

	# get segment lengths
	segments = np.sqrt(np.sum((approx[1:] - approx[:-1])**2, 1))
	# print segments
	# print np.median(segments)

	#get segment durations
	durations = time[1:] - time[:-1]
	# print durations
	# print np.median(durations)

	#get segment velocitys
	velocity = segments / durations
	velocity = velocity[np.logical_not(np.isnan(velocity))]#avoid nan

	# get segment angles
	vect = (approx[1:] - approx[:-1]) / np.transpose(np.vstack([segments, segments])) #direction vector
	cosine = np.sum(vect[1:] * vect[:-1], 1)
	angles = np.arccos(cosine)

	return np.median(segments), np.median(velocity), np.median(angles)

if __name__ == '__main__':
	with open(sys.argv[1], 'r') as f:
		stroke = f.readline()
	data = stroke.split(' ')
	points = []
	i = 0
	while i + 2 < len(data):
		points.append(StrokePoint(int(data[i]), int(data[i+1]), int(data[i+2])))
		i += 3
	print getSegFeature(points)

	
	#cur, corner = getCurvature(points)
	#map points on image
	# src = cv2.imread(sys.argv[1].replace('.txt', '.jpg').replace('stroke', 'img'), 1)

	# for p in approx:
	# 	print p
	# 	cv2.circle(src, (p[0][0], p[0][1]), 2, (0,0,255), -1)
	# 	# if curvature[i] > 0.8:
	# 	# 	cv2.circle(src, (points[i].x, points[i].y), 2, (0,0,255), -1)

	# cv2.namedWindow("points", cv2.WINDOW_NORMAL)
	# cv2.imshow("points", src)
	# cv2.waitKey(0)