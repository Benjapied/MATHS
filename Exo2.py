import tkinter as tk
from tkinter import ttk
import Exo1 as e1
import matplotlib.pyplot as plt

class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.tangent = 0  # Initialiser la tangente à 0 par défaut

class PointApp:
    def __init__(self, master):
        self.master = master
        master.title("Point Creator")
        master.geometry("1200x700")  # Augmentation de la taille de la fenêtre globale
        self.symetrie = False

        # Cadre principal
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Cadre pour la grille
        self.grid_frame = tk.Frame(self.main_frame)
        self.grid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Grille
        self.canvas = tk.Canvas(self.grid_frame, width=600, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Cadre pour les coordonnées des points
        self.coordinates_frame = tk.Frame(self.main_frame, bg="lightgray")
        self.coordinates_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.points_list_label = tk.Label(self.coordinates_frame, text="Points:", font=("Arial", 12), bg="lightgray")
        self.points_list_label.pack()

        self.points_listbox = tk.Listbox(self.coordinates_frame, width=20, height=20, font=("Arial", 10))
        self.points_listbox.pack(fill=tk.BOTH, expand=True)

        # Cadre pour les sliders
        self.sliders_frame = tk.Frame(self.coordinates_frame,width=20, height=20)
        self.sliders_frame.pack(side=tk.LEFT, fill=tk.X,expand=True)

        self.points = []
        self.tangents = []  # Liste pour stocker les valeurs des tangentes
        self.sliders = []

        self.draw_cartesian_coordinates()

        self.checkbox_var = tk.BooleanVar()
        self.checkbox_var.set(False)  # Valeur initiale de la case à cocher
        self.checkbox = ttk.Checkbutton(master, text="Symétrie", variable=self.checkbox_var, command=self.checkbox_callback)
        self.checkbox.pack()


        self.canvas.bind("<Button-1>", self.add_point)

        self.confirm_button = tk.Button(self.main_frame, text="Confirmer", command=self.confirm_points)
        self.confirm_button.pack(side=tk.BOTTOM)

    def draw_cartesian_coordinates(self):
        self.canvas.update_idletasks()  # assure que la fenêtre est correctement affichée avant de dessiner la grille
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width // 2
        center_y = height // 2

        # Axe des x
        self.canvas.create_line(0, center_y, width, center_y, fill="black")  
        for x in range(center_x, width, 20):
            self.canvas.create_line(x, 0, x, height, fill="lightgray", dash=(2, 2))

        # Axe des y
        self.canvas.create_line(center_x, 0, center_x, height, fill="black")  
        for y in range(center_y, height, 20):
            self.canvas.create_line(0, y, width, y, fill="lightgray", dash=(2, 2))

    def add_point(self, event):
        if len(self.points) < 10:
            x, y = event.x, event.y
            name = chr(ord('A') + len(self.points))  # Nommer les points de A à J
            point = Point(name, x, 700 - y)
            self.points.append(point)
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")
            self.points_listbox.insert(tk.END, f"{point.name}: ({point.x}, {700 - point.y})")
            self.create_slider(name)  # Créer le slider correspondant au point
        else:
            tk.messagebox.showwarning("Avertissement", "Le nombre maximal de points a été atteint (10).")

    def create_slider(self, name):
        slider_frame = tk.Frame(self.sliders_frame)
        slider_frame.pack()

        label = tk.Label(slider_frame)
        label.pack(side=tk.LEFT)

        slider = ttk.Scale(slider_frame, from_=-5, to=5, orient="horizontal", command=lambda value, n=name, label=label: self.update_tangent(value, n, label))
        slider.set(0)
        slider.pack(side=tk.LEFT)

        label_value = tk.Label(slider_frame, text=f"{name}")
        label_value.pack(side=tk.LEFT)

        self.sliders.append((name, slider, label_value))

    def update_tangent(self, value, name, label):
        label.config(text=int(float(value)))
        for point in self.points:
            if point.name == name:
                point.tangent = int(float(value))
                break

    def confirm_points(self):
        self.master.destroy()

    def get_points_coordinates(self):
        x_coordinates = [point.x for point in self.points]
        y_coordinates = [point.y for point in self.points]

        if self.symetrie:
            max_x = max(x_coordinates)
            for i in range(len(x_coordinates)):
                x_coordinates.append(max_x - (x_coordinates[i] - max_x))
                y_coordinates.append(y_coordinates[i])

        return x_coordinates, y_coordinates

    def get_points_tangents(self):
        tangents = [point.tangent for point in self.points]

        if self.symetrie:
            # Créer une nouvelle liste pour stocker les tangentes symétriques
            symmetrical_tangents = []
            for tangent in tangents:
                symmetrical_tangents.append(-tangent)
            # Concaténer les deux listes de tangentes
            tangents += symmetrical_tangents

        return tangents
    
    def checkbox_callback(self):
        if self.checkbox_var.get():
            self.symetrie = True
            print(self.symetrie)
        else:
            self.symetrie = False
            print(self.symetrie)

if __name__ == "__main__":
    
    root = tk.Tk()
    app = PointApp(root)
    root.mainloop()

    x_coords, y_coords = app.get_points_coordinates()
    tangents = app.get_points_tangents()

    print("Liste des abscisses:", x_coords)
    print("Liste des ordonnées:", y_coords)
    print("Liste des tangentes:", tangents)

    list1, list2 = e1.MakeHermite(x_coords,y_coords,tangents,100)

    plt.axis((0, 1200, 0, 700))
    plt.scatter(x_coords,y_coords)
    plt.plot(list1, list2)
    plt.show()
