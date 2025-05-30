from tkinter import Tk, filedialog, Text, Button, Label, Toplevel, Frame, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
import io
import base64
import webbrowser

class DilutionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dilution Calculator + Image Annotator")
        self.image_data = []
        self.create_widgets()

    def create_widgets(self):
        input_frame = Frame(self.root)
        input_frame.pack(pady=10)

        Label(input_frame, text="Reagent name").grid(row=0, column=0, padx=5)
        Label(input_frame, text="Stock Conc (μM)").grid(row=0, column=1, padx=5)
        Label(input_frame, text="Final Volume (μL)").grid(row=0, column=2, padx=5)
        Label(input_frame, text="Desired Conc (μM)").grid(row=0, column=3, padx=5)

        self.reagent_entry = Text(input_frame, width=15, height=2)
        self.stock_entry = Text(input_frame, width=15, height=2)
        self.volume_entry = Text(input_frame, width=15, height=2)
        self.desired_entry = Text(input_frame, width=15, height=2)

        self.reagent_entry.grid(row=1, column=0, padx=5)
        self.stock_entry.grid(row=1, column=1, padx=5)
        self.volume_entry.grid(row=1, column=2, padx=5)
        self.desired_entry.grid(row=1, column=3, padx=5)

        Button(input_frame, text="Add & Compute", command=self.add_and_compute).grid(row=1, column=4, padx=10)

        self.tree = ttk.Treeview(
            self.root,
            columns=("Reagent", "Stock Conc (μM)", "Final Volume (μL)", "Desired Conc (μM)", "Volume to Add (μL)"),
            show="headings"
        )

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(pady=10, fill='x', padx=10)

        Button(self.root, text="Add Image", command=self.open_image_popup).pack(pady=5)
        Button(self.root, text="Create HTML Page", command=self.create_html_page).pack(pady=10)

    def add_and_compute(self):
        try:
            stock_conc = float(self.stock_entry.get("1.0", "end-1c").strip())
            final_vol = float(self.volume_entry.get("1.0", "end-1c").strip())
            desired_conc = float(self.desired_entry.get("1.0", "end-1c").strip())
            reagent = self.reagent_entry.get("1.0", "end-1c").strip()

            if not reagent or stock_conc <= 0 or final_vol <= 0 or desired_conc <= 0:
                raise ValueError

            volume_to_add = (desired_conc * final_vol) / stock_conc
            self.tree.insert("", "end", values=(reagent, stock_conc, final_vol, desired_conc, round(volume_to_add, 2)))

        except Exception:
            self.show_error_popup("All fields must be filled correctly with numeric values.")
        finally:
            self.clear_fields()

    def show_error_popup(self, message):
        messagebox.showerror("Input Error", message)

    def clear_fields(self):
        self.reagent_entry.delete("1.0", "end")
        self.stock_entry.delete("1.0", "end")
        self.volume_entry.delete("1.0", "end")
        self.desired_entry.delete("1.0", "end")

    def open_image_popup(self):
        popup = Toplevel(self.root)
        popup.title("Add Image")
        preview_label = Label(popup)
        preview_label.pack()

        Label(popup, text="Caption:").pack()
        caption_entry = Text(popup, height=5, width=50)
        caption_entry.pack(pady=5)

        image_container = {"img_base64": None, "thumbnail": None}

        def paste_image_from_clipboard(event=None):
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                img.thumbnail((300, 300))
                img_buffer = io.BytesIO()
                img.save(img_buffer, format="PNG")
                img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                image_container["img_base64"] = img_base64

                # Update preview
                photo = ImageTk.PhotoImage(img)
                preview_label.configure(image=photo)
                preview_label.image = photo
            else:
                messagebox.showerror("No Image", "Clipboard does not contain an image.")

        def add_image_to_notes():
            if image_container["img_base64"]:
                caption = caption_entry.get("1.0", "end-1c").strip()
                self.image_data.append((image_container["img_base64"], caption))
                self.display_image_thumbnail(image_container["img_base64"], caption)
                popup.destroy()
            else:
                messagebox.showwarning("No Image", "No image has been pasted.")

        Label(popup, text="Paste image (Ctrl+V)", font=("Arial", 10, "italic")).pack(pady=5)
        Button(popup, text="Add to Notes", command=add_image_to_notes).pack(pady=5)

        popup.bind("<Control-v>", paste_image_from_clipboard)

    def display_image_thumbnail(self, img_base64, caption):
        img_data = base64.b64decode(img_base64)
        image = Image.open(io.BytesIO(img_data))
        image.thumbnail((150, 150))
        photo = ImageTk.PhotoImage(image)

        container = Frame(self.root)
        container.pack(side='top', anchor="w", pady=5)

        img_label = Label(container, image=photo)
        img_label.image = photo
        img_label.pack(side="left")

        caption_label = Label(container, text=caption, wraplength=200)
        caption_label.pack(side="left", padx=10)

        def remove_image():
            self.image_data.remove((img_base64, caption))
            container.destroy()

        Button(container, text="Remove", command=remove_image, fg="red").pack(side="left", padx=10)

    def create_html_page(self):
        html = """<html><head><title>Dilution Results</title></head><body>
        <h2>Dilution Table</h2>
        <table border="1" cellpadding="5" cellspacing="0">
        <tr><th>Reagent</th><th>Stock Conc (μM)</th><th>Final Volume (μL)</th><th>Desired Conc (μM)</th><th>Volume to Add (μL)</th></tr>
        """
        for row in self.tree.get_children():
            values = self.tree.item(row)['values']
            html += "<tr>" + "".join(f"<td>{v}</td>" for v in values) + "</tr>"

        html += "</table><h2>Images & Notes</h2>"

        for img_base64, caption in self.image_data:
            html += f'<div style="margin-bottom: 20px;"><img src="data:image/png;base64,{img_base64}" height="200"><br><p>{caption}</p></div>'

        html += "</body></html>"

        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
            webbrowser.open(file_path)

if __name__ == "__main__":
    root = Tk()
    app = DilutionApp(root)
    root.mainloop()
