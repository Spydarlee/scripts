#!/usr/bin/env python
# License: Public Domain - https://creativecommons.org/share-your-work/public-domain/cc0/

import string
from gimpfu import *
from array import array
	
def python_color_to_alpha_exact(image, layer, color):

	image_width = pdb.gimp_image_width(image)
	image_height = pdb.gimp_image_height(image)

	# Make sure this layer supports alpha so we can write to each pixel's alpha component
	layer.add_alpha()

	# Grab a pixel region (readonly)  covering the entire image and copy pixel data into an array
	source_region = layer.get_pixel_rgn(0, 0, image_width, image_height,False, False)
	source_pixels = array("B", source_region[0:image_width, 0:image_height])

	pixel_size = len(source_region[0,0])

	# Create another region (writeable) and an array that can store all our modified pixels
	destination_region = layer.get_pixel_rgn(0, 0, image_width, image_height, True, True)
	destination_pixels = array("B", "\x00" * (image_width * image_height * pixel_size))

	gimp.progress_init("Replacing color pixels with alpha...")

	x = 0
	y = 0

	# Loop through every pixel in the image/layer
	for y in xrange(0, (image_height-1)):
		for x in xrange(0, (image_width-1)):

			gimp.progress_update(1.0 * y/image_height)
			source_index = (x + image_width * y) * pixel_size
			pixel = source_pixels[source_index: source_index + pixel_size]

			# Check if this pixel matches are input color
			# If so, zero out the pixel's alpha value
			if pixel[0] == color[0] and pixel[1] == color[1] and pixel[2] == color[2]:
				pixel[3] = 0

			# Write the modified pixel out to our destination array
			destination_pixels[source_index: source_index + pixel_size] = pixel

	# Copy the whole array into the writeable pixel region
	destination_region[0:image_width, 0:image_height] = destination_pixels.tostring() 

	# Write our changes back over the original layer
	layer.flush()
	layer.merge_shadow(True)
	layer.update(0, 0, image_width,image_height)

	pdb.gimp_progress_end()	
	pdb.gimp_displays_flush()

# Register the plugin with Gimp so it appears in the Colors menu
register(
    "python_fu_color_to_alpha_exact",
    "Color To Alpha (Exact)",
    "Sets the alpha of any pixel matching the given RGB values to 0 (fully transparent)",
    "Karn Bianco",
    "Karn Bianco",
    "2018",
    "<Image>/Colors/Color To Alpha (Exact)",
    "RGBA*, GRAY*",
    [
    	(PF_COLOR, 'color', 'Color to match:', (255,0,255))
    ],
    [],
    python_color_to_alpha_exact)

main()