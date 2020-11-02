import urllib.request
from bs4 import BeautifulSoup
import os, sys
import hashlib
import numpy as np 
import imageio
import pandas as pd
from PIL import Image

import json
import pickle
#gimbalDownloader

class Downloader(object):
	def __init__(self, username, password, date, directory = None):
		super(Downloader, self).__init__()
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

	def download_1shot_i(self, i):
		self.download_1shot(self.ID_Shots[i])

	def download_all(self):
		for i in range(self.numShots):
			print("======== " + self.date_str + '\t' + str(i) + " ========")
			self.download_1shot(self.ID_Shots[i])
