# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 12:41:37 2025
@author: Boss Ashik
"""

# Smart Appointment Scheduling System with Login Page
# Technologies: Python, Tkinter, MySQL

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry
from PIL import Image, ImageTk

# -------------------- DATABASE CONNECTION --------------------

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jenish@2003",
        database="appointments_db"
    )

# ==================== LOGIN PAGE ====================

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Smart Appointment System")
        self.root.attributes("-fullscreen", True)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.create_login_ui()

    def create_login_ui(self):
        bg_frame = tk.Frame(self.root, bg="#2c3e50")
        bg_frame.pack(fill=tk.BOTH, expand=True)

        # -------- IMAGE (SAFE LOAD) --------
        try:
            img = Image.open("login.png")  # keep image in same folder
            img = img.resize((400, 400))
            self.photo = ImageTk.PhotoImage(img)
            tk.Label(bg_frame, image=self.photo, bg="#2c3e50").pack(pady=20)
        except:
            tk.Label(
                bg_frame,
                text="Smart Appointment System",
                font=("Arial", 28, "bold"),
                fg="white",
                bg="#2c3e50"
            ).pack(pady=40)

        tk.Label(
            bg_frame,
            text="LOGIN",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=10)

        form = tk.Frame(bg_frame, bg="white", bd=6)
        form.pack(pady=20)

        tk.Label(form, text="Username", font=("Arial", 12)).grid(row=0, column=0, padx=15, pady=15)
        tk.Entry(form, textvariable=self.username, font=("Arial", 12)).grid(row=0, column=1, padx=15)

        tk.Label(form, text="Password", font=("Arial", 12)).grid(row=1, column=0, padx=15, pady=15)
        tk.Entry(form, textvariable=self.password, show="*", font=("Arial", 12)).grid(row=1, column=1, padx=15)

        tk.Button(
            form,
            text="Login",
            width=18,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.check_login
        ).grid(row=2, columnspan=2, pady=20)

        tk.Button(
            bg_frame,
            text="Exit",
            bg="red",
            fg="white",
            font=("Arial", 11),
            width=10,
            command=self.root.destroy
        ).pack(pady=10)

    def check_login(self):
        # Static login (for project demo)
        if self.username.get() == "admin" and self.password.get() == "admin":
            self.root.destroy()
            main_root = tk.Tk()
            AppointmentApp(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

# ==================== MAIN APPLICATION ====================

class AppointmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Appointment Scheduling System")
        self.root.attributes("-fullscreen", True)

        # Variables
        self.client_name = tk.StringVar()
        self.contact = tk.StringVar()
        self.email = tk.StringVar()
        self.service = tk.StringVar()
        self.date = tk.StringVar()
        self.status = tk.StringVar()
        self.notes = tk.StringVar()
        self.search_var = tk.StringVar()

        self.hour = tk.StringVar(value="09")
        self.minute = tk.StringVar(value="00")
        self.selected_id = None

        self.create_widgets()
        self.fetch_data()

    # ---------------- GUI ----------------
    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Smart Appointment Scheduling System",
            font=("Arial", 22, "bold"),
            bg="#34495e",
            fg="white"
        )
        title.pack(fill=tk.X)

        tk.Button(
            self.root,
            text="Logout",
            bg="red",
            fg="white",
            font=("Arial", 11),
            command=self.logout
        ).pack(anchor="ne", padx=20, pady=5)

        # -------- LEFT FRAME --------
        frame1 = tk.Frame(self.root, bd=4, relief=tk.RIDGE)
        frame1.place(x=20, y=80, width=400, height=600)

        tk.Label(frame1, text="Appointment Details", font=("Arial", 14, "bold")).grid(row=0, columnspan=2, pady=10)

        labels = [
            "Client Name", "Contact", "Email", "Service",
            "Appointment Date", "Appointment Time", "Status", "Notes"
        ]

        for i, text in enumerate(labels):
            tk.Label(frame1, text=text).grid(row=i+1, column=0, sticky="w", padx=10, pady=5)

        tk.Entry(frame1, textvariable=self.client_name).grid(row=1, column=1)
        tk.Entry(frame1, textvariable=self.contact).grid(row=2, column=1)
        tk.Entry(frame1, textvariable=self.email).grid(row=3, column=1)

        ttk.Combobox(
            frame1,
            textvariable=self.service,
            state="readonly",
            values=("Logo Design", "Coding Class", "Resume Review", "Consultation", "Tutoring")
        ).grid(row=4, column=1)

        DateEntry(frame1, textvariable=self.date, date_pattern="yyyy-mm-dd").grid(row=5, column=1)

        time_frame = tk.Frame(frame1)
        time_frame.grid(row=6, column=1)
        tk.Spinbox(time_frame, from_=0, to=23, width=3, textvariable=self.hour, format="%02.0f").pack(side=tk.LEFT)
        tk.Label(time_frame, text=":").pack(side=tk.LEFT)
        tk.Spinbox(time_frame, from_=0, to=59, width=3, textvariable=self.minute, format="%02.0f").pack(side=tk.LEFT)

        ttk.Combobox(
            frame1,
            textvariable=self.status,
            state="readonly",
            values=("Confirmed", "Cancelled", "Completed")
        ).grid(row=7, column=1)

        tk.Entry(frame1, textvariable=self.notes).grid(row=8, column=1)

        tk.Button(frame1, text="Add", width=12, command=self.add_record).grid(row=9, column=0, pady=10)
        tk.Button(frame1, text="Update", width=12, command=self.update_record).grid(row=9, column=1)
        tk.Button(frame1, text="Delete", width=12, command=self.delete_record).grid(row=10, column=0)
        tk.Button(frame1, text="Clear", width=12, command=self.clear_fields).grid(row=10, column=1)

        # -------- RIGHT FRAME --------
        frame2 = tk.Frame(self.root, bd=4, relief=tk.RIDGE)
        frame2.place(x=450, y=80, width=850, height=600)

        tk.Entry(frame2, textvariable=self.search_var).grid(row=0, column=0, padx=10)
        tk.Button(frame2, text="Search", command=self.search_record).grid(row=0, column=1)
        tk.Button(frame2, text="View All", command=self.fetch_data).grid(row=0, column=2)

        self.table = ttk.Treeview(
            frame2,
            columns=("id","name","contact","email","service","date","time","status","notes"),
            show="headings"
        )

        for col in self.table["columns"]:
            self.table.heading(col, text=col.upper())

        self.table.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.table.bind("<ButtonRelease-1>", self.get_cursor)

    # ---------------- DATABASE FUNCTIONS ----------------
    def get_time(self):
        return f"{self.hour.get()}:{self.minute.get()}"

    def add_record(self):
        con = db_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO appointments (client_name,contact,email,service_type,app_date,app_time,status,notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                self.client_name.get(), self.contact.get(), self.email.get(),
                self.service.get(), self.date.get(), self.get_time(),
                self.status.get(), self.notes.get()
            )
        )
        con.commit(); con.close()
        self.fetch_data(); self.clear_fields()
        messagebox.showinfo("Success", "Appointment Added")

    def fetch_data(self):
        con = db_connection(); cur = con.cursor()
        cur.execute("SELECT * FROM appointments")
        self.table.delete(*self.table.get_children())
        for row in cur.fetchall():
            self.table.insert("", tk.END, values=row)
        con.close()

    def get_cursor(self, event):
        row = self.table.item(self.table.focus())['values']
        if row:
            self.selected_id = row[0]
            self.client_name.set(row[1])
            self.contact.set(row[2])
            self.email.set(row[3])
            self.service.set(row[4])
            self.date.set(row[5])
            h, m = row[6].split(':')
            self.hour.set(h); self.minute.set(m)
            self.status.set(row[7])
            self.notes.set(row[8])

    def update_record(self):
        con = db_connection(); cur = con.cursor()
        cur.execute(
            "UPDATE appointments SET client_name=%s,contact=%s,email=%s,service_type=%s,app_date=%s,app_time=%s,status=%s,notes=%s WHERE id=%s",
            (
                self.client_name.get(), self.contact.get(), self.email.get(),
                self.service.get(), self.date.get(), self.get_time(),
                self.status.get(), self.notes.get(), self.selected_id
            )
        )
        con.commit(); con.close(); self.fetch_data()
        messagebox.showinfo("Updated", "Appointment Updated")

    def delete_record(self):
        con = db_connection(); cur = con.cursor()
        cur.execute("DELETE FROM appointments WHERE id=%s", (self.selected_id,))
        con.commit(); con.close(); self.fetch_data(); self.clear_fields()

    def search_record(self):
        con = db_connection(); cur = con.cursor()
        cur.execute("SELECT * FROM appointments WHERE client_name LIKE %s OR app_date LIKE %s",
                    (f"%{self.search_var.get()}%", f"%{self.search_var.get()}%"))
        self.table.delete(*self.table.get_children())
        for row in cur.fetchall():
            self.table.insert("", tk.END, values=row)
        con.close()

    def clear_fields(self):
        self.client_name.set(""); self.contact.set(""); self.email.set("")
        self.service.set(""); self.status.set(""); self.notes.set("")
        self.selected_id = None

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        LoginPage(root)
        root.mainloop()

# ==================== RUN APPLICATION ====================
if __name__ == "__main__":
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
