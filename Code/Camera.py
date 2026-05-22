import cv2
import tensorflow as tf
import numpy as np
import threading
import time
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from queue import Queue
import csv
from datetime import datetime
import os

# Load the Model
interpreter = tf.lite.Interpreter(model_path='MoveNet_Thunder.tflite')
interpreter.allocate_tensors()

EDGES = {
    (0, 1): 'm', (0, 2): 'c', (1, 3): 'm', (2, 4): 'c',
    (5, 7): 'm', (7, 9): 'm', (6, 8): 'c', (8, 10): 'c',
    (5, 6): 'y', (5, 11): 'm', (6, 12): 'c', (11, 12): 'y',
    (11, 13): 'm', (13, 15): 'm', (12, 14): 'c', (14, 16): 'c'
}

def preprocess_image(image):
    yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
    equalized = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    gamma = 1.2
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    gamma_corrected = cv2.LUT(equalized, table)
    return gamma_corrected

class CameraScreenUI:
    def __init__(self, root, exercise_name, target_reps=10):
        self.root = root
        self.exercise_name = exercise_name
        self.target_reps = target_reps
        self.root.title("Camera Screen")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#f0f0f0")
        
        self.session_data = {
            'start_time': datetime.now(),
            'reps': [],
            'current_rep_angles': [],
            'performance_scores': [],
            'data_saved': False
        }

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.menuBar = Menu(self.root)
        self.create_menu()

        self.titleLabel = Label(self.root, text="Camera for Exercise", font=("Arial", 24, "bold"), bg="#f0f0f0")
        self.titleLabel.pack(pady=20)
        Label(self.root, text=f"{self.exercise_name} | Target: {self.target_reps} reps", 
              font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=10)

        self.home_img, self.back_img = self.load_nav_images()
        self.create_nav_buttons()

        canvas_width = 1280
        canvas_height = 720
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - canvas_width) // 2 
        y_position = ((screen_height - canvas_height) // 2) + 30
        self.cameraFeed = Canvas(self.root, width=canvas_width, height=canvas_height)
        self.cameraFeed.place(x=x_position, y=y_position)

        self.check_camera()

        self.photo = None
        self.pose = None
        self.prev_angle = None
        self.current_angle = None
        self.smoothing_factor = 0.1
        self.arm_state = "resting"
        self.curlCount = 0
        self.curl_status = "Please Move Arm into Frame"
        self.start_time = time.time()
        self.end_time = None
        self.timer_running = True
        self.completion_shown = False
        
        self.confidence_threshold = 0.3
        self.keypoint_history = {
            'right_shoulder': [],
            'right_elbow': [],
            'right_wrist': []
        }
        self.smoothing_window = 5
        
        self.pose_queue = Queue(maxsize=1)
        
        self.update_frame()
        
        # Setup CSV file
        self.data_file = 'exercise_data.csv'
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'exercise_name', 'target_reps',
                    'completed_reps', 'duration', 'score',
                    'avg_peak_angle', 'avg_rest_angle', 'form_consistency'
                ])
                
    
    def calculate_performance_score(self):
        if not self.session_data['reps']:
            return 0
        
        # Calculate form consistency (lower stddev = better)
        peak_angles = [rep['peak_angle'] for rep in self.session_data['reps']]
        rest_angles = [rep['rest_angle'] for rep in self.session_data['reps']]
        
        peak_std = np.std(peak_angles) if len(peak_angles) > 1 else 0
        rest_std = np.std(rest_angles) if len(rest_angles) > 1 else 0
        
        # Base score on completed reps and form consistency
        completion_ratio = self.curlCount / self.target_reps
        form_score = 1 - (peak_std + rest_std)/100  # Normalise the form score
        
        return round((completion_ratio * 0.7 + form_score * 0.3) * 100, 1)
    
    def save_session_data(self):
        if self.curlCount == 0 or self.session_data['data_saved']:
            return  # Don't save if no reps attempted

        duration = (datetime.now() - self.session_data['start_time']).total_seconds()
        score = self.calculate_performance_score()
        
        peak_angles = [rep['peak_angle'] for rep in self.session_data['reps']]
        rest_angles = [rep['rest_angle'] for rep in self.session_data['reps']]
        
        with open(self.data_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.session_data['start_time'].isoformat(),
                self.exercise_name,
                self.target_reps,
                self.curlCount,
                duration,
                score,
                np.mean(peak_angles) if peak_angles else 0,
                np.mean(rest_angles) if rest_angles else 0,
                1 - (np.std(peak_angles + rest_angles)/100) if peak_angles else 0
            ])
            # Mark data as saved to prevent duplicates
        self.session_data['data_saved'] = True

    def create_menu(self):
        fileMenu = Menu(self.menuBar, tearoff=0)
        fileMenu.add_command(label="Request Help", command=self.request_help)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.exit_program)
        self.menuBar.add_cascade(label="File", menu=fileMenu)
        self.root.config(menu=self.menuBar)

    def request_help(self):
        messagebox.showinfo("Help", "For assistance, please contact x8w11@students.keele.ac.com")

    def exit_program(self):
        self.save_session_data()
        self.root.quit()

    def go_to_home_screen(self):
        self.save_session_data()
        from HomeScreen import HomeScreenUI
        for widget in self.root.winfo_children():
            widget.destroy()
        HomeScreenUI(self.root)

    def go_to_choose_exercises_screen(self):
        self.save_session_data()
        from ChooseExercises import ChooseExercisesUI
        for widget in self.root.winfo_children():
            widget.destroy()
        ChooseExercisesUI(self.root)

    def check_camera(self):
        if not self.cap.isOpened():
            camera_label = Label(self.root, text="No camera found", font=("Arial", 18, "bold"),
                                bg="#f0f0f0", fg="red")
            camera_label.pack(pady=100)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            pose_thread = threading.Thread(target=self.run_pose_model, args=(frame.copy(),))
            pose_thread.start()
            pose_thread.join()

            if self.pose:
                #right_shoulder = self.pose['right_shoulder']
                #right_elbow = self.pose['right_elbow']
                #right_wrist = self.pose['right_wrist']

                right_shoulder = self.right_shoulder  # Smoothed value
                right_elbow = self.right_elbow        # Smoothed value
                right_wrist = self.right_wrist        # Smoothed value
                right_arm_edges = {edge: EDGES[edge] for edge in [(6, 8), (8, 10)]}
                
                if self.timer_running:
                    current_time = time.time()
                    elapsed_time = current_time - self.start_time
                else:
                    elapsed_time = self.end_time - self.start_time if self.end_time is not None else 0

                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                timer_text = f"Time: {minutes:02d}:{seconds:02d}"
                cv2.putText(frame, timer_text, (frame.shape[1] - 300, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                
                if self.check_for_arm(right_shoulder, right_elbow, right_wrist, 0.4):
                    angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
                    smoothed_angle = self.smoothing_angle(angle)
                    self.current_angle = smoothed_angle
                    
                    # Record angle data for current rep
                    if self.arm_state in ['curling', 'peak', 'returning']:
                        self.session_data['current_rep_angles'].append(smoothed_angle)

                    current_state = self.arm_state
                    
                    if self.timer_running:
                        if current_state == "resting":
                            if smoothed_angle < 135:
                                self.arm_state = "curling"
                                self.curl_status = "Arm is curling."
                        elif current_state == "curling":
                            if smoothed_angle <= 60:
                                self.arm_state = "peak"
                                self.curl_status = "Peak contraction!"
                        elif current_state == "peak":
                            if smoothed_angle > 60:
                                self.arm_state = "returning"
                                self.curl_status = "Returning to start..."
                        elif current_state == "returning":
                            if smoothed_angle >= 135:
                                self.arm_state = "resting"
                                self.curlCount += 1
                                self.curl_status = f"Rep completed! Count: {self.curlCount}"
                                
                                # Store rep data
                                if self.session_data['current_rep_angles']:
                                    self.session_data['reps'].append({
                                        'peak_angle': min(self.session_data['current_rep_angles']),
                                        'rest_angle': max(self.session_data['current_rep_angles']),
                                        'duration': time.time() - self.start_time
                                    })
                                    self.session_data['current_rep_angles'] = []
                                
                                if self.curlCount == self.target_reps and self.timer_running:
                                    self.end_time = time.time()
                                    self.timer_running = False
                                    self.curl_status = f"Exercise Complete! {self.target_reps} reps achieved!"
                                    if not self.completion_shown:
                                        self.show_completion_popup()
                                        self.completion_shown = True
                            else:
                                self.curl_status = "Returning to start..."

                    if self.timer_running and current_state == self.arm_state:
                        if self.arm_state == "resting" and smoothed_angle >= 135:
                            self.curl_status = "Ready - start curling!"
                        elif self.arm_state == "curling" and 60 < smoothed_angle < 135:
                            self.curl_status = "Keep curling..."
                        elif self.arm_state == "peak" and smoothed_angle <= 60:
                            self.curl_status = "Hold peak contraction!"
                        elif self.arm_state == "returning" and 60 < smoothed_angle < 135:
                            self.curl_status = "Return to start position"
                            
                    cv2.putText(frame, self.curl_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Count: {self.curlCount}/{self.target_reps}", (50, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    self.draw_connections(frame, self.pose['keypoints_with_scores'], right_arm_edges, 0.4)
                    self.draw_keypoints(frame, [right_shoulder, right_elbow, right_wrist], 0.3)
                else:
                    self.current_angle = None
                    self.curl_status = "Please position arm in frame"
                    cv2.putText(frame, self.curl_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = Image.fromarray(frame_rgb)
            self.photo = ImageTk.PhotoImage(frame_image)
            self.cameraFeed.create_image(0, 0, image=self.photo, anchor=NW)
            self.cameraFeed.update()

        self.root.after(10, self.update_frame)

    def run_pose_model(self, frame):
        preprocessed_frame = preprocess_image(frame)
        img = cv2.resize(preprocessed_frame, (256, 256))
        img = np.expand_dims(img, axis=0)
        input_image = tf.cast(img, dtype=tf.float32)

        interpreter.set_tensor(interpreter.get_input_details()[0]['index'], input_image)
        interpreter.invoke()
        keypoints_with_scores = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])

        self.pose = {
            'right_shoulder': keypoints_with_scores[0][0][6],
            'right_elbow': keypoints_with_scores[0][0][8],
            'right_wrist': keypoints_with_scores[0][0][10],
            'keypoints_with_scores': keypoints_with_scores
        }
        
        self.keypoint_history['right_shoulder'].append(keypoints_with_scores[0][0][6])
        self.keypoint_history['right_elbow'].append(keypoints_with_scores[0][0][8])
        self.keypoint_history['right_wrist'].append(keypoints_with_scores[0][0][10])
        self.smooth_keypoints()

    def draw_connections(self, frame, keypoints, edges, confidence_threshold):
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))
        for edge, color in edges.items():
            p1, p2 = edge
            y1, x1, c1 = shaped[p1]
            y2, x2, c2 = shaped[p2]
            if (c1 > confidence_threshold) and (c2 > confidence_threshold):
                if self.current_angle is not None:
                    min_angle = 60
                    max_angle = 135
                    clamped_angle = max(min(self.current_angle, max_angle), min_angle)
                    ratio = (clamped_angle - min_angle) / (max_angle - min_angle)
                    red = int(255 * ratio)
                    green = int(255 * (1 - ratio))
                    line_color = (0, green, red)
                else:
                    line_color = (0, 0, 255)
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), line_color, 2)

    def draw_keypoints(self, frame, keypoints, confidence_threshold):
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))
        for kp in shaped:
            ky, kx, kp_conf = kp
            if kp_conf > confidence_threshold:
                cv2.circle(frame, (int(kx), int(ky)), 4, (0, 255, 0), -1)

    def calculate_angle(self, a, b, c):
        ab = a[:2] - b[:2]
        bc = c[:2] - b[:2]
        ab_norm = ab / np.linalg.norm(ab)
        bc_norm = bc / np.linalg.norm(bc)
        cos_angle = np.dot(ab_norm, bc_norm)
        return np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

    def check_for_arm(self, shoulder, elbow, wrist, confidence_threshold):
        return all(kp[2] > confidence_threshold for kp in [shoulder, elbow, wrist])

    def smoothing_angle(self, angle):
        if self.prev_angle is None:
            self.prev_angle = angle
            return angle
        smoothed_angle = self.smoothing_factor * angle + (1 - self.smoothing_factor) * self.prev_angle
        self.prev_angle = smoothed_angle
        return smoothed_angle

    def smooth_keypoints(self):
        for joint in self.keypoint_history:
            if len(self.keypoint_history[joint]) > self.smoothing_window:
                self.keypoint_history[joint].pop(0)
            if self.keypoint_history[joint]:
                smoothed = np.mean(self.keypoint_history[joint], axis=0)
                setattr(self, joint, smoothed)

    def show_completion_popup(self):
        self.save_session_data()  # Save data when exercise is completed
        elapsed_time = self.end_time - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        popup = Toplevel(self.root)
        popup.title("Exercise Complete!")
        popup.geometry("450x220")
        popup.configure(bg="#f0f0f0")
        
        # Center the popup
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 450) // 2
        y = (screen_height - 220) // 2
        popup.geometry(f"+{x}+{y}")
        
        Label(popup, text="Congratulations!", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)
        Label(popup, text=f"You finished {self.target_reps} {self.exercise_name}\nin {minutes:02d}:{seconds:02d}", 
            font=("Arial", 14), bg="#f0f0f0").pack(pady=5)
        
        button_frame = Frame(popup, bg="#f0f0f0")
        button_frame.pack(pady=15)
        
        Button(button_frame, text="Finish", command=lambda: [popup.destroy(), self.go_to_home_screen()], 
            font=("Arial", 12), bg="#007BFF", fg="white", width=15).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Choose Another Exercise", 
            command=lambda: [popup.destroy(), self.go_to_choose_exercises_screen()],
            font=("Arial", 12), bg="#28A745", fg="white", width=20).pack(side=LEFT, padx=10)
        
        popup.grab_set()
        
    def load_nav_images(self):
        try:
            home_img = ImageTk.PhotoImage(Image.open("assets/home_icon.png").resize((64, 64)))
            back_img = ImageTk.PhotoImage(Image.open("assets/back_icon.png").resize((64, 64)))
            return home_img, back_img
        except Exception as e:
            print(f"Image load error: {e}")
            return None, None

    def create_nav_buttons(self):
        """Create image-based navigation buttons"""
        nav_frame = Frame(self.root, bg="#f0f0f0")
        nav_frame.place(x=10, y=10, width=140, height=74)

        # Home Button
        self.home_btn = Button(
            nav_frame,
            image=self.home_img,
            command=self.go_to_home_screen,
            relief=FLAT,
            bg="#f0f0f0",
            activebackground="#e0e0e0"
        )
        if not self.home_img:
            self.home_btn.config(text="🏠", font=("Arial", 24))
        self.home_btn.pack(side=LEFT, padx=5)

        # Back Button
        self.back_btn = Button(
            nav_frame,
            image=self.back_img,
            command=self.go_to_choose_exercises_screen,
            relief=FLAT,
            bg="#f0f0f0",
            activebackground="#e0e0e0"
        )
        if not self.back_img:
            self.back_btn.config(text="←", font=("Arial", 24))
        self.back_btn.pack(side=LEFT, padx=5)

        # Button press animations
        for btn in [self.home_btn, self.back_btn]:
            btn.bind("<ButtonPress-1>", lambda e: e.widget.config(relief=SUNKEN))
            btn.bind("<ButtonRelease-1>", lambda e: e.widget.config(relief=FLAT))

if __name__ == "__main__":
    root = Tk()
    exercise_name = "Right Arm Curls"
    target_reps = 10
    app = CameraScreenUI(root, exercise_name, target_reps)
    root.mainloop()