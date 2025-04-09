import java.util.concurrent.locks.ReentrantLock;

// Clase LISTA DOBLEMENTE ENLAZADA SINCRONIZADA
class SynchronizedDoublyLinkedList {
    private Node head = null;
    private Node tail = null;
    private final ReentrantLock lock = new ReentrantLock();

    // Clase NODO
    private static class Node {
        int value;
        Node next;
        Node prev;

        Node(int value) {
            this.value = value; // Valor del nodo
            this.next = null; // Puntero al siguiente nodo
            this.prev = null; // Puntero al nodo anterior
        }
    }

    // AÑADE item al final de la lista
    public void addLast(int value) {

        // LOCK
        lock.lock();
        try {
            Node newNode = new Node(value); // Nuevo nodo con el valor proporcionado
            
            // Si la lista está vacía
            if (tail == null) {
                head = tail = newNode; // Inicializa head y tail con el nuevo nodo 
            
            // Si la lista contiene elementos
            } else {
                tail.next = newNode; // El antiguo tail apunta delante al nuev nodo
                newNode.prev = tail; // El nuevo nodo apunta atrás al antiguo tail
                tail = newNode; // Actualiza el tail para que sea el nuevo nodo
            }

        } finally {
            lock.unlock(); // UNLOCK
        }
    }

    // ELIMINA el primer item de la lista
    public void removeFirst() {

        // LOCK
        lock.lock();
        try {

            // Si la lista no está vacía
            if (head != null) {
                head = head.next; // Mueve la cabeza al siguiente nodo
                // Si hay cabeza
                if (head != null) {
                    head.prev = null; // Elimina la referencia al nodo anterior

                // Si no hay cabeza
                } else {
                    tail = null; // Lista vacía --> actualiza tail a null
                }
            }

        } finally {
            lock.unlock(); // UNLOCK
        }
    }

    // IMPRIME la lista
    public void printList() {

        // LOCK
        lock.lock();
        try {
            Node current = head; // Nodo actual --> cabeza

            // RECORRE la lista mientras haya nodos
            while (current != null) {
                System.out.print(current.value + " ");
                current = current.next; // Se mueve al siguiente nodo
            }

            System.out.println(); // New line after printing the list

        } finally {
            lock.unlock(); // UNLOCK
        }
    }
}

// Clase PRINCIPAL
public class lab3prob09 {
    public static void main(String[] args) {
        SynchronizedDoublyLinkedList list = new SynchronizedDoublyLinkedList(); // Lista doblemente enlazada sincronizada

        int numThreads = 2; // nº de hilos que añadirán/eliminarán elementos a la lista
        int numElements = 5; // cada hilo añadirá 5 elementos

        startAddLastThreads(list, numThreads, numElements);

        // Wait a bit for all add operations to finish (not the best practice, but simple)
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Removing elements and printing the list in main thread to avoid concurrency issues
        list.removeFirst(); 
        list.printList();
    }

    // Crea e inicializa hilos que añaden elementos al final de la lista
    private static void startAddLastThreads(SynchronizedDoublyLinkedList list, int numThreads, int numElements) {
        for (int i = 0; i < numThreads; i++) { // Por cada hilo de los 2, crea un hilo
            new Thread(() -> {
                for (int j = 0; j < numElements; j++) {
                    list.addLast(j); // Cada hilo, añade 5 elementos a la lista
                }
            }).start();
        }
    }
}