import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime
from PIL import Image, ImageTk  # New import

class RecordsScreenUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Exercise Records")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#f0f0f0")

        # Load navigation images first
        self.home_img, self.back_img = self.load_nav_images()
        
        # Create main container
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.data_file = 'exercise_data.csv'

        # Create components
        self.create_menu()
        self.create_nav_buttons()
        self.create_title()
        self.create_table()
        self.create_clear_button()
        self.load_data()

    def load_nav_images(self):
       #Load navigation images with fallback
        try:
            home = ImageTk.PhotoImage(Image.open("assets/home_icon.png").resize((64, 64)))
            back = ImageTk.PhotoImage(Image.open("assets/back_icon.png").resize((64, 64)))
            return home, back
        except Exception as e:
            print(f"Image load error: {e}")
            return None, None

    def create_nav_buttons(self):
        
        nav_frame = tk.Frame(self.root, bg="#f0f0f0")
        nav_frame.place(x=10, y=10, width=140, height=74)

        # Home Button
        self.home_btn = tk.Button(
            nav_frame,
            image=self.home_img,
            command=self.go_home,
            relief=tk.FLAT,
            bg="#f0f0f0",
            activebackground="#e0e0e0"
        )
        if not self.home_img:
            self.home_btn.config(text="🏠", font=("Arial", 24))
        self.home_btn.pack(side=tk.LEFT, padx=5)

        # Back Button
        self.back_btn = tk.Button(
            nav_frame,
            image=self.back_img,
            command=self.go_back,
            relief=tk.FLAT,
            bg="#f0f0f0",
            activebackground="#e0e0e0"
        )
        if not self.back_img:
            self.back_btn.config(text="←", font=("Arial", 24))
        self.back_btn.pack(side=tk.LEFT, padx=5)

        # Button press animations
        for btn in [self.home_btn, self.back_btn]:
            btn.bind("<ButtonPress-1>", lambda e: e.widget.config(relief=tk.SUNKEN))
            btn.bind("<ButtonRelease-1>", lambda e: e.widget.config(relief=tk.FLAT))

    def create_title(self):
        """Create title label"""
        self.title_label = tk.Label(self.main_frame, 
                                  text="Exercise History Records",
                                  font=("Arial", 24, "bold"),
                                  bg="#f0f0f0")
        self.title_label.pack(pady=10)

    def create_table(self):
        """Create table with scrollbars"""
        self.table_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview setup
        self.tree = ttk.Treeview(self.table_frame, 
                                columns=('Date', 'Exercise', 'Target', 'Completed', 
                                         'Duration', 'Score', 'Avg Peak', 'Avg Rest', 'Form'),
                                show='headings')
        
        # Scrollbars
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Configure columns (keep your existing column setup)
        columns = {
            'Date': {'width': 150, 'anchor': 'center'},
            'Exercise': {'width': 120},
            'Target': {'width': 60, 'anchor': 'center'},
            'Completed': {'width': 80, 'anchor': 'center'},
            'Duration': {'width': 80, 'anchor': 'center'},
            'Score': {'width': 60, 'anchor': 'center'},
            'Avg Peak': {'width': 80, 'anchor': 'center'},
            'Avg Rest': {'width': 80, 'anchor': 'center'},
            'Form': {'width': 80, 'anchor': 'center'}
        }
        
        for col, config in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, **config)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

    def create_clear_button(self):
 
        btn_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        self.clear_btn = tk.Button(btn_frame, 
                                 text="Clear All Records",
                                 command=self.clear_records,
                                 font=("Arial", 12),
                                 bg="#DC3545", fg="white",
                                 width=20)
        self.clear_btn.pack()

    def load_data(self):
        if not os.path.exists(self.data_file):
            self.no_data_label = tk.Label(self.table_frame,
                                         text="No exercise records found",
                                         font=("Arial", 16),
                                         bg="#f0f0f0")
            self.no_data_label.pack(pady=50)
            return

        with open(self.data_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                duration = f"{float(row['duration'])/60:.1f} min"
                score = f"{float(row['score']):.1f}%"
                self.tree.insert('', 'end', values=(
                    row['timestamp'],
                    row['exercise_name'],
                    row['target_reps'],
                    row['completed_reps'],
                    duration,
                    score,
                    f"{float(row['avg_peak_angle']):.1f}°",
                    f"{float(row['avg_rest_angle']):.1f}°",
                    f"{float(row['form_consistency'])*100:.1f}%"
                ))

    def sort_column(self, col):
        items = [(self.tree.set(child, col), child) 
                for child in self.tree.get_children('')]
        
        try:
            items.sort(key=lambda x: float(x[0].strip('%° min')))
        except ValueError:
            items.sort()

        for index, (val, child) in enumerate(items):
            self.tree.move(child, '', index)

    def clear_records(self):
        if messagebox.askyesno("Confirm Clear", "Delete all exercise records?"):
            try:
                with open(self.data_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'timestamp', 'exercise_name', 'target_reps',
                        'completed_reps', 'duration', 'score',
                        'avg_peak_angle', 'avg_rest_angle', 'form_consistency'
                    ])
                
                for item in self.tree.get_children():
                    self.tree.delete(item)
                    
                messagebox.showinfo("Success", "All records have been cleared")
            except Exception as e:
                messagebox.showerror("Error", f"Could not clear records: {str(e)}")

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Request Help", command=self.show_help)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def show_help(self):
        messagebox.showinfo("Help", 
                           "Records View Help:\n\n"
                           "- Click column headers to sort\n"
                           "- Use scrollbars to navigate\n"
                           "3. Contact [Your Email Here]") # Was originally an email removed for privacy reasons

    def go_back(self):
        self.go_home()

    def go_home(self):
        from HomeScreen import HomeScreenUI
        self.destroy_current_screen()
        HomeScreenUI(self.root)

    def destroy_current_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RecordsScreenUI(root)
    root.mainloop()