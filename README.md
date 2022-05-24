
# iworkout pose classification and estimation

iworkout is a data project for fitness beginners.
This github repo is mainly to show our pose classification and angle algorithm model.

# Database

iworkout includes 5 basic workout poses: squat,deadlift,bench press,push up,hip bridge.

resource(1): https://saketshirsath.github.io/cv.github.io/

resource(2): https://drive.google.com/drive/folders/1X9fq3w2gB88vJGCKM7bhG3C4u24v3pCL?usp=sharing

web scraping tool: https://github.com/ohyicong/Google-Image-Scraper

# Pose Classfication

-> Step1: From image to csv

Mediapipe has its own pose classification solution. The main logic is to bootstrap every image, get its 33 landmarks and save into a csv, which can be used for ML model training.

Question: How to get landmarks?

```bash
#import mediapipe moduls
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose

#initialize pose tracker
with mp_pose.Pose(upper_body_only=False) as pose_tracker:
  result = pose_tracker.process(image=input_frame)
  pose_landmarks = result.pose_landmarks

#save pose landmarks
if pose_landmarks is not None:
  assert len(pose_landmarks.landmark) == 33, 'Unexpected number of predicted pose landmarks: {}'.format(len(pose_landmarks.landmark))
  pose_landmarks = [[lmk.x, lmk.y, lmk.z] for lmk in pose_landmarks.landmark]
```

For more details,please check notebooks/Pose_classification_(basic).ipynb


-> Step 2: Build up ML model

Combine the power of Mediapipe,OpenCV and Scikit-Learn. A simple RandomForest Classifier can output high accuracy of prediction.

```bash
def run(self):
    model = make_pipeline(StandardScaler(),RandomForestClassifier())
    return model
```

For more details,please check iworkout/model.py

# pose estimation

-> Step 1: poseDetector class

Prepare basic functions to do some angle normalization. Due to the fact that Mediapipe is still sensitive to camera angles, we need to preprocess our pose angles first to guarantee that all numbers are within the range of 0-180.

```bash
#calculate angles
tan_1 = math.atan2(y3-y2,x3-x2)
tan_2 = math.atan2(y1-y2,x1-x2)
if tan_1 - tan_2 < 0 :
    tan_ = abs(tan_1 - tan_2)
    angle = math.degrees(tan_)
elif tan_1 - tan_2 > 3.13 :
    tan_ = tan_1 - tan_2
    angle = 360 - math.degrees(tan_)
else:
    tan_ = tan_1 - tan_2
    angle = math.degrees(tan_)
```
```bash
#standard angles if angle > 180
def standardize(d):
    for k,v in d.items():
        if v > 180 :
            v_ = 360 -v
            d[k] = v_
        else:
            v = v
    return d

#output standardized angles
def check(d1,d2):
    if d1.values() == d2.values():
        return True
    else:
        return False
```

For more details,please check iworkout/poseDetector.py, iworkout/angle_English.py

-> Step 2: layers of pose estimation

Balance is the breakpoint.

With the help of a professional fitness coach, our algorithm focuses on comparing angles of both sides to check the whole body balance. Same for each key component to check the balance of shoulders,hips,knees and etc. so that we can output corresponding tips for users to workout properly.

For more details,please check iworkout/angle_English.py, iworkout/angle_chinese.py
