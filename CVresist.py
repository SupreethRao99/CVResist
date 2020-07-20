import cv2 as cv

#  establishing the colour ranges to detect the colour on the resistor.
#  these colour values vary depending on the camera settings, white balance and lighting.
#  Vary these parameters to suit your use-case
#  Colours are thresholded in the HSV colour space. more can be found at (https://en.wikipedia.org/wiki/HSL_and_HSV)
Colour_Range = [
    [(0, 0, 0), (255, 255, 20), "BLACK", 0, (0, 0, 0)],
    [(0, 90, 10), (15, 250, 100), "BROWN", 1, (0, 51, 102)],
    [(0, 30, 80), (10, 255, 200), "RED", 2, (0, 0, 255)],
    [(5, 150, 150), (15, 235, 250), "ORANGE", 3, (0, 128, 255)],  # ok
    [(50, 100, 100), (70, 255, 255), "YELLOW", 4, (0, 255, 255)],
    [(45, 100, 50), (75, 255, 255), "GREEN", 5, (0, 255, 0)],  # ok
    [(100, 150, 0), (140, 255, 255), "BLUE", 6, (255, 0, 0)],  # ok
    [(120, 40, 100), (140, 250, 220), "VIOLET", 7, (255, 0, 127)],
    [(0, 0, 50), (179, 50, 80), "GRAY", 8, (128, 128, 128)],
    [(0, 0, 90), (179, 15, 250), "WHITE", 9, (255, 255, 255)],
]

Red_top_low = (160, 30, 80)
Red_top_high = (179, 255, 200)

# setting up other basic necessities such as font and minimum area for a valid contour #
min_area = 0  # this parameter is determined after testing on various images
FONT = cv.FONT_HERSHEY_SIMPLEX


# method to find bands of the resistor
def findBands(img):
    img1 = cv.bilateralFilter(img, 40, 90, 90)  # image is bilaterally filtered to remove noise
    img_gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)  # image then converted to greyscale for thresholding
    img_hsv = cv.cvtColor(img1, cv.COLOR_BGR2HSV)  # image is converted to HSV colourspace for colour selection
    thresh = cv.adaptiveThreshold(img_gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 79,
                                  2)  # adaptive threshold is used to filter out the background
    thresh = cv.bitwise_not(thresh)

    bandpos = []

    for clr in Colour_Range:  # check with the pre- defined colour spaces
        mask = cv.inRange(img_hsv, clr[0], clr[1])
        if clr[2] == 'RED':  # creates two masks for the colour red a it has two colour bounds
            red_mask = cv.inRange(img_hsv, Red_top_low, Red_top_high)
            mask = cv.bitwise_or(red_mask, mask, mask)
        mask = cv.bitwise_and(mask, thresh, mask=mask)
        contours, hierarchy = cv.findContours(mask, cv.RETR_TREE,
                                              cv.CHAIN_APPROX_SIMPLE)

        for i in range(len(contours) - 1, -1, -1):
            if validContours(contours[i]):
                lmp = tuple(
                    contours[i][contours[i][:, :, 0].argmin()][0])  # finds the left most point of each valid contour
                bandpos += [lmp + tuple(clr[2:])]
            else:
                contours.pop(i)
        cv.drawContours(img1, contours, -1, clr[-1], 3)  # draws contours on screen

    cv.imshow('Contour Display', img1)
    return sorted(bandpos,
                  key=lambda tup: tup[0])  # returns a list of valid contours sorted by least value of leftmost point


# method to check the validity of the contours
def validContours(cont):
    if cv.contourArea(cont) < min_area:  # filters out all the tiny contours
        return False
    else:
        x, y, w, h = cv.boundingRect(cont)
        if float(w) / h > 0.40:
            return False
    return True


def displayResults(sortedbands):
    strvalue = ""
    if len(sortedbands) in [3, 4, 5]:
        for band in sortedbands[:-1]:
            strvalue += str(band[3])  # calculates the value of resistance
        intvalue = int(strvalue)
        intvalue *= 10 ** sortedbands[-1][3]  # applies the correct multiplier and stores the final resistance value
        print("The Resistance is ", intvalue, "ohms")
    return


# main method, here we accept the image.
if __name__ == '__main__':
    image = cv.imread('testresistor.jpg')
    sortedbands = findBands(image)
    displayResults(sortedbands)
    cv.waitKey(0)
    cv.destroyAllWindows()
