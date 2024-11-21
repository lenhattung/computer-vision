import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
from collections import Counter
from datetime import datetime
import time
from database import AttendanceDB
from face_recognition import FaceRecognition
from config import *

class AttendanceGUI:
    def __init__(self, window):
        self.window = window
        self.window.title(WINDOW_TITLE)
        self.window.geometry(WINDOW_SIZE)
    
        # Khởi tạo biến
        self.is_running = False
        self.detected_faces = []
        self.start_time = None
        self.cap = None
    
        # Khởi tạo face recognition và database
        self.face_recognizer = FaceRecognition()
        self.db = AttendanceDB()
    
        self.setup_gui()
        
    def setup_gui(self):
        # Main container
        container = ttk.Frame(self.window)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel for camera
        left_panel = ttk.Frame(container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Camera frame
        self.camera_frame = ttk.Frame(left_panel, relief='groove', borderwidth=2)
        self.camera_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.camera_label = ttk.Label(self.camera_frame)
        self.camera_label.pack(fill=tk.BOTH, expand=True)

        # Control panel
        control_panel = ttk.Frame(left_panel)
        control_panel.pack(fill=tk.X, pady=5)

        # Class entry
        ttk.Label(control_panel, text="Lớp:").pack(side=tk.LEFT, padx=5)
        self.class_var = tk.StringVar(value=DEFAULT_CLASS)
        ttk.Entry(control_panel, textvariable=self.class_var, width=10).pack(side=tk.LEFT, padx=5)

        # Control buttons
        self.start_btn = ttk.Button(control_panel, text="Bắt đầu", command=self.start_camera)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_panel, text="Xuất báo cáo", command=self.export_report).pack(side=tk.LEFT, padx=5)

        # Status frame
        status_frame = ttk.LabelFrame(left_panel, text="Trạng thái", padding=5)
        status_frame.pack(fill=tk.X, pady=5)

        # Timer label with bigger font
        self.timer_var = tk.StringVar(value="Thời gian còn lại: 15s")
        self.timer_label = ttk.Label(status_frame, textvariable=self.timer_var,
                                     font=('Helvetica', 12, 'bold'))
        self.timer_label.pack(fill=tk.X)

        self.status_var = tk.StringVar(value="Trạng thái: Chưa khởi động")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(fill=tk.X)

        # Detection results
        self.count_text = tk.Text(status_frame, height=4, width=40, font=('Helvetica', 10))
        self.count_text.pack(fill=tk.X, pady=(5, 0))

        # Right panel
        right_panel = ttk.Frame(container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        # Attendance table
        table_frame = ttk.LabelFrame(right_panel, text="Danh sách điểm danh", padding=5)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Create treeview
        columns = ('MSSV', 'Họ tên', 'Thời gian', 'Số lần')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)

        # Define headings
        self.tree.heading('MSSV', text='MSSV')
        self.tree.heading('Họ tên', text='Họ tên')
        self.tree.heading('Thời gian', text='Thời gian')
        self.tree.heading('Số lần', text='Số lần')

        # Define columns
        self.tree.column('MSSV', width=100)
        self.tree.column('Họ tên', width=150)
        self.tree.column('Thời gian', width=100)
        self.tree.column('Số lần', width=70)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def start_camera(self):
        print('start camera')
        
    def handle_camera_error(self, error_message):
        print(error_message)
        
    def process_frame(self):
        print('Dang xu ly frame')
    
    def stop_camera(self):
        print('stop_camera')
    
    def update_status(self, message):
        print('update_status')
    
    def process_attendance(self):
        print('process_attendance')
    
    def add_attendance_record(self, student_id, count):
        print('add_attendance_record')
        
    def export_report(self):
        print('export_report')
        
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceGUI(root)
    root.mainloop()    