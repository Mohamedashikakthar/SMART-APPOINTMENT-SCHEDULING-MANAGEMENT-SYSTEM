# Smart Appointment Scheduling System
# Python + Tkinter + MySQL

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry

# ---------------- DATABASE ----------------
def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jenish@2003",
        database="appointment_db"
    )

# ================= LOGIN PAGE =================
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.state("zoomed")   # FULL SCREEN FIX

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.create_ui()

    def create_ui(self):
        frame = tk.Frame(self.root, bg="#2c3e50")
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Smart Appointment Scheduling System",
                 font=("Arial", 28, "bold"),
                 fg="white", bg="#2c3e50").pack(pady=40)

        form = tk.Frame(frame, bg="white", bd=6)
        form.pack(pady=20)

        tk.Label(form, text="Username").grid(row=0, column=0, padx=15, pady=10)
        tk.Entry(form, textvariable=self.username).grid(row=0, column=1)

        tk.Label(form, text="Password").grid(row=1, column=0, padx=15, pady=10)
        tk.Entry(form, textvariable=self.password, show="*").grid(row=1, column=1)

        tk.Button(form, text="Login", width=15,
                  bg="green", fg="white",
                  command=self.check_login).grid(row=2, columnspan=2, pady=10)

        # ✅ EXIT BUTTON ADDED
        tk.Button(frame, text="Exit", width=12,
                  bg="red", fg="white",
                  command=self.root.destroy).pack(pady=10)

    def check_login(self):
        if self.username.get() == "admin" and self.password.get() == "admin":
            self.root.destroy()
            root = tk.Tk()
            AppointmentApp(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid Login")

# ================= MAIN APP =================
class AppointmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Appointment Scheduling System")
        self.root.state("zoomed")   # FULL SCREEN FIX

        # Variables
        self.client_name = tk.StringVar()
        self.contact = tk.StringVar()
        self.email = tk.StringVar()
        self.service = tk.StringVar()
        self.date = tk.StringVar()
        self.status = tk.StringVar()
        self.notes = tk.StringVar()
        self.search = tk.StringVar()
        self.hour = tk.StringVar(value="09")
        self.minute = tk.StringVar(value="00")
        self.selected_id = None

        self.create_ui()
        self.fetch_data()

    def create_ui(self):
        # TITLE
        tk.Label(self.root, text="Smart Appointment Scheduling System",
                 font=("Arial", 22, "bold"),
                 bg="#34495e", fg="white").grid(row=0, column=0, columnspan=2, sticky="ew")

        # MAIN FRAMES
        left = tk.Frame(self.root, bd=4, relief=tk.RIDGE)
        left.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        right = tk.Frame(self.root, bd=4, relief=tk.RIDGE)
        right.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

        # -------- LEFT FORM --------
        labels = ["Client Name","Contact","Email","Service","Date","Time","Status","Notes"]
        vars_ = [self.client_name,self.contact,self.email,
                 self.service,self.date,None,self.status,self.notes]

        for i, lbl in enumerate(labels):
            tk.Label(left, text=lbl).grid(row=i, column=0, padx=10, pady=6, sticky="w")

        tk.Entry(left, textvariable=self.client_name).grid(row=0, column=1)
        tk.Entry(left, textvariable=self.contact).grid(row=1, column=1)
        tk.Entry(left, textvariable=self.email).grid(row=2, column=1)

        ttk.Combobox(left, textvariable=self.service,
                     values=("Consultation","Coding","Design"),
                     state="readonly").grid(row=3, column=1)

        DateEntry(left, textvariable=self.date).grid(row=4, column=1)

        tf = tk.Frame(left)
        tf.grid(row=5, column=1)
        tk.Spinbox(tf, from_=0, to=23, width=4, textvariable=self.hour,
                   format="%02.0f").pack(side=tk.LEFT)
        tk.Label(tf, text=":").pack(side=tk.LEFT)
        tk.Spinbox(tf, from_=0, to=59, width=4, textvariable=self.minute,
                   format="%02.0f").pack(side=tk.LEFT)

        ttk.Combobox(left, textvariable=self.status,
                     values=("Confirmed","Cancelled","Completed"),
                     state="readonly").grid(row=6, column=1)

        tk.Entry(left, textvariable=self.notes).grid(row=7, column=1)

        tk.Button(left, text="Add", width=12, command=self.add_record).grid(row=8, column=0, pady=10)
        tk.Button(left, text="Update", width=12, command=self.update_record).grid(row=8, column=1)
        tk.Button(left, text="Delete", width=12, command=self.delete_record).grid(row=9, column=0)
        tk.Button(left, text="Clear", width=12, command=self.clear_fields).grid(row=9, column=1)

        # -------- RIGHT TABLE --------
        tk.Label(right, text="Search:").grid(row=0, column=0, padx=10)
        tk.Entry(right, textvariable=self.search, width=30).grid(row=0, column=1)
        tk.Button(right, text="Search", command=self.search_data).grid(row=0, column=2)
        tk.Button(right, text="View All", command=self.fetch_data).grid(row=0, column=3)

        cols = ("ID","NAME","CONTACT","EMAIL","SERVICE","DATE","TIME","STATUS","NOTES")
        self.table = ttk.Treeview(right, columns=cols, show="headings")

        for c in cols:
            self.table.heading(c, text=c)
            self.table.column(c, width=120)

        self.table.grid(row=1, column=0, columnspan=4, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(3, weight=1)

        self.table.bind("<ButtonRelease-1>", self.get_cursor)

    # -------- DB FUNCTIONS --------
    def get_time(self):
        return f"{self.hour.get()}:{self.minute.get()}"

    def add_record(self):
        con = db_connection(); cur = con.cursor()
        cur.execute("""
        INSERT INTO appointments
        (client_name,contact,email,service_type,app_date,app_time,status,notes)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            self.client_name.get(), self.contact.get(), self.email.get(),
            self.service.get(), self.date.get(),
            self.get_time(), self.status.get(), self.notes.get()
        ))
        con.commit(); con.close()
        self.fetch_data(); self.clear_fields()

    def fetch_data(self):
        con = db_connection(); cur = con.cursor()
        cur.execute("SELECT * FROM appointments")
        self.table.delete(*self.table.get_children())
        for r in cur.fetchall():
            self.table.insert("", tk.END, values=r)
        con.close()

    def get_cursor(self, e):
        row = self.table.item(self.table.focus())['values']
        if row:
            self.selected_id = row[0]
            self.client_name.set(row[1])
            self.contact.set(row[2])
            self.email.set(row[3])
            self.service.set(row[4])
            self.date.set(row[5])
            h,m = row[6].split(":")
            self.hour.set(h); self.minute.set(m)
            self.status.set(row[7])
            self.notes.set(row[8])

    def update_record(self):
        con = db_connection(); cur = con.cursor()
        cur.execute("""
        UPDATE appointments SET
        client_name=%s,contact=%s,email=%s,service_type=%s,
        app_date=%s,app_time=%s,status=%s,notes=%s
        WHERE id=%s
        """, (
            self.client_name.get(), self.contact.get(), self.email.get(),
            self.service.get(), self.date.get(),
            self.get_time(), self.status.get(), self.notes.get(),
            self.selected_id
        ))
        con.commit(); con.close()
        self.fetch_data()

    def delete_record(self):
        con = db_connection(); cur = con.cursor()
        cur.execute("DELETE FROM appointments WHERE id=%s",(self.selected_id,))
        con.commit(); con.close()
        self.fetch_data(); self.clear_fields()

    def search_data(self):
        key = self.search.get()
        con = db_connection(); cur = con.cursor()
        cur.execute("""
        SELECT * FROM appointments WHERE
        client_name LIKE %s OR contact LIKE %s OR email LIKE %s
        """,(f"%{key}%",)*3)
        self.table.delete(*self.table.get_children())
        for r in cur.fetchall():
            self.table.insert("", tk.END, values=r)
        con.close()

    def clear_fields(self):
        self.client_name.set(""); self.contact.set("")
        self.email.set(""); self.service.set("")
        self.status.set(""); self.notes.set("")
        self.selected_id = None

# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
