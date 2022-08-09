def destroyKinects():
	"""
	Clear all except first kinect
	"""
	finder = op('opfind1')
	for i in reversed(range(finder.numRows - 2)):
		p = finder[i+2, 'path']
		op(p).destroy()
	return

def createKinects():
	"""
	Create all other devices
	"""
	n = parent().par.Numberofdevices.eval()
	template = op('Azure1')
	for i in range(n - 1):
		i += 1
		o = parent().copy(template)
		o.nodeX = template.nodeX
		o.nodeY = template.nodeY - 200*i
		o.par.clone = template.name
	return

def recognizeKinects():
	"""
	Gather info from all devices
	"""
	target 	= op(parent().par.Inputsop)
	kinects = target.op('kinectazure1').par.sensor.menuNames
	n 	=  len(kinects)
	pairs = n -1
	options = pairs - 1
	parent().par.Numberofdevices = n
	parent().par.Numberofpairs = pairs
	parent().par.Devices = ','.join(kinects)
	parent().par.Currentpair.max = options
	parent().par.Currentpair.normMax = options
	return

def gatherKinects():
	recognizeKinects()
	destroyKinects()
	createKinects()
	return

gatherKinects()


