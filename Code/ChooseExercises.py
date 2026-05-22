from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import threading
import time
import queue
from PIL import Image, ImageTk

class ChooseExercisesUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Choose Exercises")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#f0f0f0")
        self.loading_queue = queue.Queue()

        # Exercise configuration
        self.implemented_exercises = ["Right Arm Curls"]
        self.exercise_dates = {exercise: "N/A" for exercise in ["Right Arm Curls", "Squats", "Jumping Jacks"]}
        self.exercise_labels = {}

        # Load navigation images
        self.home_img, self.back_img = self.load_navigation_images()
        
        self.create_menu()
        self.create_widgets()

    def load_navigation_images(self):
        try:
            home_img = ImageTk.PhotoImage(Image.open("assets/home_icon.png").resize((64, 64)))
            back_img = ImageTk.PhotoImage(Image.open("assets/back_icon.png").resize((64, 64)))
            return home_img, back_img
        except Exception as e:
            print(f"Error loading images: {str(e)}")
            return None, None

    def create_menu(self):
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Request Help", command=self.request_help)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_program)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

    def create_widgets(self):
        Label(self.root, text="Select an Exercise", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

        # Navigation buttons frame
        nav_frame = Frame(self.root, bg="#f0f0f0")
        nav_frame.place(x=10, y=10)

        # Home Button with image
        self.home_btn = Button(nav_frame, image=self.home_img, command=self.go_to_home_screen,
                             borderwidth=0, bg="#f0f0f0", activebackground="#e0e0e0")
        self.home_btn.image = self.home_img
        self.home_btn.pack(side=LEFT, padx=5)

        # Back Button with image
        self.back_btn = Button(nav_frame, image=self.back_img, command=self.go_back,
                              borderwidth=0, bg="#f0f0f0", activebackground="#e0e0e0")
        self.back_btn.image = self.back_img
        self.back_btn.pack(side=LEFT, padx=5)

        # Fallback to text if images failed to load
        if not self.home_img:
            self.home_btn.config(text="🏠", font=("Arial", 24))
        if not self.back_img:
            self.back_btn.config(text="←", font=("Arial", 24))

        # Add button press animations
        for btn in [self.home_btn, self.back_btn]:
            btn.bind("<ButtonPress-1>", lambda e: e.widget.config(relief=SUNKEN))
            btn.bind("<ButtonRelease-1>", lambda e: e.widget.config(relief=FLAT))

        # Exercise buttons
        for exercise in self.exercise_dates:
            frame = Frame(self.root, bg="#f0f0f0")
            frame.pack(pady=10, padx=50, fill="x", expand=True)

            Button(frame, text=exercise, font=("Arial", 20, "bold"), width=15, height=2,
                   bg="#007BFF", fg="white", command=lambda e=exercise: self.select_exercise(e)
                   ).pack(side="left", padx=20, pady=5)

            label = Label(frame, text=f"{exercise} - {self.exercise_dates[exercise]}", 
                         font=("Arial", 18), bg="#f0f0f0")
            label.pack(side="right", padx=20)
            self.exercise_labels[exercise] = label

    def select_exercise(self, exercise_name):
        if exercise_name not in self.implemented_exercises:
            messagebox.showinfo("Coming Soon", 
                               f"{exercise_name} exercise is coming soon!\n\n"
                               "Currently only Right Arm Curls is available.")
            return
        self.show_rep_selection_dialog(exercise_name)

    def show_rep_selection_dialog(self, exercise_name):
        dialog = Toplevel(self.root)
        dialog.title("Select Target Reps")
        dialog.grab_set()
        dialog.geometry("300x150")
        dialog.configure(bg="#f0f0f0")

        Label(dialog, text=f"Target reps for {exercise_name}:",
              font=("Arial", 12), bg="#f0f0f0").pack(pady=10)

        rep_options = [5, 10, 15, 20, 25, 30]
        reps_var = StringVar(value=10)
        
        reps_dropdown = ttk.Combobox(dialog, 
                                   textvariable=reps_var,
                                   values=rep_options,
                                   state="readonly",
                                   font=("Arial", 12))
        reps_dropdown.pack(pady=5)

        button_frame = Frame(dialog, bg="#f0f0f0")
        button_frame.pack(pady=10)

        def set_reps():
            try:
                reps = int(reps_var.get())
                dialog.destroy()
                self.start_exercise(exercise_name, reps)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please select a valid number of reps")

        Button(button_frame, text="OK", command=set_reps, 
               bg="#007BFF", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(button_frame, text="Cancel", command=dialog.destroy,
               bg="#DC3545", fg="white", width=10).pack(side=RIGHT, padx=5)

    def start_exercise(self, exercise_name, target_reps):
        self.exercise_dates[exercise_name] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.exercise_labels[exercise_name].config(
            text=f"{exercise_name} - {self.exercise_dates[exercise_name]}"
        )
        self.show_camera_ui(exercise_name, target_reps)

    def show_camera_ui(self, exercise_name, target_reps):
        try:
            # Show loading screen
            self.show_loading_screen(exercise_name)
            
            # Start model loading in a separate thread
            threading.Thread(target=self.load_camera_model, 
                           args=(exercise_name, target_reps),
                           daemon=True).start()
            
            # Start checking the loading queue
            self.root.after(100, self.check_loading_queue)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
            self.go_to_home_screen()

    def show_loading_screen(self, exercise_name):
        # Clear current widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Loading screen elements
        self.loading_frame = Frame(self.root, bg="#f0f0f0")
        self.loading_frame.pack(expand=True, fill=BOTH)
        
        Label(self.loading_frame, text=f"Initialising {exercise_name}", 
             font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=50)
        
        self.progress = ttk.Progressbar(self.loading_frame, 
                                      orient=HORIZONTAL,
                                      length=300,
                                      mode='indeterminate')
        self.progress.pack(pady=10)
        self.progress.start(10)
        
        self.status_label = Label(self.loading_frame, 
                                text="Loading pose estimation model...",
                                font=("Arial", 14),
                                bg="#f0f0f0")
        self.status_label.pack(pady=10)

    def load_camera_model(self, exercise_name, target_reps):
        try:
            # Simulated loading steps
            self.loading_queue.put(("progress", "Initialising TensorFlow..."))
            time.sleep(1)
            
            self.loading_queue.put(("progress", "Loading MoveNet model..."))
            time.sleep(2)
            
            self.loading_queue.put(("progress", "Initialising camera..."))
            time.sleep(1)
            
            self.loading_queue.put(("complete", ""))
            
            # Import and start camera UI
            from Camera import CameraScreenUI
            self.loading_queue.put(("launch", (exercise_name, target_reps)))
            
        except Exception as e:
            self.loading_queue.put(("error", str(e)))

    def check_loading_queue(self):
        try:
            while True:
                msg_type, content = self.loading_queue.get_nowait()
                
                if msg_type == "progress":
                    self.status_label.config(text=content)
                elif msg_type == "complete":
                    self.progress.stop()
                    self.status_label.config(text="Model loaded successfully!")
                elif msg_type == "launch":
                    exercise_name, target_reps = content
                    self.root.after(500, lambda: self.launch_camera_ui(exercise_name, target_reps))
                elif msg_type == "error":
                    self.progress.stop()
                    self.status_label.config(text=f"Error: {content}", fg="red")
                    Button(self.loading_frame, text="Return to Home", 
                          command=self.go_to_home_screen,
                          bg="#007BFF", fg="white").pack(pady=20)
                    break
                    
        except queue.Empty:
            self.root.after(100, self.check_loading_queue)

    def launch_camera_ui(self, exercise_name, target_reps):
        from Camera import CameraScreenUI
        for widget in self.root.winfo_children():
            widget.destroy()
        CameraScreenUI(self.root, exercise_name, target_reps)

    def request_help(self):
        messagebox.showinfo("Help", "For assistance, please contact x8w11@students.keele.ac.uk")

    def exit_program(self):
        self.root.quit()

    def go_back(self):
        self.go_to_home_screen()

    def go_to_home_screen(self):
        try:
            # Clear current screen properly
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Reinitialise the home screen
            from HomeScreen import HomeScreenUI
            self.root.title("Home Screen")  # Reset window title
            self.root.configure(bg="#f0f0f0")  # Reset background
            HomeScreenUI(self.root)
            
            # Reset any fullscreen attributes if needed
            self.root.attributes('-fullscreen', True)
            
        except ImportError as e:
            messagebox.showerror("Navigation Error", 
                            f"Failed to load home screen: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", 
                            f"Unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = ChooseExercisesUI(root)
    root.mainloop()