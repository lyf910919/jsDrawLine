from strokeProcess import *
import cPickle as pickle
from sklearn.preprocessing import MinMaxScaler as Scaler

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
		strokeFeature.append(feature)
	strokeFeature = np.array(strokeFeature)
	model = learnParam(strokeFeature, musicFeature)
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

if __name__ == '__main__':
	sys.stderr = open('errlog.txt', 'w+')
	# sys.stdout = open('outlog.txt', 'w+')
	musicFeature = np.genfromtxt('musicFeature_aubio.csv', delimiter=',')
	if sys.argv[1] == '-learn':
		print sys.argv
		if len(sys.argv) != 7:
			raise AssertionError('number of arguments not right!')
		fileList = []
		userName = sys.argv[2]
		for i in range(3,7):
			fileList.append(sys.argv[i])
		model = learnUserData(fileList, musicFeature[[46, 48, 3, 29]])
		with open(userName+'model', 'wb+') as f:
			pickle.dump(model, f)
	elif sys.argv[1] == '-recommend':
		if len(sys.argv) != 4:
			raise AssertionError('number of arguments not right!')
		with open(sys.argv[2]+'model', 'rb') as f:
			model = pickle.load(f)
		indList = returnMusic(sys.argv[3], model, musicFeature)
		print indList[0], indList[len(indList)/3], \
		indList[2*len(indList)/3], indList[-1]

	sys.stderr.close()
	sys.stderr = sys.__stderr__
	# sys.stdout.close()
	# sys.stdout = sys.__stdout__