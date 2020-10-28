#!/usr/bin/env python3
# Inspiration http://scottbezek.blogspot.com/2016/04/scripting-kicad-pcbnew-exports.html
import pcbnew
from PIL import Image, ImageChops
import io
# import BytesIO
import cairosvg
import sys


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

# Load board and initialize plot controller
board = pcbnew.LoadBoard(sys.argv[1])
pc = pcbnew.PLOT_CONTROLLER(board)
po = pc.GetPlotOptions()
po.SetPlotFrameRef(False)

# Set current layer
pc.SetLayer(pcbnew.F_Cu)

# Plot single layer to file
#pc.OpenPlotfile("front_copper", pcbnew.PLOT_FORMAT_SVG, "front_copper")
#print("Plotting to " + pc.GetPlotFileName())
#pc.PlotLayer()
#pc.ClosePlot()

#F.Mask
pc.SetLayer(pcbnew.F_Mask)
pc.OpenPlotfile("front_mask", pcbnew.PLOT_FORMAT_SVG, "front_mask")
print("Plotting to " + pc.GetPlotFileName())
name_mask = pc.GetPlotFileName()
pc.PlotLayer()
pc.ClosePlot()

#F.SilkS
pc.SetLayer(pcbnew.F_SilkS)
pc.OpenPlotfile("front_silk", pcbnew.PLOT_FORMAT_SVG, "front_silk")
print("Plotting to " + pc.GetPlotFileName())
name_silk = pc.GetPlotFileName()
pc.PlotLayer()
pc.ClosePlot()

out_silk = io.BytesIO()
cairosvg.svg2png(url=name_silk, write_to=out_silk, scale=2.0)
image_silk = Image.open(out_silk)
out_mask = io.BytesIO()
cairosvg.svg2png(url=name_mask, write_to=out_mask, scale=2.0)
image_mask = Image.open(out_mask)

#image_silk.show()

pixels_silk = image_silk.load() # create the pixel map
pixels_mask = image_mask.load()

# https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#PIL.Image.Image.paste
#image_silk = image_silk.convert("RGB")
for i in range(image_silk.size[0]): # for every pixel:
    for j in range(image_silk.size[1]):
       if pixels_silk[i,j] != (0, 0, 0, 0) and pixels_mask[i,j] != (0, 0, 0, 0):

       	 pixels_silk[i,j] = (255, 0 ,0)


image_silk = trim(image_silk)
#image_silk.save("test.png",optimize=0)
image_silk.show()
