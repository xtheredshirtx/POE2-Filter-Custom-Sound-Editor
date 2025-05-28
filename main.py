import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil

class FilterSoundEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("POE2 Filter Sound Editor")
        self.root.geometry("1200x600")
        self.root.minsize(800, 400)
        self.filter_data = []
        self.filter_path = ""
        self.bulk_mode = tk.BooleanVar(value=False)

        self.setup_gui()

    def setup_gui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Load Filter File", command=self.load_filter).pack(pady=5)

        self.tree = ttk.Treeview(frame, columns=("rarity", "sound", "context"), show='headings')
        self.tree.heading("rarity", text="Rarity")
        self.tree.heading("sound", text="Sound File")
        self.tree.heading("context", text="Item Context")
        self.tree.column("rarity", width=150, anchor=tk.W)
        self.tree.column("sound", width=300, anchor=tk.W)
        self.tree.column("context", width=700, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.context_label = ttk.Label(frame, text="Item Context: ", wraplength=1100, justify="left")
        self.context_label.pack(pady=5)

        options_frame = ttk.Frame(frame)
        options_frame.pack(pady=5)

        ttk.Checkbutton(options_frame, text="Bulk Replace All Matching Sounds", variable=self.bulk_mode).pack(side=tk.LEFT, padx=5)
        ttk.Button(options_frame, text="Replace Sound File", command=self.replace_sound).pack(side=tk.LEFT, padx=5)

        self.tree.bind("<<TreeviewSelect>>", self.display_context)

    def load_filter(self):
        self.filter_path = filedialog.askopenfilename(filetypes=[("Filter Files", "*.filter")])
        if not self.filter_path:
            return

        with open(self.filter_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

        self.refresh_filter_data()

    def refresh_filter_data(self):
        self.filter_data.clear()
        self.tree.delete(*self.tree.get_children())

        current_block = []
        self.block_indices = []
        start_idx = 0
        for i, line in enumerate(self.lines):
            stripped = line.strip()
            if stripped.startswith("Show") or stripped.startswith("Hide"):
                if current_block:
                    self.process_block(current_block, start_idx)
                current_block = [stripped]
                start_idx = i
            else:
                current_block.append(stripped)

        if current_block:
            self.process_block(current_block, start_idx)

        self.tree.yview_moveto(0)

    def process_block(self, block, start_idx):
        sound_lines = [l for l in block if "CustomAlertSound" in l or "PlayAlertSound" in l]
        if not sound_lines:
            return

        rarity_lines = [l for l in block if "Rarity" in l]
        if not rarity_lines:
            rarity_lines = ["Rarity Unknown"]

        context_lines = [l for l in block if any(k in l for k in ["Class", "BaseType", "ItemLevel", "Sockets", "GemLevel", "DropLevel", "HasInfluence", "BaseDefencePercentile", "Corrupted"])]
        header = block[0] if block else ""

        rarity = ", ".join(rarity_lines)
        context = " ; ".join(context_lines)

        for sound in sound_lines:
            parts = sound.split('"')
            if len(parts) > 1:
                sound_file = parts[1]
                self.filter_data.append({
                    "rarity": rarity,
                    "sound": sound_file,
                    "line": sound,
                    "context": context,
                    "header": header,
                    "start_idx": start_idx
                })
                self.tree.insert("", "end", values=(rarity, sound_file, context))

    def display_context(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected)['values']
            self.context_label.config(text=f"Item Context: {values[2]}")

    def replace_sound(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a sound entry to replace.")
            return

        entry = self.tree.item(selected)['values']

        new_sound_path = filedialog.askopenfilename(filetypes=[
            ("Audio Files", "*.wav *.ogg *.mp3 *.wmv")
        ])
        if not new_sound_path:
            return

        new_filename = os.path.basename(new_sound_path)
        dest_path = os.path.join(os.path.dirname(self.filter_path), new_filename)

        try:
            shutil.copy(new_sound_path, dest_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy new sound file: {e}")
            return

        def update_sound(start_idx, old_sound):
            i = start_idx
            while i < len(self.lines):
                line = self.lines[i].strip()
                if (line.startswith("Show") or line.startswith("Hide")) and i != start_idx:
                    break
                if ("CustomAlertSound" in line or "PlayAlertSound" in line) and old_sound in line:
                    self.lines[i] = f'CustomAlertSound "{new_filename}" 300\n'
                    break
                if ("#CustomAlertSound" in line or "# CustomAlertSound" in line) and old_sound in line:
                    self.lines[i] = f'CustomAlertSound "{new_filename}" 300\n'
                    break
                i += 1

        if self.bulk_mode.get():
            for match in self.filter_data:
                if match['sound'] == entry[1]:
                    update_sound(match['start_idx'], entry[1])
        else:
            match = next((d for d in self.filter_data if d['rarity'] == entry[0] and d['sound'] == entry[1] and d['context'] == entry[2]), None)
            if not match:
                messagebox.showerror("Error", "Could not match entry.")
                return
            update_sound(match['start_idx'], entry[1])

        try:
            with open(self.filter_path, 'w', encoding='utf-8') as f:
                f.writelines(self.lines)
            messagebox.showinfo("Success", f"Updated sound(s) to {new_filename}.")
            self.refresh_filter_data()  # Refresh view without reloading the file
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update filter: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = FilterSoundEditor(root)
    root.mainloop()
