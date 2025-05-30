from tkinter import Tk, Toplevel, Text, Button, Label, Frame, messagebox
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk, ImageGrab
import io
import base64
import os
from datetime import datetime

class DilutionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dilution Calculator + Image Annotator")
        self.image_data = []  # Store image base64 and captions
        self.dilution_data = []  # Store dilution data
        self.create_widgets()

    def create_widgets(self):
        # Dilution Input Frame
        input_frame = Frame(self.root)
        input_frame.pack(pady=10)

        # Labels and Entries for Dilution Calculation
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

        # Treeview for displaying dilution data
        self.tree = ttk.Treeview(self.root, columns=("Reagent", "Stock Conc (μM)", "Final Volume (μL)", "Desired Conc (μM)", "Volume to Add (μL)"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(pady=10, fill='x', padx=10)

        # Buttons for adding image, creating HTML, clearing fields, and quitting
        Button(self.root, text="Add Image", command=self.open_image_popup).pack(pady=5)
        Button(self.root, text="Create HTML Page", command=self.create_html_page).pack(pady=5)
        Button(self.root, text="Clear All", command=self.clear_all).pack(pady=5)
        Button(self.root, text="Quit", command=self.quit_app).pack(pady=5)

    def add_and_compute(self):
        try:
            stock_conc = float(self.stock_entry.get("1.0", "end-1c").strip())
            final_vol = float(self.volume_entry.get("1.0", "end-1c").strip())
            desired_conc = float(self.desired_entry.get("1.0", "end-1c").strip())
            reagent = self.reagent_entry.get("1.0", "end-1c").strip()

            if stock_conc <= 0 or final_vol <= 0 or desired_conc <= 0 or not reagent:
                raise ValueError

            volume_to_add = (desired_conc * final_vol) / stock_conc
            row = (reagent, stock_conc, final_vol, desired_conc, round(volume_to_add, 2))
            self.dilution_data.append(row)
            self.tree.insert("", "end", values=row)
        except:
            self.show_error_popup("Please ensure all fields are filled with valid numeric values.")
        finally:
            self.clear_fields()

    def show_error_popup(self, message):
        messagebox.showerror("Input Error", message)

    def clear_fields(self):
        for field in [self.reagent_entry, self.stock_entry, self.volume_entry, self.desired_entry]:
            field.delete("1.0", "end")

    def clear_all(self):
        # Clear the treeview and reset dilution data
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.dilution_data = []

        # Clear the image previews and reset image data
        for widget in self.root.winfo_children():
            # If the widget is a Frame that contains image thumbnails and captions, destroy it
            if isinstance(widget, Frame) and widget not in [self.tree, self.root.winfo_children()[-1]]:
                widget.destroy()  # Remove image thumbnails and captions

        self.image_data = []  # Clear the image data list
        self.clear_fields()

    def quit_app(self):
        self.root.quit()

    def open_image_popup(self):
        popup = Toplevel(self.root)
        popup.title("Add Image")

        Label(popup, text="Paste image with Ctrl+V or drag and drop below:").pack(pady=5)

        drop_frame = Frame(popup, width=300, height=200, bg="lightgrey")
        drop_frame.pack(pady=5)
        drop_frame.pack_propagate(False)

        image_preview_label = Label(drop_frame)
        image_preview_label.pack()

        def handle_image(img):
            if img:
                img.thumbnail((200, 200))
                img_buffer = io.BytesIO()
                img.save(img_buffer, format="PNG")
                img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

                preview_img = ImageTk.PhotoImage(img)
                image_preview_label.configure(image=preview_img)
                image_preview_label.image = preview_img
                popup.image_base64 = img_base64

        def on_paste(event=None):
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                handle_image(img)

        def on_drop(event):
            file_path = event.data.strip('{}')
            if os.path.isfile(file_path):
                try:
                    img = Image.open(file_path)
                    handle_image(img)
                except:
                    messagebox.showerror("Error", "Could not open image.")

        drop_frame.drop_target_register(DND_FILES)
        drop_frame.dnd_bind('<<Drop>>', on_drop)
        popup.bind("<Control-v>", on_paste)

        Label(popup, text="Caption:").pack()
        caption_entry = Text(popup, height=3, width=50)
        caption_entry.pack(pady=5)

        def add_to_main():
            caption = caption_entry.get("1.0", "end-1c").strip()
            if hasattr(popup, 'image_base64'):
                self.image_data.append((popup.image_base64, caption))
                self.display_image_thumbnail(popup.image_base64, caption)
                popup.destroy()
            else:
                messagebox.showwarning("Missing", "No image to add!")

        Button(popup, text="Add to Notes", command=add_to_main).pack(pady=5)

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
        html = ['<html><head><title>Dilution Report</title></head><body>']
        html.append(f'<h2>Dilution Report - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</h2>')

        if self.dilution_data:
            html.append("<h3>Dilution Table</h3><table border='1'><tr><th>Reagent</th><th>Stock Conc (μM)</th><th>Final Volume (μL)</th><th>Desired Conc (μM)</th><th>Volume to Add (μL)</th></tr>")
            for row in self.dilution_data:
                html.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
            html.append("</table>")

        if self.image_data:
            html.append("<h3>Images and Notes</h3>")
            for img_b64, caption in self.image_data:
                html.append(f'<div style="margin:10px 0;"><img src="data:image/png;base64,{img_b64}" style="max-width:300px;"><p>{caption}</p></div>')

        html.append('</body></html>')

        filename = f"dilution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, "w") as f:
            f.write("\n".join(html))
        messagebox.showinfo("HTML Created", f"Report saved as {filename}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = DilutionApp(root)
    root.mainloop()
