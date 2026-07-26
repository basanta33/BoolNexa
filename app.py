import tkinter as tk

class Gate:
    def __init__(self, canvas, gate_type, x, y):
        self.canvas = canvas
        self.gate_type = gate_type
        self.x, self.y = x, y
        self.items = []
        self.draw()

    def draw(self):
        for item in self.items:
            self.canvas.delete(item)
        self.items = []
        
        w, h = 80, 60
        # Draw ANSI-compliant logic symbols
        if self.gate_type == "AND":
            arc = self.canvas.create_arc(self.x, self.y, self.x+w, self.y+h, start=270, extent=180, style=tk.ARC, width=2)
            line = self.canvas.create_line(self.x+w/2, self.y, self.x+w/2, self.y+h, width=2)
            self.items = [arc, line]
        else:
            rect = self.canvas.create_rectangle(self.x, self.y, self.x+w, self.y+h, fill="white", width=2)
            text = self.canvas.create_text(self.x+w/2, self.y+h/2, text=self.gate_type)
            self.items = [rect, text]

        for item in self.items:
            self.canvas.tag_bind(item, "<B1-Motion>", self.drag)
            self.canvas.tag_bind(item, "<Button-3>", self.show_menu)

    def drag(self, event):
        dx = event.x - (self.x + 40)
        dy = event.y - (self.y + 30)
        self.x += dx
        self.y += dy
        for item in self.items:
            self.canvas.move(item, dx, dy)

    def show_menu(self, event):
        menu = tk.Menu(self.canvas, tearoff=0)
        menu.add_command(label="Rotate Clockwise", command=lambda: print(f"Rotating {self.gate_type}"))
        menu.tk_popup(event.x_root, event.y_root)

class SchematicDesigner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Professional Schematic Designer")
        self.geometry("1200x800")
        
        self.toolbox = tk.Frame(self, width=100, bg="#2c3e50")
        self.toolbox.pack(side="left", fill="y")
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side="right", fill="both", expand=True)
        
        self.ghost = None
        self.offset_x, self.offset_y = 40, 30

        for gate in ["AND", "OR", "NOT"]:
            lbl = tk.Label(self.toolbox, text=gate, bg="#34495e", fg="white", padx=10, pady=10)
            lbl.pack(pady=5, fill="x")
            # Bind the click event to the label
            lbl.bind("<ButtonPress-1>", lambda e, g=gate: self.start_drag(e, g))

    def start_drag(self, event, gate_type):
        # Get mouse position relative to canvas
        x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        
        # Create ghost at the actual mouse position
        self.ghost = self.canvas.create_rectangle(
            x - self.offset_x, y - self.offset_y, 
            x + self.offset_x, y + self.offset_y, 
            fill="gray", stipple="gray50"
        )
        self.canvas.bind("<Motion>", self.move_ghost)
        self.canvas.bind("<ButtonRelease-1>", lambda e: self.drop_gate(e, gate_type))

    def move_ghost(self, event):
        if self.ghost:
            self.canvas.coords(self.ghost, event.x - self.offset_x, event.y - self.offset_y, 
                               event.x + self.offset_x, event.y + self.offset_y)

    def drop_gate(self, event, gate_type):
        if self.ghost:
            self.canvas.delete(self.ghost)
        self.ghost = None
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        Gate(self.canvas, gate_type, event.x - self.offset_x, event.y - self.offset_y)

if __name__ == "__main__":
    app = SchematicDesigner()
    app.mainloop()