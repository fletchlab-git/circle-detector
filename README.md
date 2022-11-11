# circle-detector
A CLI script to detect circles in images and quantify edge transitions. All the circle detection parameters are tuneable,
with example values given in the help docstring sufficient for detecting 45um beads. However, sky's the limit! By 
increasing minR and maxR, you can detect large circles, by adjusting p1 you can detect better in low/high contrast images,
and if you're interested in the profile of the edge of your circles, the f parameter has got you covered.

## Usage
```buildoutcfg
usage: detect.py [-h]  -i IMAGE -p1 HOUGH PARAMETER 1 -p2 HOUGH PARAMETER 2 -minR MINIMUM RADIUS -maxR MAXIMUM RADIUS
                        -f FUZZY REGION

arguments:
  -h, --help            help message
  -i IMAGE, --input IMAGE
                        Path to the image
  -p1 HOUGH PARAMETER 1, --param1 HOUGH PARAMETER 1
                        Threshold for edge detection. If not sure, start with 200 (sufficient for detecting 45 um beads)
                        More info is available on the openCV documentation.
  -p2 HOUGH PARAMETER 2, --param2 HOUGH PARAMETER 2
                        Accumulator threshold for the circle centers. If not sure, start with 15 (sufficient for 
                        detecting 45 um beads). More info is available on the openCV documentation.
  -minR MINIMUM RADIUS, --minRadius MINIMUM RADIUS
                        Minimum radius (in pixels) for detected circles. Cirlces detected outside the range of (minR, maxR)
                        will be discarded. For 45um beads imaged at 10X (cornerscope cam), 25 pixels is sufficient.
  -maxR MAXIMUM RADIUS, --maxRadius MAXIMUM RADIUS
                        Maximum radius (in pixels) for detected circles. Cirlces detected outside the range of (minR, maxR)
                        will be discarded. For 45um beads imaged at 10X (cornerscope cam), 35 pixels is sufficient.
  -f FUZZY REGION, -- fuzzy FUZZY REGION
                        Length in pixels of precipitate region. An estimate is fine; naturally, this parameter is 
                        magnification dependent. For 45 um beads imaged on a 10X camera assayed at a 2:3 dilution, 16 
                        is a sufficient value.
```
