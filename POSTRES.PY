import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, Scrollbar

class Nodo:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class ListaEnlazada:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def insertar(self, data):
        nuevo_nodo = Nodo(data)
        if self.is_empty():
            self.head = nuevo_nodo
            self.tail = nuevo_nodo
        else:
            nuevo_nodo.prev = self.tail
            self.tail.next = nuevo_nodo
            self.tail = nuevo_nodo

    def borrar(self, data_borrar):
        actual = self.head
        while actual:
            if actual.data == data_borrar:
                if actual.next:
                    actual.next.prev = actual.prev
                else:
                    self.tail = actual.prev

                if actual.prev:
                    actual.prev.next = actual.next
                else:
                    self.head = actual.next
                return True
            actual = actual.next
        return False

    def buscar(self, data_buscada):
        actual = self.head
        while actual:
            if actual.data == data_buscada:
                return actual
            actual = actual.next
        return None
    
    def recorrer_generador(self):
        actual = self.head
        while actual:
            yield actual.data
            actual = actual.next

class Postre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ingredientes = ListaEnlazada()

    def __lt__(self, other):
        return self.nombre.lower() < other.nombre.lower()

class AppRecetario:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Recetas de Postres")
        self.root.geometry("1000x700")
        
        self.recetario = [] 
        
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        tk.Label(main_frame, text="Postres (Arreglo Ordenado)", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=5)
        
        frame_postres = tk.Frame(main_frame)
        frame_postres.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        
        scroll_postres = Scrollbar(frame_postres)
        scroll_postres.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_postres_widget = Listbox(frame_postres, yscrollcommand=scroll_postres.set, exportselection=False)
        self.lista_postres_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_postres.config(command=self.lista_postres_widget.yview)
        
        self.lista_postres_widget.bind("<<ListboxSelect>>", self.mostrar_ingredientes)

        tk.Label(main_frame, text="Ingredientes (Lista Enlazada)", font=("Arial", 14, "bold")).grid(row=0, column=1, pady=5)
        
        frame_ingredientes = tk.Frame(main_frame)
        frame_ingredientes.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        
        scroll_ingredientes = Scrollbar(frame_ingredientes)
        scroll_ingredientes.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_ingredientes_widget = Listbox(frame_ingredientes, yscrollcommand=scroll_ingredientes.set, exportselection=False)
        self.lista_ingredientes_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_ingredientes.config(command=self.lista_ingredientes_widget.yview)

        botones_frame = tk.Frame(root, pady=10)
        botones_frame.pack(fill=tk.X)
        
        btn_alta_p = tk.Button(botones_frame, text="Dar de Alta Postre", command=self.dar_alta_postre)
        btn_alta_p.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        btn_baja_p = tk.Button(botones_frame, text="Dar de Baja Postre", command=self.dar_baja_postre, fg="red")
        btn_baja_p.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        btn_alta_i = tk.Button(botones_frame, text="Añadir Ingrediente", command=self.insertar_ingrediente)
        btn_alta_i.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        btn_baja_i = tk.Button(botones_frame, text="Eliminar Ingrediente", command=self.eliminar_ingrediente, fg="orange")
        btn_baja_i.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def _get_postre_seleccionado(self):
        try:
            indice = self.lista_postres_widget.curselection()[0]
            nombre_postre = self.lista_postres_widget.get(indice)
            for postre in self.recetario:
                if postre.nombre == nombre_postre:
                    return postre
        except IndexError:
            return None

    def _actualizar_lista_postres_widget(self):
        self.lista_postres_widget.delete(0, tk.END)
        self.lista_ingredientes_widget.delete(0, tk.END)
        
        self.recetario.sort() 
        
        for postre in self.recetario:
            self.lista_postres_widget.insert(tk.END, postre.nombre)

    def mostrar_ingredientes(self, event=None):
        self.lista_ingredientes_widget.delete(0, tk.END)
        postre = self._get_postre_seleccionado()
        
        if postre:
            for ingrediente in postre.ingredientes.recorrer_generador():
                self.lista_ingredientes_widget.insert(tk.END, f"  • {ingrediente}")

    def insertar_ingrediente(self):
        postre = self._get_postre_seleccionado()
        if not postre:
            messagebox.showwarning("Error", "Debes seleccionar un postre primero.")
            return

        ingrediente = simpledialog.askstring("Nuevo Ingrediente", f"Añadir ingrediente a '{postre.nombre}':")
        if ingrediente:
            if postre.ingredientes.buscar(ingrediente):
                messagebox.showwarning("Duplicado", f"'{ingrediente}' ya está en la lista.")
            else:
                postre.ingredientes.insertar(ingrediente)
                self.mostrar_ingredientes()

    def eliminar_ingrediente(self):
        postre = self._get_postre_seleccionado()
        if not postre:
            messagebox.showwarning("Error", "Debes seleccionar un postre primero.")
            return

        try:
            indice_ing = self.lista_ingredientes_widget.curselection()[0]
            ingrediente_a_borrar = self.lista_ingredientes_widget.get(indice_ing).strip()[2:]
            
            if messagebox.askyesno("Confirmar", f"¿Eliminar '{ingrediente_a_borrar}' de '{postre.nombre}'?"):
                postre.ingredientes.borrar(ingrediente_a_borrar)
                self.mostrar_ingredientes()
                
        except IndexError:
            messagebox.showwarning("Error", "Debes seleccionar un ingrediente a eliminar.")

    def dar_alta_postre(self):
        nombre = simpledialog.askstring("Nuevo Postre", "Nombre del nuevo postre:")
        if nombre:
            for postre in self.recetario:
                if postre.nombre.lower() == nombre.lower():
                    messagebox.showwarning("Duplicado", "Ese postre ya existe.")
                    return
            
            nuevo_postre = Postre(nombre)
            self.recetario.append(nuevo_postre)
            self._actualizar_lista_postres_widget()
            messagebox.showinfo("Éxito", f"'{nombre}' añadido. Ahora puedes seleccionarlo y añadir ingredientes.")

    def dar_baja_postre(self):
        postre = self._get_postre_seleccionado()
        if not postre:
            messagebox.showwarning("Error", "Tienes que selleccionar uno.")
            return

        if messagebox.askyesno("Confirmar Baja", f"¿Estás seguro de eliminar '{postre.nombre}' y todos sus ingredientes?"):
            self.recetario.remove(postre)
            self._actualizar_lista_postres_widget()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppRecetario(root)
    root.mainloop()