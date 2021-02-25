#!/usr/bin/env python2
# License: Public Domain - https://creativecommons.org/share-your-work/public-domain/cc0/

from gimpfu import *
import math

def create_spritesheet(image, singleRow, widthCells, heightCells):

    # Grab all the layers from the original image, each one of which will become an animation frame
    layers = image.layers
    numLayers = len(layers)

    # Work out how many rows and columns we need for each of our layers/animation frames
    if singleRow:
        numRows = 1
        numCols=numLayers
    else:
        if widthCells != 0 or heightCells !=0:
            if widthCells !=0 and heightCells !=0: #fixed
                numRows=heightCells
                numCols=widthCells
            else:
                if widthCells !=0: #width given, calculate height
                    numCols=widthCells
                    numRows=int(math.ceil(numLayers/widthCells))
                else: #height given, calculate width
                    numRows=heightCells
                    numCols=int(math.ceil(numLayers/heightCells))
        else: #auto
            numRows=int(math.ceil(math.sqrt(numLayers)))
            numCols=numRows

    # And then determine the size of our new image based on the number of rows and columns
    newImgWidth = image.width * numCols
    newImgHeight = image.height * numRows

    # Create a new image and a single layer that fills the entire canvas
    newImage = gimp.Image(newImgWidth, newImgHeight, RGB)
    newLayer = gimp.Layer(newImage, "Spritesheet", newImgWidth, newImgHeight, RGBA_IMAGE, 100, NORMAL_MODE)
    newImage.add_layer(newLayer, 1)

    # Clear any selections on the original image to esure we copy each layer in its entirety
    pdb.gimp_selection_none(image)

    # Layers are in the reverse order we want them so start at the end of the list and work backwards
    layerIndex = (numLayers - 1)

    # Loop over our spritesheet grid filling each one row at a time
    for y in xrange(0, numRows):
        for x in xrange(0, numCols):
            #Pre-process the layer to make sure we copy over a layer with a size the same as the image
            
            #Get layer's size and offsets to restore after copying its contents over
            lOffX, lOffY=pdb.gimp_drawable_offsets(layers[layerIndex])
            lW=pdb.gimp_drawable_width(layers[layerIndex])
            lH=pdb.gimp_drawable_height(layers[layerIndex])
            #Resize the layer to image size
            pdb.gimp_layer_resize_to_image_size(layers[layerIndex])
            # Copy the layer's contents and paste it into a "floating" layer in the new image
            pdb.gimp_edit_copy(layers[layerIndex])
            floatingLayer = pdb.gimp_edit_paste(newLayer, TRUE)
            #Restore the original layer's size and offsets
            pdb.gimp_layer_resize(layers[layerIndex], lW, lH, -lOffX, -lOffY)


            # This floating layer will default to the center of the new image so we first shift to the top left
            # corner (0, 0) and and then shift to correct grid position based on current row and column index
            xOffset = (-newImgWidth/2) + (image.width/2) + (x * image.width)
            yOffset = (-newImgHeight/2) + (image.height/2) + (y * image.height)

            # GIMP will only copy non-transparent pixels, so if our image contains transparency
            # the new floating layer may be smaller than we want which will cause animation issues.
            # To resolve this we adjust our position by the difference in layer size to ensure everything aligns
            xOffset += (image.width - floatingLayer.width) / 2
            yOffset += (image.height - floatingLayer.height) / 2

            # Move the floating layer into the correct position
            pdb.gimp_layer_translate(floatingLayer, xOffset, yOffset)

            # Move to the next layer, unless we're all done in which case exit!
            layerIndex = (layerIndex - 1)
            if layerIndex < 0:
                break;

    # Merge the last floating layer into our final 'Spritesheet' layer
    pdb.gimp_image_merge_visible_layers(newImage, 0)

    # Create and show a new image window for our spritesheet
    gimp.Display(newImage)
    gimp.displays_flush()

# Register the plugin with Gimp so it appears in the filters menu
register(
    "python_fu_create_spritesheet",
    "Creates a spritesheet (in a new image) from the layers of the current image.",
    "Creates a spritesheet (in a new image) from the layers of the current image.",
    "Author: Karn Bianco. Contributors: Eneko Castresana",
    "Author: Karn Bianco. Contributors: Eneko Castresana",
    "2018",
    "Create Spritesheet",
    "*",
    [
        (PF_IMAGE, 'image', 'Input image:', None),
        (PF_BOOL, "singleRow", "Output to a single row?", FALSE),
        (PF_INT, "widthCells", "Width cells (0 for auto)", 0),
        (PF_INT, "heightCells", "Height cells (0 for auto)", 0)
    ],
    [],
    create_spritesheet, menu="<Image>/Filters/Animation/")

main()
