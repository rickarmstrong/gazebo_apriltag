#!/usr/bin/env python3
import os
import cv2

# Texture size must be power of two. We resize the images from apriltag-imgs to this size.
# With the default tag image size (10pix), tags will not be clearly rendered due to rescaling and interpolation.
TAG_SIZE_PIX = 2048
THUMB_SIZE_PIX = 256
TAG_COUNT = 16  # Generate this many tags, with IDs starting at zero.

class Generator:
	def __init__(self):
		with open('template/model.sdf', 'r') as f:
			self.sdf_template = f.read()

		with open('template/model.config', 'r') as f:
			self.config_template = f.read()

	def generate(self, tag_directory, tag_name, tag_size, thumb_size):
		img = cv2.imread('%s/%s.png' % (tag_directory, tag_name), cv2.IMREAD_UNCHANGED)
		img_full = cv2.resize(img, (tag_size, tag_size), interpolation=cv2.INTER_NEAREST)
		img_thumb = cv2.resize(img, (thumb_size, thumb_size), interpolation=cv2.INTER_NEAREST)

		if not os.path.exists('models/%s/materials/textures' % tag_name):
			os.makedirs('models/%s/materials/textures' % tag_name)

		if not os.path.exists('models/%s/thumbnails' % tag_name):
			os.makedirs('models/%s/thumbnails' % tag_name)

		with open('models/%s/model.sdf' % tag_name, 'w') as f:
			f.write(self.sdf_template.replace('tag36_11_00000', tag_name))

		with open('models/%s/model.config' % tag_name, 'w') as f:
			f.write(self.config_template.replace('tag36_11_00000', tag_name))

		cv2.imwrite('models/%s/materials/textures/%s.png' % (tag_name, tag_name), img_full)
		cv2.imwrite('models/%s/thumbnails/%s.png' % (tag_name, tag_name), img_thumb)


def main():
	generator = Generator()
	for i in range(TAG_COUNT):
		generator.generate('apriltag-imgs/tagCircle21h7', 'tag21_07_%05d' % i, TAG_SIZE_PIX, THUMB_SIZE_PIX)


if __name__ == '__main__':
	main()
