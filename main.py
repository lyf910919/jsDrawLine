from strokeProcess import *
from aubioAnalysis import *
import os, sys
import matplotlib.pyplot as plt
# from sklearn.cluster import *
# from sklearn.preprocessing import MinMaxScaler as Scaler
import cPickle as pickle

def getAllMusicFeature(dir):
	f = open('musicInd.txt', 'w+')
	musicList = filter(lambda fileName: '.wav' in fileName, os.listdir(dir))
	musicFeature = []
	i = 1
	for music in musicList:
		print i, music
		print >> f, i, music
		i+=1
		musicFeature.append(getMusicFeature(dir+music))
	musicFeature = np.array(musicFeature)
	#f.close()
	return musicFeature

def learnParam(strokeFeature, musicFeature):
	if len(strokeFeature) < 4 or len(strokeFeature) != len(musicFeature):
		raise ValueError("stroke feature matrix size or music feature size error")

	b = np.array([[1] for i in range(len(strokeFeature))])
	strokeFeature = np.hstack((b, strokeFeature))
	model = np.linalg.solve(strokeFeature, musicFeature[:,0])
	for i in range(1, musicFeature.shape[1]):
		model = np.vstack((model, np.linalg.solve(strokeFeature, musicFeature[:,i])))
	print "learned model: "
	print model
	return model

def recommend(strokeFeature, model, musicFeature):
	strokeFeature = np.insert(strokeFeature, 0, 1)
	mappedFeature = np.dot(model, strokeFeature)
	musicFeature = np.vstack((mappedFeature, musicFeature))
	scaler = Scaler()
	musicFeature = scaler.fit_transform(musicFeature)
	
	#find nearest neighbor
	dist = [0 for i in range(len(musicFeature))]
	for i in range(1, len(musicFeature)):
		dist[i] = float(np.sqrt(np.sum((musicFeature[0] - musicFeature[i])**2)))

	sortedInd = sorted(range(len(musicFeature)), key=lambda i: dist[i])
	

	#all music ind were added 1, so return the ind - 1
	sortedInd = list(np.array(sortedInd[1:])-1)
	print 'recommendation order: ', sortedInd
	return sortedInd

def testFunctions():
	strokeFeature = np.array([[1,2,3], [6,5,8], [2,11,0], [23,71,111]])
	musicFeature = np.array([[1,0.3], [4,0.01], [7,0.7], [141,0.005]])
	model = [[-2.65397631, -0.82423858,  1.02749577,  0.80774112],\
	[ 0.33049915, -0.06717005,  0.04580372, -0.01831218]]
	learnParam(strokeFeature, musicFeature)
	recommend(np.array([2,11,0]), model, musicFeature)

def learnUserData(flieList, musicFeature):
	if len(fileList)  != 4:
		raise ValueError('less than 4 strokes!')
	strokeFeature = []
	for i in range(4):
		with open(fileList[i], 'r') as f:
			stroke = f.readline()
		data = stroke.split(' ')
		points = []
		i = 0
		while i + 2 < len(data):
			points.append(StrokePoint(int(data[i]), int(data[i+1]), int(data[i+2])))
			i += 3
		feature =  getSegFeature(points)
		strokeFeature.append([feature])
	strokeFeature = np.array(strokeFeature)
	model = learnParam(strokeFeature, musicFeature)
	return model

def returnMusic(strokeFile, model, musicFeature):
	with open(strokeFile, 'r') as f:
		stroke = f.readline()
	data = stroke.split(' ')
	points = []
	i = 0
	while i + 2 < len(data):
		points.append(StrokePoint(int(data[i]), int(data[i+1]), int(data[i+2])))
		i += 3
	strokeFeature =  getSegFeature(points)
	indList = recommend(strokeFeature, model, musicFeature)
	return indList

	# path = sys.argv[1]
	# musicFeature = getAllMusicFeature(path)
	# print musicFeature
	# np.savetxt('musicFeature_aubio.csv', musicFeature, delimiter=',')
	# musicFeature = np.genfromtxt('musicFeature_aubio.csv', delimiter=',')
	#plot
	# plt.xlabel('bpm')
	# plt.ylabel('pitch diff')
	# plt.scatter(musicFeature[:, 0], musicFeature[:, 1])
	# plt.show()

if __name__ == '__main__':
	musicFeature = np.genfromtxt('musicFeature_aubio.csv', delimiter=',')
	if sys.argv[1] == '-learn':
		if len(sys.argv) < 7:
			raise AssertionError("arguments less than 6")
		userName = sys.argv[2]
		fileList = []
		for i in range(3,7):
			fileList.append(sys.argv[i])
		model = learnUserData(fileList, musicFeature[[46, 48, 3, 29]])
		with open(userName+'model', 'wb+') as f:
			pickle.dump(f, model)
	elif sys.argv[1] == '-recommend':
		if len(sys.argv) < 4:
			raise AssertionError("arguments less than 3")
		userName = sys.argv[2]
		with open(userName+'model', 'rb') as f:
			model = pickle.load(f)
		indList = returnMusic(sys.argv[3], model, musicFeature)
		print indList[0], indList[len(indList)/3], \
		 indList[2*len(indList)/3], indList[-1]

'''
#file name preprocess
person = set()e
fileList = os.listdir(u'train')
for fileName in fileList:
	if fileName[0] == '.':
		continue
	p = fileName[0:fileName.find('_')]
	if p not in person:
		person.add(p)

#get feature vector from all files
all_feature = []
all_label = []
all_num_label = []
for p in person:
	feature = []
	for n in range(1, 11):
		fileName = 'train/' + p + '_' + str(n) + '.txt'
		print fileName
		f = open(fileName, 'r')
		stroke = f.readline()
		f.close()
		data = stroke.split(' ')
		points = []
		i = 0
		while i + 2 < len(data):
			points.append(StrokePoint(int(data[i]), int(data[i+1]), int(data[i+2])))
			i += 3

		#if the stroke is empty
		if len(points) < 2:
			continue

		#feature.append(getFeature(points))
		feature.append(getSegFeature(points))
		print len(feature)
		all_label.append(p+'_'+str(n)+'.txt')
		all_num_label.append(n)
	feature = np.vstack(feature)
	#normalize feature vector
	#feature = feature / feature.max(0)
	# scaler = Scaler()
	# feature = scaler.fit_transform(feature)
	all_feature.append(feature)

#save all features and label
all_feature = np.vstack(all_feature)
np.savetxt("res_seg.csv", all_feature, delimiter=",", fmt='%.5f')
all_num_label = np.array(all_num_label)
np.savetxt("label_seg.csv", all_num_label, delimiter=',', fmt='%d')

#save corresponding file name
f = open("res.txt", 'w')
for label in all_label:
	print >> f, label.encode('utf8')
f.close()

#variance of feature
print np.var(all_feature, 0)

#input for machine learning
X = all_feature
y = all_num_label

#kmeans clustering
N = 2
km = KMeans(n_clusters=N)
labels = km.fit_predict(all_feature)
print labels
res = [[] for i in range(N)]
res_num = [[] for i in range(N)]
for i in range(len(labels)):
	res[labels[i]].append(all_label[i].encode('utf8'))
	res_num[labels[i]].append(all_num_label[i])
centers = [[0, 0] for i in range(N)]
for i in range(N):
	cnt = [0 for j in range(10+1)]
	max_v, max_i = 0, 0
	for j in res_num[i]:
		cnt[j] += 1
		if cnt[j] > max_v:
			max_v = cnt[j]
			max_i = j
	centers[i] = [max_v, max_i]

f = open("cluster_seg.txt", 'w+')
for i in range(len(res)):
	out = ' '.join(res[i])
	print >> f, out
for i in range(N):
	print >> f, centers[i]
f.close()
'''