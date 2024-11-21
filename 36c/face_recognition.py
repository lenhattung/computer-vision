import cv2
import numpy as np
import pickle
import os

class FaceRecognition:
    def __init__(self, path='./'):
        # Load models
        self.faceDetectionModel = os.path.join(path, 'models/res10_300x300_ssd_iter_140000_fp16.caffemodel')
        self.faceDetectionProto = os.path.join(path, 'models/deploy.prototxt.txt')
        self.faceDescriptor = os.path.join(path, 'models/openface.nn4.small2.v1.t7')
        self.face_recognition_model = pickle.load(open(os.path.join(path, 'ml_face_person_identity.pkl'), 'rb'))

        # Khởi tạo models
        self.detectorModel = cv2.dnn.readNetFromCaffe(self.faceDetectionProto, self.faceDetectionModel)
        self.descriptorModel = cv2.dnn.readNetFromTorch(self.faceDescriptor)
        
    def pipeline_model(self, frame):
        image = frame.copy()
        h, w = frame.shape[:2]

        img_blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123), swapRB=False, crop=False)
        self.detectorModel.setInput(img_blob)
        detections = self.detectorModel.forward()

        machinelearning_results = {
            'face_detect_score': [],
            'face_name': [],
            'face_name_score': [],
            'count': [],
            'bbox': []
        }

        count = 1
        for i, confidence in enumerate(detections[0, 0, :, 2]):
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                startx, starty, endx, endy = box.astype(int)

                machinelearning_results['bbox'].append((startx, starty, endx, endy))

                face_roi = frame[starty:endy, startx:endx]
                face_blob = cv2.dnn.blobFromImage(face_roi, 1 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=True)
                self.descriptorModel.setInput(face_blob)
                vectors = self.descriptorModel.forward()

                face_name = self.face_recognition_model.predict(vectors)[0]
                individual_predictions = [clf.predict(vectors)[0] for clf in self.face_recognition_model.estimators_]
                agreement_count = sum([1 for pred in individual_predictions if pred == face_name])
                face_score = agreement_count / len(self.face_recognition_model.estimators_)

                machinelearning_results['count'].append(count)
                machinelearning_results['face_detect_score'].append(confidence)
                machinelearning_results['face_name'].append(face_name)
                machinelearning_results['face_name_score'].append(face_score)
                count += 1

        return machinelearning_results