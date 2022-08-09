def onValueChange(par, prev):
	# use par.eval() to get current value
	name = par.name
	val = par.eval()

	if name == 'Currentpair':
		current = parent().par.Currentpair.eval()
		devices = parent().par.Devices.eval()
		devices = devices.split(',')
		parent().par.Ids = '{}, {}'.format(devices[current], devices[current+1])
	return

def onPulse(par):
	name = par.name
	
	if name == 'Calibrate':
		mode = parent().par.Mode.eval()
		pair = ( int(parent().par.Specifypairx), 
				 int(parent().par.Specifypairy) )
		parent().Calibrate(pair=pair, mode=mode)
		
	elif name == 'Refine':
		pair = ( int(parent().par.Specifypairx), 
				 int(parent().par.Specifypairy) )
		parent().Refine(pair=pair)
		
	elif name == 'Gatherkinects':
		op('recognitionScript').run()

	return

def onExpressionChange(par, val, prev):
	return

def onExportChange(par, val, prev):
	return

def onEnableChange(par, val, prev):
	return

def onModeChange(par, val, prev):
	return
	