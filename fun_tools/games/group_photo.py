import cv2
import numpy as np
from ultralytics import YOLO
import mediapipe as mp
import random
import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from PIL import Image, ImageTk

class GroupPhotoAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Group Photo Analysis")
        self.root.geometry("500x600")
        self.image_path = None
        self.model = YOLO("yolov8m.pt")
        self.setup_gui()

    def setup_gui(self):
        """GUI 레이아웃 설정"""
        Label(self.root, text="이미지 선택", font=("Arial", 14)).pack(pady=10)
        Button(self.root, text="이미지 선택", command=self.select_image).pack()

        self.img_label = Label(self.root)
        self.img_label.pack(pady=10)

        Label(self.root, text="벌칙 입력", font=("Arial", 14)).pack(pady=10)
        self.mission_entry = Entry(self.root, width=30)
        self.mission_entry.pack(pady=5)

        Button(self.root, text="분석 시작", command=self.start_analysis).pack(pady=20)

    def select_image(self):
        """이미지 파일 선택"""
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if self.image_path:
            img = Image.open(self.image_path)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.img_label.config(image=img)
            self.img_label.image = img
            self.img_label.text = self.image_path

    def start_analysis(self):
        """분석 시작"""
        if not self.image_path:
            messagebox.showerror("Error", "이미지를 선택하세요.")
            return
        mission = self.mission_entry.get()
        if not mission:
            messagebox.showerror("Error", "벌칙을 입력하세요.")
            return
        self.analyze_group_photo(self.image_path, mission)

    def analyze_group_photo(self, image_path, mission, confidence_threshold=0.5):
        """YOLO로 사람 감지 후 Mediapipe로 분석"""
        image = cv2.imread(image_path)
        if image is None:
            messagebox.showerror("Error", "이미지를 불러올 수 없습니다.")
            return

        results = self.model(image)
        detections = results[0].boxes.data.cpu().numpy()

        people = [d for d in detections if int(d[5]) == 0 and d[4] >= confidence_threshold]
        all_features = []

        for idx, person in enumerate(people, start=1):
            x1, y1, x2, y2, _, _ = person
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            person_image = image[y1:y2, x1:x2]
            features = self.analyze_person(person_image, idx)
            all_features.extend(features)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"Person {idx}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if all_features:
            selected_feature = random.choice(all_features)
            result_text = f"{selected_feature} : {mission}"
            messagebox.showinfo("Result", result_text)
        else:
            result_text = "감지된 특징이 없습니다."
            messagebox.showinfo("Result", result_text)

        cv2.imshow("Group Photo Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def analyze_person(self, image_region, person_id):
        """개별 사람의 특징 분석"""
        features = []
        h, w, _ = image_region.shape

        # BGR 이미지를 RGB로 변환
        image_rgb = cv2.cvtColor(image_region, cv2.COLOR_BGR2RGB)

        # Mediapipe Hands 분석
        with mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
            hand_results = hands.process(image_rgb)
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
                    thumb_ip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_IP]
                    wrist = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]

                    # 엄지손가락 감지: TIP이 IP보다 위에 있는 경우
                    if thumb_tip.y < thumb_ip.y and thumb_tip.y < wrist.y:
                        features.append(f"Person {person_id}: 엄지손가락을 올린 사람")

                    # 손가락 V 포즈 감지
                    index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
                    middle_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
                    if index_tip.y < middle_tip.y:  # 손가락으로 V 포즈
                        features.append(f"Person {person_id}: 손가락으로 V 포즈를 한 사람")

        return features