import qrcode
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import csv

OUTPUT_DIR = "output_qr"
os.makedirs(OUTPUT_DIR, exist_ok=True)
last_qr_path = None

def generate_single_qr():
    global last_qr_path
    url = entry.get().strip()
    if not url.startswith(("http://", "https://")):
        messagebox.showerror("Invalid URL", "URL must start with http:// or https://")
        return
    filepath = os.path.join(OUTPUT_DIR, "qrcode.png")
    create_qr_image(url, filepath)
    preview_qr(filepath)
    last_qr_path = filepath

def generate_batch_qr():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file) if file_path.endswith(".csv") else (line.strip() for line in file)
        count = 0
        for i, row in enumerate(reader):
            url = row[0] if isinstance(row, list) else row
            if url.startswith(("http://", "https://")):
                filepath = os.path.join(OUTPUT_DIR, f"qr_{i+1}.png")
                create_qr_image(url, filepath)
                count += 1
        messagebox.showinfo("Done", f"{count} QR codes saved to '{OUTPUT_DIR}'")

def save_qr_as():
    if not last_qr_path or not os.path.exists(last_qr_path):
        messagebox.showwarning("No QR", "No QR code to save. Generate one first.")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    if save_path:
        Image.open(last_qr_path).save(save_path)
        messagebox.showinfo("Saved", f"QR code saved to:\n{save_path}")

def create_qr_image(url, filepath):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)

def preview_qr(filepath):
    img = Image.open(filepath).resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    qr_preview.config(image=img_tk)
    qr_preview.image = img_tk

def styled_button(master, text, command, bg, fg):
    return Button(master, text=text, command=command,
                  font=("Segoe UI", 12, "bold"),
                  bg=bg, fg=fg, activebackground="#2d2d2d", activeforeground="white",
                  relief=FLAT, padx=10, pady=6, bd=0, cursor="hand2")

root = Tk()
root.title("QR Code Generator")
root.geometry("460x580")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

Label(root, text="QR Code Generator", font=("Segoe UI", 18, "bold"), fg="#f5f5f5", bg="#1e1e1e").pack(pady=20)

entry = Entry(root, font=("Segoe UI", 12), width=40, bg="#2c2c2c", fg="white", insertbackground="white", relief=FLAT)
entry.pack(pady=10, ipady=8)

styled_button(root, "Generate QR (Manual)", generate_single_qr, "#00b894", "white").pack(pady=8)
styled_button(root, "Generate QR (From File)", generate_batch_qr, "#0984e3", "white").pack(pady=8)
styled_button(root, "💾 Save As...", save_qr_as, "#6c5ce7", "white").pack(pady=8)

qr_preview = Label(root, bg="#1e1e1e")
qr_preview.pack(pady=25)

Label(root, text="Created by Raed — github.com/raed-1", font=("Segoe UI", 9), fg="#888", bg="#1e1e1e").pack(side="bottom", pady=10)

root.mainloop()