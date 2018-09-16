import numpy as np
import cv2

numImgs = 10 # Number of pictures to take
imgs = [] # The pictures
hues = [] # Hues of the pictures
saturations = [] # Saturation of the pictures
values = [] # Vals of the pictures
lowerBound = 30 # To replace pixel if dimer than this val
upperBound = 220 # To replace pixel if brighter than this val

def main():
  takePictures()
  replacePixels()
  waitToEnd()

# Connects to webcam and takes pictures
# Keep the webcam VERY still
def takePictures():
  cap = cv2.VideoCapture(0)
  # Read some dummy frames to allow time for startup
  for i in range(0,10):
    cap.read()

  for i in range(0,numImgs):
    ret, frame = cap.read()
    if ret:
      imgs.append(frame)
      H, S, V = cv2.split(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))
      hues.append(H)
      values.append(V)
      saturations.append(S)
    else:
      raise Exception('Problem reading from webcam')

# Replaces pixels that do not fit bounds
def replacePixels():
  img_hue = hues[0]
  img_sats = saturations[0]
  img_val = values[0]
  for i in range(0, len(img_val)):
    for j in range(0, len(img_val[0])):
      if img_val[i][j] < lowerBound:
        # replace a pixel
        for x in range(1, len(values)):
          currHue = hues[x]
          currSats = saturations[x]
          currVal = values[x]
          if currVal[i][j] >= lowerBound and currVal[i][j] < upperBound:
            img_hue[i][j] = currHue[i][j]
            img_sats[i][j] = currSats[i][j]
            img_val[i][j] = currVal[i][j]
            break
      elif img_val[i][j] > upperBound:
        # replace a pixel
        for x in range(1, len(values)):
          currHue = hues[x]
          currSats = saturations[x]
          currVal = values[x]
          if currVal[i][j] < upperBound and currVal[i][j] >= lowerBound:
            img_hue[i][j] = currHue[i][j]
            img_sats[i][j] = currSats[i][j]
            img_val[i][j] = currVal[i][j]
            break

  finalHsv = cv2.merge((img_hue, img_sats, img_val))
  finalImg = cv2.cvtColor(finalHsv, cv2.COLOR_HSV2BGR)
  cv2.imshow('Final_Image',finalImg)

# Waits for q to be pressed (on mac)
def waitToEnd():
  print "Press 'q' to quit"
  while(True):
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break  

main()