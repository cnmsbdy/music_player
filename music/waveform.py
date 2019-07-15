from pydub import AudioSegment
from matplotlib import pyplot as plot
from PIL import Image, ImageDraw
import numpy as np
import os


class WaveForm():

	BARS = 100
	BAR_HEIGHT = 60
	LINE_WIDTH = 5

	def __init__(self):
		self.dir = os.listdir(os.getcwd())

	def read_file(self):
		self.data = list()
		self.search_song = [file for file in self.dir if file.endswith('.wav')]
		for song in self.search_song:
			audio = AudioSegment.from_file(song)
			self.data.append(np.fromstring(audio._data, np.int16))
			fs = audio.frame_rate
		return self.data
	

	#Check end song and added +1 index
	def draw_graph(self):
		length = len(self.read_file()[1])
		RATIO = length/self.BARS
		_size = (128,128)
		count = 0
		maximum_item = 0
		max_array = []
		highest_line = 0
		for d in self.read_file()[0]:
			if count < RATIO:
				count = count + 1

				if abs(d) > maximum_item:
					maximum_item = abs(d)
			else:
				max_array.append(maximum_item)

				if maximum_item > highest_line:
					highest_line = maximum_item

				maximum_item = 0
				count = 1

		line_ratio = highest_line/self.BAR_HEIGHT

		im = Image.new('RGBA', (self.BARS * self.LINE_WIDTH, self.BAR_HEIGHT), (255, 255, 255, 1))
		draw = ImageDraw.Draw(im)

		current_x = 1
		for item in max_array:
			item_height = item/line_ratio

			current_y = (self.BAR_HEIGHT - item_height)/2
			draw.line((current_x, current_y, current_x, current_y + item_height), fill=(169, 171, 172), width=4)

			current_x = current_x + self.LINE_WIDTH
		im = im.convert('RGB')
		im.save('image.jpg')
		

a = WaveForm()
a.draw_graph()