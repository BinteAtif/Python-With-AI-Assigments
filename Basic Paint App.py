import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageDraw
import random


class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Paint App")

        # Canvas
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # PIL image (for saving)
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Defaults
        self.current_color = "black"
        self.current_tool = "brush"
        self.current_brush = "pen"
        self.brush_size = 5
        self.start_x, self.start_y = None, None
        self.selected_item = None
        self.item_fonts = {}
        self.default_font = "Arial"
        self.default_font_size = 20

        # Mouse binding
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Toolbar
        toolbar = tk.Frame(root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Palette buttons
        tk.Button(toolbar, text="Colors", command=self.show_colors).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Brushes", command=self.show_brushes).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Shapes", command=self.show_shapes).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Text", command=lambda: self.set_tool("text")).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Emojis", command=self.show_emojis).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Styles", command=self.show_styles).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Move Tool", command=lambda: self.set_tool("move")).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Eraser", command=lambda: self.set_tool("eraser")).pack(side=tk.LEFT)

        tk.Button(toolbar, text="Save", command=self.save_image).pack(side=tk.RIGHT)
        tk.Button(toolbar, text="Don't Save", command=self.exit_without_save).pack(side=tk.RIGHT)

        # Sub-toolbar (palettes)
        self.subtoolbar = tk.Frame(root)
        self.subtoolbar.pack(side=tk.TOP, fill=tk.X)

    # ---------------------- TOOLS ----------------------

    def clear_subtoolbar(self):
        for widget in self.subtoolbar.winfo_children():
            widget.destroy()

    def set_tool(self, tool):
        self.current_tool = tool
        self.selected_item = None

    def set_color(self, color):
        self.current_color = color

    def set_brush(self, brush):
        self.current_tool = "brush"
        self.current_brush = brush
        sizes = {"pen": 2, "pencil": 1, "ink": 4, "oil": 8, "paint": 12}
        self.brush_size = sizes.get(brush, 5)

    def set_emoji(self, emoji):
        self.current_tool = "emoji"
        self.selected_emoji = emoji

    # ---------------------- PALETTES ----------------------

    def show_colors(self):
        self.clear_subtoolbar()
        colors = ["black", "gray", "red", "orange", "yellow", "green",
                  "blue", "purple", "brown", "pink", "cyan", "magenta"]
        for c in colors:
            tk.Button(self.subtoolbar, bg=c, width=2,
                      command=lambda col=c: self.set_color(col)).pack(side=tk.LEFT, padx=1)

    def show_brushes(self):
        self.clear_subtoolbar()
        brushes = ["pen", "pencil", "ink", "oil", "paint"]
        for b in brushes:
            tk.Button(self.subtoolbar, text=b.capitalize(),
                      command=lambda br=b: self.set_brush(br)).pack(side=tk.LEFT, padx=2)
        tk.Label(self.subtoolbar, text="Size:").pack(side=tk.LEFT, padx=5)
        size_slider = tk.Scale(self.subtoolbar, from_=1, to=50, orient=tk.HORIZONTAL,
                               command=lambda val: self.set_brush_size(int(val)), length=100)
        size_slider.set(self.brush_size)
        size_slider.pack(side=tk.LEFT)

    def show_shapes(self):
        self.clear_subtoolbar()
        for shape in ["Rectangle", "Oval", "Line", "Triangle"]:
            tk.Button(self.subtoolbar, text=shape,
                      command=lambda sh=shape.lower(): self.set_tool(sh)).pack(side=tk.LEFT, padx=2)

    def show_emojis(self):
        self.clear_subtoolbar()
        emojis = ["😀", "❤️", "⭐", "🎨", "🐱", "🌸", "🔥", "🍕", "🚀", "🎵"]
        for e in emojis:
            tk.Button(self.subtoolbar, text=e, command=lambda em=e: self.set_emoji(em)).pack(side=tk.LEFT, padx=1)

    def show_styles(self):
        self.clear_subtoolbar()

        # Fill color
        tk.Label(self.subtoolbar, text="Fill Color:").pack(side=tk.LEFT, padx=5)
        for c in ["black", "red", "blue", "green", "purple", "orange", "pink"]:
            tk.Button(self.subtoolbar, bg=c, width=2,
                      command=lambda col=c: self.apply_style("color", col)).pack(side=tk.LEFT)

        # Outline color
        tk.Label(self.subtoolbar, text="Outline:").pack(side=tk.LEFT, padx=5)
        for c in ["black", "red", "blue", "green"]:
            tk.Button(self.subtoolbar, bg=c, width=2,
                      command=lambda col=c: self.apply_style("outline", col)).pack(side=tk.LEFT)

        # Fonts
        tk.Label(self.subtoolbar, text="Font:").pack(side=tk.LEFT, padx=5)
        for f in ["Arial", "Courier", "Times", "Comic Sans MS"]:
            tk.Button(self.subtoolbar, text=f,
                      command=lambda ff=f: self.apply_style("font", ff)).pack(side=tk.LEFT)

        # Font size
        tk.Label(self.subtoolbar, text="Size:").pack(side=tk.LEFT, padx=5)
        size_slider = tk.Scale(self.subtoolbar, from_=8, to=72, orient=tk.HORIZONTAL,
                               command=lambda val: self.apply_style("size", int(val)), length=100)
        size_slider.set(20)
        size_slider.pack(side=tk.LEFT)

    def apply_style(self, style_type, value):
        if self.selected_item:
            tags = self.canvas.gettags(self.selected_item)
            if style_type == "color":
                if "shape" in tags or "text" in tags:
                    self.canvas.itemconfig(self.selected_item, fill=value)
            elif style_type == "outline" and "shape" in tags:
                self.canvas.itemconfig(self.selected_item, outline=value)
            elif style_type == "font" and "text" in tags:
                family, size = self.item_fonts.get(self.selected_item, (self.default_font, self.default_font_size))
                self.item_fonts[self.selected_item] = (value, size)
                self.canvas.itemconfig(self.selected_item, font=(value, size))
            elif style_type == "size" and "text" in tags:
                family, _ = self.item_fonts.get(self.selected_item, (self.default_font, self.default_font_size))
                self.item_fonts[self.selected_item] = (family, value)
                self.canvas.itemconfig(self.selected_item, font=(family, value))
        else:
            # No selection → set defaults
            if style_type == "color":
                self.current_color = value
            elif style_type == "font":
                self.default_font = value
            elif style_type == "size":
                self.default_font_size = value

    def set_brush_size(self, size):
        self.brush_size = size

    # ---------------------- DRAWING ----------------------

    def on_click(self, event):
        self.start_x, self.start_y = event.x, event.y

        if self.current_tool == "text":
            text = simpledialog.askstring("Text", "Enter text:")
            if text:
                item = self.canvas.create_text(event.x, event.y, text=text,
                                               fill=self.current_color,
                                               font=(self.default_font, self.default_font_size),
                                               tags="text")
                self.item_fonts[item] = (self.default_font, self.default_font_size)

        elif self.current_tool == "emoji":
            item = self.canvas.create_text(event.x, event.y, text=self.selected_emoji,
                                           font=(self.default_font, self.default_font_size),
                                           fill=self.current_color, tags="text")
            self.item_fonts[item] = (self.default_font, self.default_font_size)

        elif self.current_tool == "move":
            self.selected_item = self.canvas.find_closest(event.x, event.y)[0]

        elif self.current_tool == "eraser":
            x1, y1 = event.x - self.brush_size, event.y - self.brush_size
            x2, y2 = event.x + self.brush_size, event.y + self.brush_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

    def paint(self, event):
        if self.current_tool == "brush":
            x1, y1 = event.x - self.brush_size, event.y - self.brush_size
            x2, y2 = event.x + self.brush_size, event.y + self.brush_size
            if self.current_brush == "pen":
                self.canvas.create_oval(x1, y1, x2, y2, fill=self.current_color, outline="")
            elif self.current_brush == "pencil":
                jitter = random.randint(-1, 1)
                self.canvas.create_line(event.x, event.y, event.x + jitter, event.y + jitter,
                                        fill=self.current_color, width=1)
            elif self.current_brush == "ink":
                self.canvas.create_oval(x1, y1, x2, y2, fill=self.current_color, outline="")
            elif self.current_brush == "oil":
                for _ in range(3):
                    ox, oy = random.randint(-2, 2), random.randint(-2, 2)
                    self.canvas.create_oval(x1+ox, y1+oy, x2+ox, y2+oy, fill=self.current_color, outline="")
            elif self.current_brush == "paint":
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.current_color, outline="")
        elif self.current_tool == "eraser":
            x1, y1 = event.x - self.brush_size, event.y - self.brush_size
            x2, y2 = event.x + self.brush_size, event.y + self.brush_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")
        elif self.current_tool == "move" and self.selected_item:
            dx, dy = event.x - self.start_x, event.y - self.start_y
            self.canvas.move(self.selected_item, dx, dy)
            self.start_x, self.start_y = event.x, event.y

    def on_release(self, event):
        if self.current_tool in ["rectangle", "oval", "line", "triangle"]:
            if not self.start_x or not self.start_y:
                return
            if self.current_tool == "rectangle":
                self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y,
                                             outline=self.current_color, fill="", width=2, tags="shape")
            elif self.current_tool == "oval":
                self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y,
                                        outline=self.current_color, fill="", width=2, tags="shape")
            elif self.current_tool == "line":
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                        fill=self.current_color, width=2, tags="shape")
            elif self.current_tool == "triangle":
                self.canvas.create_polygon(self.start_x, self.start_y, event.x, event.y,
                                           self.start_x, event.y, outline=self.current_color,
                                           fill="", width=2, tags="shape")

        self.start_x, self.start_y = None, None

    # ---------------------- FILE ----------------------

    def save_image(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if filename:
            self.image.save(filename)
            messagebox.showinfo("Saved", "Image saved successfully!")

    def exit_without_save(self):
        if messagebox.askyesno("Exit", "Exit without saving?"):
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()