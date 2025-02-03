import tkinter as tk
from tkinter import ttk
import random

class DraggableWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.geometry("300x200+100+100")
        self.config(bg="#2a2a2a")
        self.attributes("-alpha", 0.95)
        
        # Custom title bar
        self.title_bar = tk.Frame(self, bg="#1a1a1a", height=30)
        self.title_bar.pack(fill=tk.X)
        
        # Drag functionality
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)
        
        # Close button
        self.close_btn = tk.Label(self.title_bar, text="✕", fg="white", bg="#1a1a1a")
        self.close_btn.pack(side=tk.RIGHT, padx=5)
        self.close_btn.bind("<Button-1>", lambda e: self.destroy())
        
        # Main content
        self.prediction_label = tk.Label(self, text="Next: -", fg="#00ff9d", bg="#2a2a2a", 
                                       font=("Arial", 24, "bold"))
        self.prediction_label.pack(pady=20)
        
        # Confidence meter
        self.canvas = tk.Canvas(self, width=200, height=8, bg="#2a2a2a", 
                              highlightthickness=0)
        self.canvas.pack()
        self.confidence_bar = self.canvas.create_rectangle(0,0,0,8, fill="#00ff9d")
        
        # Stats panel
        self.stats_frame = ttk.Frame(self)
        self.stats_frame.pack(pady=10)
        
        stats = [("Accuracy", "78%"), ("Win Streak", "5"), ("Last 10", "8/10")]
        for text, value in stats:
            tk.Label(self.stats_frame, text=text+":", fg="gray", bg="#2a2a2a").grid(sticky="w")
            tk.Label(self.stats_frame, text=value, fg="#00ff9d", bg="#2a2a2a").grid(row=0, column=1, sticky="e")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        self.geometry(f"+{self.winfo_x()+dx}+{self.winfo_y()+dy}")

    def update_ui(self, prediction, confidence):
        self.prediction_label.config(text=f"Next: {prediction}")
        self.canvas.coords(self.confidence_bar, 0,0,200*(confidence/100),8)
