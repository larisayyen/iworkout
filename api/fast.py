
from fastapi import FastAPI, UploadFile, File
from fastapi.datastructures import UploadFile
from fastapi.middleware.cors import CORSMiddleware
import mediapipe
import numpy as np
import pandas as pd
import cv2
import uvicorn
import pickle
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose


PATH_TO_LOCAL_MODEL = 'pipeline3.pkl'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.post("/predict_pose")
async def make_predict(img:UploadFile=File(...)):

    contents = await img.read()
    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    imgRGB = cv2.cvtColor(cv2_img,cv2.COLOR_BGR2RGB)
    with mp_pose.Pose() as pose_tracker:
        result = pose_tracker.process(image=imgRGB)
        pose_landmarks = result.pose_landmarks

    if pose_landmarks is not None:
        mp_drawing.draw_landmarks(
            image=imgRGB,
            landmark_list=pose_landmarks,
            connections=mp_pose.POSE_CONNECTIONS)
        pose_landmarks = [[lmk.x, lmk.y, lmk.z] for lmk in pose_landmarks.landmark]
        frame_height, frame_width = imgRGB.shape[:2]
        pose_landmarks *= np.array([frame_width, frame_height, frame_width])
        pose_landmarks = np.around(pose_landmarks, 5).flatten().tolist()

    x_pred = pd.DataFrame(pose_landmarks)
    x_pred = x_pred.T.to_numpy()
    print(x_pred[0].shape)

    model = pickle.load(open(PATH_TO_LOCAL_MODEL,"rb"))
    y_pred = model.predict(x_pred[0].reshape(1,99))
    #print(y_pred)

    return {'workout pose':y_pred[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
