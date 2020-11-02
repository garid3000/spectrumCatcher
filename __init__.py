import urllib.request
from bs4 import BeautifulSoup
import os, sys
import hashlib
import numpy as np 
import imageio
from PIL import Image

import json
import pickle
#gimbalDownloader

class downloader(object):
	def __init__(self, username, password, date, directory = None):
		super(downloader, self).__init__()
		self.username    = username
		self.password    = password
		self.date_str    = date
		self.directory   = directory if directory != None else date
		# self.directoryBMP= self.directory + '/raw_BMPs'
		self.pass_hex    = None
		self.url         = None
		self.numShots    = 0
		self.ID_Shots	 = []

		# self.parsed_html = None

	def checkDir(self):
		return os.path.isdir(self.directory)
	def mkdir(self):
		if self.checkDir():
			return True
		else:
			try:
				os.mkdir(self.directory)
				# os.mkdir(self.directoryBMP)
				return True
			except:
				return False
	
	def passConvert(self):
		hash_obj = hashlib.md5(self.password.encode())
		self.pass_hex = hash_obj.hexdigest()
	
	def mkUrl(self):
		self.passConvert()
		self.url = 'http://spectrumcatcher.polarstarspace.com/veggie/report/report.php?id=' + self.username + "&v=103&c=" + self.pass_hex + "&data_day=" + self.date_str
		# print(url)

	def downloadUrl(self):
		self.mkUrl()
		try:
			urllib.request.urlretrieve(self.url, 'new_all_page1day.html')
			return True
		except:
			return False
	def processHTML(self):
		self.mkdir()
		self.downloadUrl()
		html = open('new_all_page1day.html', 'r',  encoding='utf-8').read()
		parsed_html = BeautifulSoup(html)

		x = parsed_html.body.find('table', attrs={'class':'table table-hover'})
		imgTimes = []
		try:
			for i in range(len(x)-1):
				tmp = str(x.contents[i+1])
				tmp1 = tmp.split("\"")[1].split('_')
				tmp2 = tmp1[-3] + '_'+ tmp1[-2]
				imgTimes.append(tmp2)
				print(i, '\t',  tmp2)
			self.numShots = len(imgTimes)
			self.ID_Shots = imgTimes
			return True
		except:
			return False
			#probably because of download error or no shots in that day

	def download_1shot(self, each_image_id):
		tmp = 'http://spectrumcatcher.polarstarspace.com/veggie/report/view_report.php?id='+self.username+'&v=103&c='+self.pass_hex+'&fname=VeggieCamera_crops_spectrum_' # 20191213_140027_0.bmp'
		tmp = tmp + each_image_id + '_0.bmp'
		print(tmp)
		urllib.request.urlretrieve(tmp,  "tmp.tmp")

		#reading the which farm, & healthy or not
		html = open('tmp.tmp', 'r' ,  encoding='utf-8').read()
		parsed_html = BeautifulSoup(html)
		tmp = parsed_html.body.main.find('div', attrs={'class':'info-title'}).text
		tag = tmp.split(']')[-2].split('[')[1]
		tag = each_image_id.split('_')[1][:2] + 'h_' + tag  # this is also the folder
		#info: angle, time, etc
		x = parsed_html.body.main.div.div.find('div', attrs = {'class':'ndvi-table slider'})
		x.find('div', attrs = {'class':'ndvi-text'})
		tracks = x.find_all('div', {'class':"ndvi-text"})
		infoOfShots = tracks[-2].text
		Pitch   = infoOfShots.split('：')[3][:5]
		Roll    = infoOfShots.split('：')[4][:5]
		Azimuth = infoOfShots.split('：')[5][:5]
		Exposure= infoOfShots.split('：')[7][:5]
		#     print(Pitch, Roll, Azimuth, Exposure, end = '')


		#folder uusgeh gej oroldoh
		try:
		    os.mkdir(self.directory + "/" + tag)
		except:
		    pass


		try:
		    os.mkdir(self.directory + "/" + tag + '/raw_BMPs')
		except:
		    pass




		try:
		    os.mkdir(self.directory + "/" + tag + '/OriginalRGB')
		except:
		    pass


		urlname = 'http://spectrumcatcher.polarstarspace.com/veggie/results/'+self.username+'/' + each_image_id + "_crop.csv"
		print(self.directory[-2:], tag, urlname)
		urllib.request.urlretrieve(urlname,  self.directory + "/" + tag  + '/' + each_image_id + 
		#                                '_' + Pitch    +
		#                                '_' + Roll     +
		#                                '_' + Azimuth  +
		#                                '_' + Exposure +
		                           "_crop.csv")

		urlname = 'http://spectrumcatcher.polarstarspace.com/veggie/results/'+self.username+'/' + each_image_id + "_full.csv"
		print(self.directory[-2:],  tag, urlname)
		urllib.request.urlretrieve(urlname,  self.directory + "/" + tag  + '/' + each_image_id + 
		#                                '_' + Pitch    +
		#                                '_' + Roll     +
		#                                '_' + Azimuth  +
		#                                '_' + Exposure +
		                           "_full.csv")


		urlname = 'http://spectrumcatcher.polarstarspace.com/veggie/results/'+self.username+'/' + each_image_id + "_spec_NDVI.csv"
		print(self.directory[-2:],  tag, urlname)
		urllib.request.urlretrieve(urlname,  self.directory + "/" + tag  + '/' + each_image_id + 
		#                                '_' + Pitch    +
		#                                '_' + Roll     +
		#                                '_' + Azimuth  +
		#                                '_' + Exposure +
		                           "_spec_NDVI.csv")


		urlname = 'http://spectrumcatcher.polarstarspace.com/veggie/results/'+self.username+'/VeggieCamera_crops_device_' + each_image_id + ".json"
		print(self.directory[-2:],  tag, urlname)
		urllib.request.urlretrieve(urlname,  self.directory + "/" + tag  + '/' + each_image_id + 
		#                                '_' + Pitch    +
		#                                '_' + Roll     +
		#                                '_' + Azimuth  +
		#                                '_' + Exposure +
		                           ".json")



		# print(day[-2:], count, tag, urlname)

		urlname = 'http://spectrumcatcher.polarstarspace.com/veggie/report/view_photo.php?id='+self.username+'&pic_id=' + each_image_id
		print(self.directory[-2:],  tag, urlname)
		urllib.request.urlretrieve(urlname,  self.directory + "/" + tag  + '/' + each_image_id + 
		#                                '_' + Pitch    +
		#                                '_' + Roll     +
		#                                '_' + Azimuth  +
		#                                '_' + Exposure +
		                           ".jpeg")

		#requested by Kuriki-san that I don't have to download spectrometer raw image
		urlname = 'http://spectrumcatcher.polarstarspace.com/veggie/results/'+self.username+'/' + each_image_id + "_rotate.png"
		print(self.directory[-2:], tag, urlname)
		urllib.request.urlretrieve(urlname,  self.directory + "/" + tag  + '/' + each_image_id + 
		#                                '_' + Pitch    +
		#                                '_' + Roll     +
		#                                '_' + Azimuth  +
		#                                '_' + Exposure +
		                           ".png")

		#urlname = 'http://spectrumcatcher.polarstarspace.com/veggie/results/'+self.username+'/' + each_image_id + "_rotate.png"
		for iii in range(16):
			urlname	= 'http://spectrumcatcher.polarstarspace.com/veggie/results/'+self.username+'/VeggieCamera_crops_spectrum_'+each_image_id+'_'+str(iii)+'.bmp'
			print(self.directory[-2:], tag, urlname)
			try:
				fName = self.directory + "/" + tag  + '/raw_BMPs/' + each_image_id + "_"+str(iii)+".bmp"
				urllib.request.urlretrieve(urlname,  fName)
				im = Image.open(fName)
				tmpy = np.array(im)
				im = Image.fromarray(tmpy.transpose()).transpose(Image.FLIP_LEFT_RIGHT)
				# im = Image.fromarray(tmpy.transpose().transpose(Image.FLIP_LEFT_RIGHT))

				im.save(fName)
				print('saved')
			except:
				print("\t\tno:", each_image_id, iii)
		urlname	= "http://spectrumcatcher.polarstarspace.com/veggie/results/"+self.username+"/VeggieCamera_crops_picture_" + each_image_id + ".jpg"
		#'http://spectrumcatcher.polarstarspace.com/veggie/results/'+self.username+'/VeggieCamera_crops_spectrum_'+each_image_id+'_'+str(iii)+'.bmp'
		print(self.directory[-2:], tag, urlname)
		urllib.request.urlretrieve(urlname,  self.directory + "/" + tag  + '/OriginalRGB/' + each_image_id + "_.jpg")



	def download_1shot_i(self, i):
		self.download_1shot(self.ID_Shots[i])

	def download_all(self):
		for i in range(self.numShots):
			print("======== " + self.date_str + '\t' + str(i) + " ========")
			self.download_1shot(self.ID_Shots[i])





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