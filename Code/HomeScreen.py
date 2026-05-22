from tkinter import *
from tkinter import messagebox
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
from datetime import datetime


class HomeScreenUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Exercise Analytics")
        self.root.attributes('-fullscreen', True)
        self.current_chart = 0
        self.chart_cycle = None
        self.data_file = 'exercise_data.csv'
        
        # Main container setup
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=True)
        
        try:
            # Validate CSV first
            if not self.validate_csv():
                raise Exception("Invalid or missing exercise_data.csv")
            
            # Load initial data
            self.df = self.load_data()
            
            # Setup UI components
            self.create_menu()
            self.create_widgets()
            self.setup_charts()
            self.create_nav_dots()
            self.setup_chart_cycle()
            
        except Exception as e:
            messagebox.showerror("Initialization Error", 
                f"Failed to start application:\n{str(e)}\n\n"
                "Ensure:\n1. exercise_data.csv exists\n2. Correct format\n"
                "3. Required packages installed")
            self.root.quit()

    def validate_csv(self):
        required_cols = ['timestamp', 'exercise_name', 'target_reps',
                        'completed_reps', 'duration', 'score',
                        'avg_peak_angle', 'avg_rest_angle', 'form_consistency']
        if not os.path.exists(self.data_file):
            return False
        try:
            df = pd.read_csv(self.data_file)
            return all(col in df.columns for col in required_cols)
        except:
            return False

    def load_data(self):
        df = pd.read_csv(self.data_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df

    def create_menu(self):
        menubar = Menu(self.root)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Request Help", command=self.request_help)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_program)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def create_widgets(self):
        # Header
        Label(self.main_frame, text="Exercise Analytics Dashboard", 
             font=("Arial", 16, "bold"), pady=10).pack()
        
        # Buttons frame
        btn_frame = Frame(self.main_frame)
        btn_frame.pack(pady=10)
        
        Button(btn_frame, text="Choose Exercise", command=self.open_choose_exercises,
              bg="#007BFF", fg="white", width=20).pack(side=LEFT, padx=10)
        Button(btn_frame, text="View Records", command=self.open_records_screen,
              bg="#28A745", fg="white", width=20).pack(side=LEFT, padx=10)
        
        # Chart container
        self.chart_frame = Frame(self.main_frame)
        self.chart_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Navigation dots
        self.nav_dots_frame = Frame(self.main_frame)
        self.nav_dots_frame.pack(pady=10)

    def setup_charts(self):
        self.chart_figs = []
        self.chart_canvases = []
        
        # Create all three chart types
        self.create_line_chart()
        self.create_bar_chart()
        self.create_radar_chart()
        
        # Hide all initially
        for canvas in self.chart_canvases:
            canvas.get_tk_widget().pack_forget()
        
        # Show first chart
        self.chart_canvases[0].get_tk_widget().pack(fill=BOTH, expand=True)

    def create_line_chart(self):
        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Get last 5 exercises
        recent_data = self.df.tail(5)
        ax.plot(recent_data['timestamp'], recent_data['duration'], 
               marker='o', color='#007BFF')
        
        ax.set_title("Recent Exercise Duration Trend", fontsize=14)
        ax.set_ylabel("Duration (minutes)", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.setp(ax.get_xticklabels(), rotation=45)
        
        self.chart_figs.append(fig)
        self.chart_canvases.append(FigureCanvasTkAgg(fig, self.chart_frame))

    def create_bar_chart(self):
        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Calculate completion rates
        completion = (self.df['completed_reps'] / self.df['target_reps'] * 100)
        exercise_types = self.df['exercise_name'].value_counts().index
        
        ax.bar(exercise_types, completion.groupby(self.df['exercise_name']).mean(),
              color=['#28A745', '#FFC107', '#DC3545'])
        
        ax.set_title("Average Completion Rate by Exercise Type", fontsize=14)
        ax.set_ylabel("Completion Rate (%)", fontsize=12)
        ax.set_ylim(0, 100)
        
        self.chart_figs.append(fig)
        self.chart_canvases.append(FigureCanvasTkAgg(fig, self.chart_frame))

    def create_radar_chart(self):
        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111, polar=True)
        
        # Calculate average metrics
        metrics = {
            'Duration': self.df['duration'].mean(),
            'Completion': (self.df['completed_reps'] / self.df['target_reps']).mean() * 100,
            'Form': self.df['form_consistency'].mean() * 100,
            'Peak Angle': self.df['avg_peak_angle'].mean(),
            'Rest Angle': self.df['avg_rest_angle'].mean()
        }
        
        # Normalize values
        max_val = max(metrics.values())
        values = [v/max_val*100 for v in metrics.values()]
        categories = list(metrics.keys())
        
        # Complete the loop
        values += values[:1]
        angles = [n / len(categories) * 2 * 3.14159 for n in range(len(categories))]
        angles += angles[:1]
        
        ax.plot(angles, values, color='#FF5733', linewidth=2)
        ax.fill(angles, values, color='#FF5733', alpha=0.25)
        ax.set_theta_offset(3.14159 / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids([a * 180/3.14159 for a in angles[:-1]], categories)
        
        # Modified title positioning
        ax.set_title("Performance Overview Radar Chart", 
                    fontsize=14,
                    y=1.0,  # Move title up (default=1.0)
                    pad= 20)  # Add padding above title
        
        self.chart_figs.append(fig)
        self.chart_canvases.append(FigureCanvasTkAgg(fig, self.chart_frame))

    def create_nav_dots(self):
        self.dots = []
        for i in range(3):
            dot = Canvas(self.nav_dots_frame, width=25, height=25, 
                        bg='white', highlightthickness=0)
            dot.create_oval(5, 5, 20, 20, fill='gray', outline='gray')
            dot.pack(side=LEFT, padx=5)
            dot.bind("<Button-1>", lambda e, idx=i: self.show_chart(idx))
            self.dots.append(dot)
        self.update_dots(0)

    def update_dots(self, active_idx):
        for i, dot in enumerate(self.dots):
            color = "#007BFF" if i == active_idx else "gray"
            dot.itemconfig(1, fill=color, outline=color)

    def setup_chart_cycle(self):
        self.chart_cycle = self.root.after(10000, self.cycle_charts)

    def cycle_charts(self):
        self.show_chart((self.current_chart + 1) % 3)
        self.chart_cycle = self.root.after(10000, self.cycle_charts)

    def show_chart(self, idx):
        # Hide all charts
        for canvas in self.chart_canvases:
            canvas.get_tk_widget().pack_forget()
        
        # Show selected chart
        self.chart_canvases[idx].get_tk_widget().pack(fill=BOTH, expand=True)
        self.current_chart = idx
        self.update_dots(idx)
        
        # Restart cycle timer
        if self.chart_cycle:
            self.root.after_cancel(self.chart_cycle)
        self.setup_chart_cycle()

    def open_choose_exercises(self):
        self.cleanup()
        from ChooseExercises import ChooseExercisesUI
        ChooseExercisesUI(self.root)

    def open_records_screen(self):
        self.cleanup()
        from Records import RecordsScreenUI
        RecordsScreenUI(self.root)
    
    def cleanup(self):
        if self.chart_cycle:
            self.root.after_cancel(self.chart_cycle)
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def request_help(self):
        messagebox.showinfo("Help", 
                         "Exercise Analytics Help:\n\n"
                         "1. Charts cycle every 10 seconds\n"
                         "2. Click dots to select charts\n"
                         "3. Contact [Your Email Here]") # Was originally an email removed for privacy reasons

    def exit_program(self):
        if self.chart_cycle:
            self.root.after_cancel(self.chart_cycle)
        self.root.quit()

if __name__ == "__main__":
    root = Tk()
    app = HomeScreenUI(root)
    root.mainloop()