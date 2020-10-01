# CVResist
A python program that reads resistor values from images using OpenCV. 
Refrence: https://opencv.org/

## Working

### Image pre-processing
A bilateral filter is used to remove noise and other artefacts that may interfere in the detection of colour. A bilateral filter is used over a
simple gaussian filter as it preserves edge sharpness. The image is then thresholded using an Adaptive threshold to filter out the background and the body of the 
resistor. We then invert this threshold so that our region of interests are the coloured resistor bands. The blockSize and the constant is determined empirically.

### Determination of colour bands

A predifined list that consists of lower and upper colour bounds for every band is stored in the **BGR** format as well **H**ue**S**aturation**V**alue (HSV)
format along with a multiplier which is used in determining the order of magnitude for the resistor. This list is then iterated over and mask for each colour is 
created and then bitwise-ANDed with the thresholded image.All the contours are found for this new mask. The contours are then filtered to discard any contours whose
areas are lower than a preset value or to filter out those contours whos aspect ratios are not right. Doing this allows contours which are roughly rectangular and 
may pass as a colour band of a resistor.The left most point for all the valid contours are then found and stored into a list. This list is then sored by the lowest value of the position of the bands.
This correlates to position of the band on the resistor when read from left to right ( ie Tolerace band is on the right ).

### Displaying the result

The sorted list of the position of the bands are iterated over and each element is extracted and then multiplied with the correct multilpier to arrive at the correct
resistance value. This is then displayed on the console.

## Improvements

This program can be adapted to work on live video by using a neural network or a cascade classifier to detect a resistor in a video and then using this program to
read the resistance on the detected resistor.

## Limitations

Colour detection is heavily dependent on ambient lighting, camera settings etc and thus the program might not identify/misclassify colours the resistor, this can
be rectified by changing the thresholds of each colour. More can be read about this at (https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv)
