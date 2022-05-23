
# iworkout pose classification and estimation

iworkout is a data project for fitness beginners.
This github repo is mainly to show our pose classification and angle algorithm model.

# database

iworkout includes 5 basic workout poses: squat,deadlift,bench press,push up,hip bridge

resource(1):https://saketshirsath.github.io/cv.github.io/
resource(2):https://drive.google.com/drive/folders/1X9fq3w2gB88vJGCKM7bhG3C4u24v3pCL?usp=sharing

scraper tool:https://github.com/ohyicong/Google-Image-Scraper

# pose classfication

-Step 1: From image to csv

Mediapipe has its own pose classification solution which can run in a Jupyter Notebook or Google Colab. The main logic is to bootstrap every image, get its 33 landmarks and save into a csv, which can be used for ML model training.

Please Check notebooks/Pose_classification_(basic).ipynb
Image for landmarks: pose_tracking_full_body_landmarks.png

-Step 2: Build up ML model

Combine the power of Mediapipe,OpenCV and Scikit-Learn. A simple RandomForest Classifier can output high accuracy of prediction.

Please Check notebooks/Body_pose_predict.ipynb , iworkout/model.py

# pose estimation

-Step 1: poseDetector class

Prepare angle functions to do some normalization. Due to the reason that Mediapipe is still sensitive to camera angles, we need to preprocess our pose angles first to guarantee that all numbers are within the range of 0-180.

Please Check iworkout/poseDetector.py

-Step 2: layers of pose estimation

Balance is the breakpoint.

With the help of a professional fitness coach, our algorithm focuses on comparing angles of both sides to check the whole body balance. Same for each key component to check the balance of shoulders,hips,knees and etc so that we can output corresponding tips for users to workout properly.

Please Check iworkout/angle_English.py, iworkout/angle_chinese.py
