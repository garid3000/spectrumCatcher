



##################################################################################################

def slashChanger(someString):
	tmp = ''
	for char in someString:
		if char == '\\':
			tmp += '/'
		else:
			tmp +=char
	return tmp



class singleShot(object):
	"""docstring for singleShot"""
	def __init__(self, id, pics_dir, json_dir, crop_dir, full_dir, spec_dir, _rawBMPs):
		super(singleShot, self).__init__()
		self.id       = id
		self.pics_dir = pics_dir
		self.json_dir = json_dir
		self.crop_dir = crop_dir
		self.full_dir = full_dir
		self.spec_dir = spec_dir
		self.crop_img_dir = None

		self.plot_img_full = None
		self.plot_img_crop = None
		self.plot_img_spec = None
		self.rawBMPs  = _rawBMPs


		file = open(self.json_dir, 'r', encoding = 'utf-8')
		self.jsonDic = json.loads(file.read())
		file.close()

def refreshFolder(directory):
	directory = slashChanger(directory)
	print(directory)
	try:
		fnames = [s for s in os.listdir(directory) if os.path.isfile(directory + '/' + s) and '.jpeg' in s]
	except:
		return []
	print(fnames)
	fnames.sort()
	Fnames = [directory + '/' + s for s in fnames]

	mainThing = []
	for fname in fnames:
		tmp_pic_dir = directory + '/' + fname
		ID = fname.split('.')[0]
		tmp_json_dir = directory + '/' + ID + '.json' 		if os.path.isfile(directory + '/' + ID + '.json') else None
		tmp_crop_dir = directory + '/' + ID + '_crop.csv' 	if os.path.isfile(directory + '/' + ID + '_crop.csv') else None
		tmp_full_dir = directory + '/' + ID + '_full.csv' 	if os.path.isfile(directory + '/' + ID + '_full.csv') else None
		tmp_spec_dir = directory + '/' + ID + '_spec_NDVI.csv' if os.path.isfile(directory + '/' + ID + '_spec_NDVI.csv') else None
		_tmpRAWs_ = []
		for i in range(16):
			_tmpRaw_ = directory + '/raw_BMPs/' + ID + "_" + str(i) + '.bmp'
			print(_tmpRaw_, os.path.isfile(_tmpRaw_))
			if os.path.isfile(_tmpRaw_):
				_tmpRAWs_.append(_tmpRaw_)

		mainThing.append(singleShot(ID, tmp_pic_dir, tmp_json_dir, tmp_crop_dir, tmp_full_dir, tmp_spec_dir, _tmpRAWs_))
	
	try:
		os.mkdir(directory + "/meta")
	except:
		pass

	with open(directory + '/meta/about.meta', 'wb') as config_dictionary_file:
		pickle.dump(mainThing, config_dictionary_file)
	return mainThing


def get_spectrum(filename, startpixel, endpixel, outputfile = None):
	try:
		img = imageio.imread(filename)
	except:
		print("error image reading")
   
	if img.shape == (640, 480, 3):                  #for RGB bmp file (wihth blue/red lines)
		tmp = img[startpixel:endpixel, :, 0]        #assuming 3 channels are equal ,(so I'm only using the red channel)
	else:
		tmp = img[startpixel:endpixel, :]           #for mono bmp file (without blue/red lines)
	tmp = np.mean(tmp, 0)
   
	if outputfile != None:
		np.savetxt(outputfile, tmp, delimiter=',')
		print('saved as \"', outputfile, '\"')
	return tmp


def grayToWhite(grayNarray):
	grayTowhiteRATIO = np.array([0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709,
	   0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709,
	   0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709,
	   0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709,
	   0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709,
	   0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7709, 0.7708,
	   0.7688, 0.7665, 0.764 , 0.7601, 0.7552, 0.7493, 0.7424, 0.7348,
	   0.7261, 0.7162, 0.7056, 0.6944, 0.6829, 0.6712, 0.6595, 0.6479,
	   0.6367, 0.6267, 0.6179, 0.6098, 0.603 , 0.5975, 0.5923, 0.5867,
	   0.5812, 0.576 , 0.571 , 0.5661, 0.5614, 0.5569, 0.5526, 0.5479,
	   0.5428, 0.5377, 0.5328, 0.5281, 0.5238, 0.5201, 0.5169, 0.5138,
	   0.5109, 0.5083, 0.5055, 0.5028, 0.5002, 0.4979, 0.4958, 0.4941,
	   0.4927, 0.4916, 0.4904, 0.4892, 0.4882, 0.487 , 0.4858, 0.4845,
	   0.4834, 0.4824, 0.4812, 0.4802, 0.4792, 0.4781, 0.4768, 0.4754,
	   0.474 , 0.4727, 0.4715, 0.4703, 0.4693, 0.4685, 0.4677, 0.467 ,
	   0.4663, 0.4654, 0.4646, 0.4638, 0.4631, 0.4624, 0.4618, 0.4611,
	   0.4604, 0.4595, 0.4586, 0.4577, 0.4568, 0.4559, 0.4551, 0.4542,
	   0.4534, 0.4526, 0.452 , 0.4515, 0.4512, 0.4512, 0.4512, 0.4512,
	   0.4513, 0.4514, 0.4516, 0.4519, 0.4521, 0.4522, 0.4522, 0.4521,
	   0.4519, 0.4516, 0.4512, 0.4506, 0.45  , 0.4493, 0.4484, 0.4476,
	   0.4468, 0.446 , 0.4454, 0.4448, 0.4443, 0.4439, 0.4436, 0.4434,
	   0.4434, 0.4436, 0.4438, 0.4442, 0.4447, 0.4452, 0.4458, 0.4465,
	   0.4472, 0.4478, 0.4485, 0.4492, 0.4499, 0.4506, 0.4514, 0.4522,
	   0.4532, 0.4543, 0.4556, 0.4571, 0.4588, 0.4607, 0.4629, 0.4653,
	   0.4679, 0.4706, 0.4737, 0.477 , 0.4808, 0.4848, 0.4889, 0.4932,
	   0.4979, 0.5027, 0.5077, 0.5129, 0.5181, 0.5234, 0.529 , 0.5345,
	   0.5401, 0.5455, 0.551 , 0.5565, 0.5622, 0.568 , 0.5737, 0.5792,
	   0.5847, 0.5904, 0.5962, 0.602 , 0.6079, 0.6137, 0.6197, 0.6259,
	   0.6323, 0.6388, 0.6455, 0.6522, 0.659 , 0.666 , 0.6729, 0.6799,
	   0.687 , 0.6942, 0.7017, 0.7091, 0.7165, 0.724 , 0.7314, 0.739 ,
	   0.7465, 0.754 , 0.7614, 0.7687, 0.776 , 0.7832, 0.7903, 0.7974,
	   0.8044, 0.8112, 0.8178, 0.8242, 0.8303, 0.8362, 0.8417, 0.8469,
	   0.8519, 0.8568, 0.8614, 0.8658, 0.8701, 0.8742, 0.8781, 0.8816,
	   0.885 , 0.8882, 0.8913, 0.8942, 0.8968, 0.8991, 0.9012, 0.9033,
	   0.9052, 0.9069, 0.9084, 0.9099, 0.9112, 0.9124, 0.9134, 0.9145,
	   0.9156, 0.9165, 0.9174, 0.9182, 0.9189, 0.9196, 0.9204, 0.9212,
	   0.922 , 0.9227, 0.9234, 0.9239, 0.9243, 0.9248, 0.9252, 0.9256,
	   0.926 , 0.9264, 0.9267, 0.927 , 0.9272, 0.9274, 0.9275, 0.9277,
	   0.9277, 0.9277, 0.9277, 0.9278, 0.9279, 0.928 , 0.9281, 0.9283,
	   0.9284, 0.9286, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287,
	   0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287, 0.9287])
	
	return (grayNarray - 16) / grayTowhiteRATIO + 16 
# def readMdata(directory):
# 	if (os.path.isfile(directory + '/meta/about.meta')):
# 		try:
# 			with open(directory + '/meta/about.meta', 'rb') as config_dictionary_file:
# 				mainThing = pickle.load(config_dictionary_file)
# 			return mainThing
# 		except:
# 			return None
# 	return refreshFolder(directory)
# # refreshFolder(sys.aasdrgv[1])