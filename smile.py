# Detect how much a person smiles.
# Written by iCrazyBlaze - Updated 13/08/2018

########################### CONFIG ############################
# Print list items to console
printlist = True

# Amount of items to put in list (amount of data to collect)
gatheramount = 50
###############################################################
print("Loading...")

# For OpenCV and Face Tracking
import cv2
import threading
import itertools
import operator
# For saying insults
import insults
import random
# Choose random window title
windowtitle = random.choice(insults.titles)
# Setup TTS (Windows only)
import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")


# Function to find most common list item

def most_common(L):
  SL = sorted((x, i) for i, x in enumerate(L))
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]


def be_mean():
    # Read random insult from list in insults.py
    saythis = random.choice(insults.insultslist)
    print("")
    print(saythis)
    print("")
    # Destroy window and stop capturing
    cap.release()
    cv2.destroyAllWindows()
    # Say with TTS (Windows only)
    speak.Speak(saythis)


# Cascade files go in same directory
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

cap = cv2.VideoCapture(0)

# While true the loop will be running
running = True

# Create empty list for smiling true/false
list = []


while running == True:

    # OpenCV Setup
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Find and track faces
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        print("Found", len(faces), "faces in image")

        # Find and track smiles
        is_smiling = False
        smiles = smile_cascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.16,
            minNeighbors=35,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x,y,w,h) in smiles:
            print("Found", len(smiles), "smiles in image")
            cv2.rectangle(roi_color, (x, y), (x+w, y+h), (0, 255, 0), 2)

        for (x,y,w,h) in smiles:
            cv2.putText(img,'Smile Detected',(x,y-7), 3, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
            is_smiling = True

        # Keep gathering data until the amount to gather is no longer bigger
        if len(list) < gatheramount:
            list.append(is_smiling)

            if printlist == True:
                print(list)
        else:
            if most_common(list) == True:
                print("")
                print("You smiled a lot.")
                print("")
                be_mean()
            else:
                print("")
                print("You don't seem very happy...")
                print("")

            # Quit loop
            running = False


        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex,ey,ew,eh) in eyes:
        #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)
        #     print("Found", len(eyes), "eyes")


    # Create window with title from insults.py
    cv2.imshow(windowtitle,img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
