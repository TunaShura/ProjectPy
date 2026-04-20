import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# ================= THEME =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT,
            major TEXT,
            gpa REAL
        )
    ''')
    conn.commit()
    conn.close()

# ================= APP CLASS =================
class StudentApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý sinh viên - University.db")
        self.geometry("680x700")
        self.resizable(False, False)

        #Header
        header = ctk.CTkFrame(self, corner_radius=0, fg_color=("#1a73e8", "#1558b0"))
        header.pack(fill="x")
        ctk.CTkLabel(header, text="  University Student Manager",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white").pack(side="left", pady=14, padx=16)

        #Main container
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=16)

        #Input frame
        input_frame = ctk.CTkFrame(main)
        input_frame.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(input_frame, text="Thong tin sinh vien",
                     font=ctk.CTkFont(size=14, weight="bold")).grid(
                     row=0, column=0, columnspan=4, pady=(12, 8), padx=16, sticky="w")

        fields = [("ID Sinh viên:", "id"), ("Họ và tên:", "name"),
                  ("Chuyên ngành:", "major"), ("Điểm GPA:", "gpa")]

        self.vars = {}
        for i, (label, key) in enumerate(fields):
            col = (i % 2) * 2
            row = 1 + i // 2
            ctk.CTkLabel(input_frame, text=label, anchor="w").grid(
                row=row, column=col, sticky="w", padx=(16 if col == 0 else 10, 4), pady=6)
            var = ctk.StringVar()
            self.vars[key] = var
            ctk.CTkEntry(input_frame, textvariable=var, width=220,
                         placeholder_text=label.replace(":", "")).grid(
                row=row, column=col + 1, sticky="ew", padx=(0, 16 if col == 2 else 8), pady=6)

        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)

        #Button frame
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 12))

        buttons = [
            ("+ Thêm sinh viên",         self.add_student,      "blue",  0, 0),
            ("Cập nhật GPA (theo ID)",    self.update_gpa,       "blue",  0, 1),
            ("Hiển thị tất cả",           self.show_all,         "green", 1, 0),
            ("Lọc GPA > 3.0",            self.filter_gpa,       "green", 1, 1),
            ("Xóa sinh viên GPA < 2.0",  self.delete_low_gpa,   "red",   2, 0),
        ]

        for text, cmd, color, row, col in buttons:
            span = 2 if col == 0 and row == 2 else 1
            ctk.CTkButton(btn_frame, text=text, command=cmd,
                          fg_color={"blue": ("#1a73e8","#1558b0"),
                                    "green": ("#2e7d32","#1b5e20"),
                                    "red": ("#c62828","#8b0000")}[color],
                          hover_color={"blue": "#0d47a1",
                                       "green": "#1b5e20",
                                       "red": "#6a0000"}[color],
                          corner_radius=8, height=38,
                          font=ctk.CTkFont(size=13)).grid(
                row=row, column=col, columnspan=span,
                padx=5, pady=4, sticky="ew")

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # ---- Status badge ----
        self.status_var = ctk.StringVar(value="Sẵn sàng")
        self.status_label = ctk.CTkLabel(main, textvariable=self.status_var,
                                         font=ctk.CTkFont(size=12),
                                         text_color=("gray40", "gray70"))
        self.status_label.pack(anchor="w", pady=(0, 4))

        # ---- List frame ----
        list_frame = ctk.CTkFrame(main)
        list_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(list_frame, text="Danh sách sinh viên",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(
                     anchor="w", padx=16, pady=(12, 6))

        # Header row
        hdr = ctk.CTkFrame(list_frame, fg_color=("#1a73e8","#1558b0"), corner_radius=6)
        hdr.pack(fill="x", padx=12, pady=(0, 4))
        for col, w in zip(["ID", "Họ và tên", "Chuyên ngành", "GPA"],
                          [80, 180, 200, 60]):
            ctk.CTkLabel(hdr, text=col, width=w,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="white").pack(side="left", pady=6, padx=4)

        # Scrollable rows
        self.scroll_frame = ctk.CTkScrollableFrame(list_frame, height=240)
        self.scroll_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.show_all()

    #DB helpers
    def get_conn(self):
        return sqlite3.connect("university.db")

    def set_status(self, msg, color="gray70"):
        self.status_var.set(msg)
        self.status_label.configure(text_color=color)

    def render_rows(self, rows):
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        if not rows:
            ctk.CTkLabel(self.scroll_frame, text="Không có dữ liệu.",
                         text_color=("gray50","gray60")).pack(pady=20)
            return
        for i, row in enumerate(rows):
            bg = ("#f5f5f5","#2b2b2b") if i % 2 == 0 else ("#ffffff","#333333")
            r = ctk.CTkFrame(self.scroll_frame, fg_color=bg, corner_radius=4)
            r.pack(fill="x", pady=1)
            for val, w in zip(row, [80, 180, 200, 60]):
                ctk.CTkLabel(r, text=str(val), width=w,
                             font=ctk.CTkFont(size=12),
                             anchor="w").pack(side="left", pady=5, padx=4)

    # ---- Actions ----
    def add_student(self):
        conn = self.get_conn()
        try:
            conn.cursor().execute(
                "INSERT INTO students VALUES (?,?,?,?)",
                (self.vars["id"].get(), self.vars["name"].get(),
                 self.vars["major"].get(), float(self.vars["gpa"].get())))
            conn.commit()
            self.set_status("Đã thêm sinh viên thành công!", ("#2e7d32","#66bb6a"))
            self.show_all()
        except Exception as e:
            messagebox.showerror("Loi", str(e))
        finally:
            conn.close()

    def show_all(self):
        conn = self.get_conn()
        rows = conn.cursor().execute("SELECT * FROM students").fetchall()
        conn.close()
        self.render_rows(rows)
        self.set_status(f"Hiển thị {len(rows)} sinh viên.")

    def filter_gpa(self):
        conn = self.get_conn()
        rows = conn.cursor().execute(
            "SELECT * FROM students WHERE gpa > 3.0 ORDER BY gpa DESC").fetchall()
        conn.close()
        self.render_rows(rows)
        self.set_status(f"Tìm thấy {len(rows)} sinh viên có GPA > 3.0.",
                        ("#1a73e8","#64b5f6"))

    def update_gpa(self):
        conn = self.get_conn()
        try:
            conn.cursor().execute(
                "UPDATE students SET gpa=? WHERE id=?",
                (float(self.vars["gpa"].get()), self.vars["id"].get()))
            conn.commit()
            self.set_status("Cập nhật GPA thành công!", ("#2e7d32","#66bb6a"))
            self.show_all()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def delete_low_gpa(self):
        if not messagebox.askyesno("Xác nhận", "Xóa tất cả sinh viên có GPA < 2.0?"):
            return
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE gpa < 2.0")
        deleted = cur.rowcount
        conn.commit()
        conn.close()
        self.set_status(f"Đã xóa {deleted} sinh viên có GPA < 2.0.",
                        ("#c62828","#ef9a9a"))
        self.show_all()

# ================= MAIN =================
if __name__ == "__main__":
    init_db()
    app = StudentApp()
    app.mainloop()