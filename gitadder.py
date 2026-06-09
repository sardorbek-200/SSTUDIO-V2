import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

class SStudioGitPro:
    def __init__(self, root):
        self.root = root
        self.root.title("SStudio Git Select Pro")
        self.root.geometry("600x450")

        # Asosiy jadval (Treeview)
        # selectmode='extended' aynan sen xohlagan "bir nechta faylni alohida tanlash" imkonini beradi
        self.tree = ttk.Treeview(root, columns=("path"), show="tree", selectmode='extended')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Scrollbar (agar fayllar ko'p bo'lsa)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # Tugmalar
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill='x', padx=10, pady=10)

        tk.Button(btn_frame, text="🚀 Tanlanganlarni Add & Commit", 
                  command=self.add_and_commit, bg="#2196F3", fg="white", font=('Arial', 10, 'bold')).pack(fill='x')

        self.load_files()

    def load_files(self):
        # Loyiha papkasini skanerlash
        for root, dirs, files in os.walk('.'):
            for file in files:
                path = os.path.join(root, file)
                # .git va venv kabi narsalarni filtrlaymiz
                if '.git' not in path and 'venv' not in path and '__pycache__' not in path:
                    self.tree.insert('', 'end', text=path)

    def add_and_commit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ogohlantirish", "Hech narsa tanlanmadi!")
            return
        
        # Tanlangan fayllarni add qilish
        for item in selected:
            path = self.tree.item(item, 'text')
            subprocess.run(["git", "add", path])
        
        # Commit qilish
        msg = "SStudio Auto-Commit"
        subprocess.run(["git", "commit", "-m", msg])
        messagebox.showinfo("Success", f"{len(selected)} ta fayl muvaffaqiyatli commit qilindi!")

root = tk.Tk()
app = SStudioGitPro(root)
root.mainloop()