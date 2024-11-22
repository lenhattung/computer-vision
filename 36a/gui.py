import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
from datetime import datetime
import time
from database import *
from face_recognition import *

class AttendanceGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Hệ thống điểm danh")
        self.window.geometry("1200x700")
        
        self.is_running = False
        self.cap = None
        self.face_recognizer = FaceRecognition()
        self.db = AttendanceDB()
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main container using grid for better control
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Header with class selection and controls
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0,10), sticky="ew")
        
        ttk.Label(header_frame, text="Lớp:").pack(side=tk.LEFT, padx=5)
        self.class_var = tk.StringVar(value="21DTH")
        self.class_entry = ttk.Entry(header_frame, textvariable=self.class_var, width=10)
        self.class_entry.pack(side=tk.LEFT, padx=5)
        
        self.start_btn = ttk.Button(header_frame, text="Bắt đầu điểm danh", command=self.toggle_camera)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(header_frame, text="Xuất báo cáo", command=self.export_attendance).pack(side=tk.LEFT, padx=5)
        
        # Camera and status panel
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=1, column=0, padx=(0,10), sticky="nsew")
        
        # Camera view
        self.camera_label = ttk.Label(left_panel)
        self.camera_label.pack(fill=tk.BOTH, expand=True)
        
        # Status panel
        status_frame = ttk.LabelFrame(left_panel, text="Thông tin điểm danh", padding=5)
        status_frame.pack(fill=tk.X, pady=(10,0))
        
        self.timer_var = tk.StringVar(value="00:00")
        ttk.Label(status_frame, textvariable=self.timer_var, font=('Helvetica', 12, 'bold')).pack()
        
        self.status_var = tk.StringVar(value="Sẵn sàng")
        ttk.Label(status_frame, textvariable=self.status_var).pack()
        
        # Attendance table
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=1, column=1, sticky="nsew")
        
        columns = ('MSSV', 'Họ tên', 'Thời gian', 'Độ tin cậy')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        self.status_text = tk.Text(status_frame, height=5, width=40)
        self.status_text.pack(fill=tk.X, pady=5)

    def toggle_camera(self):
        if not self.is_running:
            self.start_camera()
        else:
            self.stop_camera()

    def start_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Không thể kết nối camera")
            
            self.is_running = True
            self.start_btn.configure(text="Dừng")
            self.status_var.set("Đang điểm danh...")
            self.start_time = time.time()
            self.process_frame()
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
            self.stop_camera()

    def process_frame(self):
        if self.is_running:
            ret, frame = self.cap.read()
            if ret:
                # Face recognition
                results = self.face_recognizer.pipeline_model(frame)
                
                # Dictionary to count detections
                if not hasattr(self, 'detection_counts'):
                    self.detection_counts = {}
                
                # Clear status text and update with current detections
                self.status_text.delete(1.0, tk.END)
                self.status_text.insert(tk.END, "Khuôn mặt đang phát hiện:\n")
                
                # Draw detection boxes and update counts
                for i, bbox in enumerate(results['bbox']):
                    startx, starty, endx, endy = bbox
                    cv2.rectangle(frame, (startx, starty), (endx, endy), (0, 255, 0), 2)
                    
                    student_id = results['face_name'][i]
                    confidence = results['face_name_score'][i]
                    
                    self.detection_counts[student_id] = self.detection_counts.get(student_id, 0) + 1
                    
                    # Display count instead of confidence
                    text = f"{student_id} ({self.detection_counts.get(student_id, 0)})"
                    cv2.putText(frame, text, (startx, starty-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Update status text
                    self.status_text.insert(tk.END, f"{student_id}: {self.detection_counts.get(student_id, 0)} lần\n")
    
                # Update display
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
                
                # Update timer and check for timeout
                elapsed = int(time.time() - self.start_time)
                remaining = max(10 - elapsed, 0)
                self.timer_var.set(f"Còn lại: {remaining}s")
                
                if remaining > 0:
                    self.window.after(10, self.process_frame)
                else:
                    # Find student with highest detection count
                    if self.detection_counts:
                        most_frequent_student = max(self.detection_counts.items(), key=lambda x: x[1])
                        student_id, count = most_frequent_student
                        
                        # Clear existing tree items
                        #for item in self.tree.get_children():
                            #self.tree.delete(item)
                        
                        # Get student name from database
                        student_name = self.db.get_student_name(student_id)
                        current_time = datetime.now().strftime("%H:%M:%S")
                        
                        # Add to database and tree
                        #self.tree.insert('', 'end', values=(
                        #    student_id,
                       #     student_name,
                        #    current_time,
                       #     f"{count} lần"
                        #))
                        
                        if self.db.mark_attendance(student_id, self.class_var.get(), count):
                            self.tree.insert('', 'end', values=(
                                student_id,
                                student_name,
                                current_time,
                                f"{count} lần"
                            ))
                    
                    self.detection_counts = {}
                    self.stop_camera()
                    messagebox.showinfo("Thông báo", "Đã hoàn thành điểm danh")

    def stop_camera(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.start_btn.configure(text="Bắt đầu điểm danh")
        self.status_var.set("Đã dừng")

    def add_attendance_record(self, student_id, confidence):
        # Add new attendance record to treeview
        name = self.db.get_student_name(student_id)
        current_time = datetime.now().strftime("%H:%M:%S")
        
        self.tree.insert('', 0, values=(
            student_id,
            name,
            current_time,
            f"{confidence:.2f}"
        ))

    def export_attendance(self):
        try:
            class_id = self.class_var.get()
            if not class_id:
                raise ValueError("Vui lòng nhập mã lớp")
            
            filename = f"attendance_{class_id}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("MSSV,Họ tên,Thời gian,Độ tin cậy\n")
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    f.write(f"{','.join(map(str, values))}\n")
                    
            messagebox.showinfo("Thành công", f"Đã xuất file {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceGUI(root)
    root.mainloop()