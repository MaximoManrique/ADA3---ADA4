

class Nodo:
   
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
       
        return f"Nodo(data={self.data})"

class LinkedList:
   
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def is_empty(self):
        
        return self.head is None

    def __len__(self):
        
        return self.count

   

    def insert_at_start(self, data):
        """Inserta un nuevo nodo al inicio (head)."""
        nuevo_nodo = Nodo(data)
        if self.is_empty():
            self.head = nuevo_nodo
            self.tail = nuevo_nodo
        else:
            nuevo_nodo.next = self.head
            self.head.prev = nuevo_nodo
            self.head = nuevo_nodo
        self.count += 1

    def insert_at_end(self, data):
        """Inserta un nuevo nodo al final (tail)."""
        nuevo_nodo = Nodo(data)
        if self.is_empty():
            self.head = nuevo_nodo
            self.tail = nuevo_nodo
        else:
            nuevo_nodo.prev = self.tail
            self.tail.next = nuevo_nodo
            self.tail = nuevo_nodo
        self.count += 1

    # --- MÉTODOS DE BORRADO ---

    def remove_from_start(self):
        """Borra el nodo inicial (head) y devuelve su dato."""
        if self.is_empty():
            return None # O lanzar un error
        
        data = self.head.data
        if self.head == self.tail: # Si solo hay un nodo
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        
        self.count -= 1
        return data

    def remove_from_end(self):
        """Borra el nodo final (tail) y devuelve su dato."""
        if self.is_empty():
            return None
            
        data = self.tail.data
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            
        self.count -= 1
        return data

    def remove_by_value(self, data_borrar):
        """
        (¡NUEVO!)
        Busca un dato en la lista y borra su primera aparición.
        Devuelve True si lo borró, False si no lo encontró.
        """
        actual = self.head
        while actual:
            if actual.data == data_borrar:
                # --- Encontramos el nodo, ahora a re-enlazar ---
                
                # 1. Si no es la cabeza, enlaza el anterior con el siguiente
                if actual.prev:
                    actual.prev.next = actual.next
                else:
                    # Si es la cabeza, actualiza self.head
                    self.head = actual.next

                # 2. Si no es la cola, enlaza el siguiente con el anterior
                if actual.next:
                    actual.next.prev = actual.prev
                else:
                    # Si es la cola, actualiza self.tail
                    self.tail = actual.prev
                    
                self.count -= 1
                return True # Nodo borrado
            
            actual = actual.next
        return False # No se encontró

    # --- MÉTODOS DE BÚSQUEDA Y RECORRIDO ---

    def find(self, data_buscada):
        """
        (¡NUEVO!)
        Busca un dato en la lista.
        Devuelve el objeto Nodo si lo encuentra, o None si no.
        """
        actual = self.head
        while actual:
            if actual.data == data_buscada:
                return actual # Devuelve el nodo completo
            actual = actual.next
        return None

    def peek_start(self):
        """Muestra el dato del inicio sin borrarlo."""
        return self.head.data if self.head else None
        
    def peek_end(self):
        """Muestra el dato del final sin borrarlo."""
        return self.tail.data if self.tail else None

    def __iter__(self):
        
        actual = self.head
        while actual:
            yield actual.data 
            actual = actual.next



class Stack:
   
  
    def __init__(self):
        self._lista_interna = LinkedList()

    def push(self, item):
        self._lista_interna.insert_at_start(item)

    def pop(self):
        return self._lista_interna.remove_from_start()

    def peek(self):
        return self._lista_interna.peek_start()

    def is_empty(self):
        return self._lista_interna.is_empty()

    def size(self):
        return len(self._lista_interna)


class Queue:
    
    def __init__(self):
        self._lista_interna = LinkedList()

    def enqueue(self, item):
        self._lista_interna.insert_at_end(item)

    def dequeue(self):
        return self._lista_interna.remove_from_start()

    def front(self):
        return self._lista_interna.peek_start()

    def is_empty(self):
        return self._lista_interna.is_empty()

    def size(self):
        return len(self._lista_interna)