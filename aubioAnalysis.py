import sys
import aubio
from aubio import source, tempo, pvoc, filterbank, fvec, pitch, freqtomidi
import numpy as np

def getBmp(path, params={}):
	try:
		win_s = params['win_s']
		samplerate = params['samplerate']
		hop_s = params['hop_s']
	except:
		#default:
		samplerate, win_s, hop_s = 44100, 1024, 512

	s = source(path, samplerate, hop_s)
	samplerate = s.samplerate
	o = tempo("specdiff", win_s, hop_s, samplerate)

	#list of beats, in samples
	beats = []
	#Total number of frames read
	total_frames = 0

	while True:
		samples, read = s()
		is_beat = o(samples)
		if is_beat:
			this_beat = o.get_last_s()
			beats.append(this_beat)
		total_frames += read
		if read < hop_s:
			break

	bpms = 60./np.diff(beats)
	b = np.median(bpms)
	return b

def getMelEnergy(path):
	win_s = 512 		#fft size
	hop_s = win_s / 4 	#hop size

	samplerate = 0
	s = source(path, samplerate, hop_s)
	samplerate = s.samplerate

	pv = pvoc(win_s, hop_s)
	f = filterbank(40, win_s)
	f.set_mel_coeffs_slaney(samplerate)

	energies = np.zeros((40, ))
	o = {}

	total_frames = 0
	downsample = 2

	while True:
		samples, read = s()
		fftgrain = pv(samples)
		new_energies = f(fftgrain)
		energies = np.vstack([energies, new_energies])
		total_frames += read
		if read < hop_s:
			break
	return energies

def getPitchDiff(path):
	downsample = 1
	samplerate = 44100 / downsample

	win_s = 4096 / downsample # fft size
	hop_s = 512  / downsample # hop size

	s = source(path, samplerate, hop_s)
	samplerate = s.samplerate

	tolerance = 0.8

	pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
	pitch_o.set_unit("midi")
	pitch_o.set_tolerance(tolerance)

	pitches = []
	confidences = []

	# total number of frames read
	total_frames = 0
	while True:
	    samples, read = s()
	    pitch = pitch_o(samples)[0]
	    #pitch = int(round(pitch))
	    confidence = pitch_o.get_confidence()
	    #if confidence < 0.8: pitch = 0.
	    #print "%f %f %f" % (total_frames / float(samplerate), pitch, confidence)
	    pitches += [pitch]
	    confidences += [confidence]
	    total_frames += read
	    if read < hop_s: break
	return np.median(np.fabs(np.diff(pitches)))

def getMusicFeature(path):
	bpm = getBmp(path)
	pitchDiff = getPitchDiff(path)
	return bpm, pitchDiff

if __name__ == '__main__':
	for f in sys.argv[1:]:
		bpm = getBmp(f)
		pitchDiff = getPitchDiff(f)
		print bpm, pitchDiff