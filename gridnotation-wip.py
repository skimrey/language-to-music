import tkinter as tk

# Set up the GUI
root = tk.Tk()
root.title("Music Input GUI")

# Create the grid
grid = tk.Canvas(root, width=600, height=400)
grid.pack()

# Configure the grid to fill the entire GUI width
grid.configure(width=root.width)


# Define the grid dimensions (semitones x eighth notes)
semitones = 12
eighth_notes = 4

# Create the grid lines
for i in range(semitones):
    grid.create_line(i * 50, 0, i * 50, 400)  # horizontal lines
for j in range(eighth_notes):
    grid.create_line(0, j * 50, 600, j * 50)  # vertical lines

# Define the dot class
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = "black"

# Create a list to store the dots
dots = []

# Define the dot placement function
def place_dot(event):
    x = event.x // 50
    y = event.y // 50
    dot = Dot(x, y)
    dots.append(dot)
    grid.create_oval(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill=dot.color)

# Bind the dot placement function to mouse clicks
grid.bind("<Button-1>", place_dot)

# Define the Convert to MIDI button
button = tk.Button(root, text="Convert to MIDI", command=convert_to_midi)
button.pack()

# Define the convert_to_midi function
def convert_to_midi():
    # TO DO: implement MIDI conversion logic here
    # For now, just print the dot placements
    print(dots)

root.mainloop()