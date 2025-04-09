import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.Condition;
import java.util.ArrayList;
import java.util.List;

class SynchronizedQueue {
    private Node head, tail; // Nodo cabeza y cola de la cola
    private final ReentrantLock lock = new ReentrantLock(); // Lock reentrante
    private final Condition notEmpty = lock.newCondition(); // Condición de no vacío

    // Clase NODE
    private static class Node {
        int value; 
        Node next; 
        
        Node(int value) {
            this.value = value; // Valor
            this.next = null; // Puntero al siguiente nodo
        }
    }

    // Constructor
    public SynchronizedQueue() {
        this.head = this.tail = null; // Inicializa la cola --> sin cabeza ni cola
    }

    // ENQUEUE - Añade item al final de la cola
    public void enqueue(int value) {

        // LOCK 
        lock.lock();
        try {
            Node newNode = new Node(value); // Crea nuevo nodo con valor proporcionado
            
            // Si no hay cola (cola vacía)
            if (tail == null) { 
                head = tail = newNode; // Nuevo nodo es cabeza y cola
            
            // Si hay cola
            } else {
                tail.next = newNode; // Se añade el nuevo nodo al final de la cola
                tail = newNode; // Se actualiza la cola para que apunte al nuevo nodo
            }
            notEmpty.signal(); // SIGNAL 

        } finally {
            lock.unlock(); // UNLOCK
        }
    }
    
    // DEQUEUE - Elimina y devuelve el item de la cabeza de la cola
    public int dequeue() throws InterruptedException {

        // LOCK
        lock.lock();
        try {
            while (head == null) { // Mientras la cola esté vacía
                notEmpty.await(); // WAIT
            }

            int value = head.value; // Guarda valor del nodo cabeza actual
            head = head.next; // Mueve la cabeza al siguiente nodo

            if (head == null) { // Si la cola queda vacía
                tail = null; // Actualiza la cola para que sea null
            }
            return value; // Devuelve el valor del pincipio de la cola que hemos quitado

        } finally {
            lock.unlock(); // UNLOCK
        }
    }

    // PEEK - Devuelve el item de la cabeza de la cola, sin eliminarlo
    public int peek() throws InterruptedException {
        lock.lock();
        try {
            while (head == null) { // Mientras la cola esté vacía
                notEmpty.await(); // WAIT
            }
            return head.value; // Devuelve valor de la cabeza de la cola

        } finally {
            lock.unlock(); // UNLOCK
        }
    }

    // isEMPTY - Comprueba si la cola está vacía
    public boolean isEmpty() {
        lock.lock(); // LOCK
        try {
            return head == null; // Devuelve si la cola está vacía

        } finally {
            lock.unlock(); // UNLOCK
        }
    }
}


// Clase MAIN
public class lab3prob08 {
    public static void main(String[] args) {
        SynchronizedQueue queue = new SynchronizedQueue(); // Cola sincronizada
        int numThreads = 2; // nº de hilos que harán queue/dequeue
        int numElements = 10; // cada hilo hará queue/dequeue de 10 elementos

        startEnqueueThreads(queue, numThreads, numElements); // Lanza hilos de encolado
        startDequeueThreads(queue, numThreads, numElements); // Lanza hilos de desencolado
    }

    // Crea e inicializa hilos que hagan ENQUEUE de elementos en la cola
    private static void startEnqueueThreads(SynchronizedQueue queue, int numThreads, int numElements) {
        List<Thread> threads = new ArrayList<>(); // Lista de hilos

        for (int i = 0; i < numThreads; i++) { // Por cada hilo de los 2, crea un hilo
            int threadNum = i; // Para usar en la expresión lambda
            Thread thread = new Thread(() -> { // LO QUE HACE cada HILO

                for (int j = 0; j < numElements; j++) { // Hacer ENQUEUE de 10 elementos

                    // ENQUEUE de elemento en la cola
                    queue.enqueue(threadNum * numElements + j);
                    System.out.println("Thread " + threadNum + " enqueued: " + (threadNum * numElements + j));
                    
                    try {
                        Thread.sleep(100); // Simula un pequeño retraso
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });

            threads.add(thread); // Añade el hilo a la lista
            thread.start(); // Inicializa el hilo
        }
    }

    // Crea e inicializa hilos que hagan DEQUEUE de elementos de la cola
    private static void startDequeueThreads(SynchronizedQueue queue, int numThreads, int numElements) {
        List<Thread> threads = new ArrayList<>(); // Lista de hilos

        for (int i = 0; i < numThreads; i++) { // Por cada hilo de los 2, crea un hilo
            Thread thread = new Thread(() -> { // LO QUE HACE cada HILO

                for (int j = 0; j < numElements; j++) { // Hacer DEQUEUE de 10 elementos

                    // DEQUEUE de elemento de la cola
                    try {
                        int value = queue.dequeue(); // DEQUEUE
                        System.out.println(Thread.currentThread().getName() + " dequeued: " + value);
                        Thread.sleep(100); // Simula un pequeño retraso

                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });

            threads.add(thread); // Añade el hilo a la lista
            thread.start(); // Inicializa el hilo
        }
    }
}