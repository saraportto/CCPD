import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

// NODO tipo INT
class NodeInt {
    int value;
    NodeInt next;

    public NodeInt(int value) {
        this.value = value; // Valor del nodo
        this.next = null; // Nodo siguiente
    }
}

// PILA SINCRONIZADA
class SynchronizedStack {
    private NodeInt top; // Nodo superior de la pila
    private final ReentrantLock lock = new ReentrantLock(); // Lock reentrante
    private final Condition notEmptyCondition = lock.newCondition(); // Condición de no vacío

    // Constructor
    public SynchronizedStack() {
        this.top = null; // Inicializa la pila
    }

    // PUSH - Añade item arriba de la pila
    public void push(int value) {

        // LOCK
        lock.lock();
        try {
            NodeInt newNode = new NodeInt(value); // Nuevo nodo con el valor a añadir
            newNode.next = top; // Nuevo nodo apunta al antiguo top
            top = newNode; // Actualiza top para que ahora apunte al nuevo nodo 
            notEmptyCondition.signalAll(); // SIGNAL posibles hilos en espera (por pop y peek)
        
        } finally {
            lock.unlock(); // UNLOCK
        }
    }

    // POP - Elimina y devuelve el item de arriba de la pila
    public int pop() throws InterruptedException {

        // LOCK 
        lock.lock();
        try {
            while (top == null) { // Si la pila está vacía
                notEmptyCondition.await(); // WAIT
            }

            int value = top.value; // Guarda valor del nodo superior
            top = top.next; // Actualiza top para que apunte al siguiente nodo (el que estaba justo debajo)
            return value; // Devuelve el valor del nodo eliminado

        } finally {
            lock.unlock(); // UNLOCK
        }
    }

    // PEEK - Devuelve el item de arriba de a pila, sin eliminarlo
    public int peek() throws InterruptedException {

        // LOCK
        lock.lock();
        try {
            while (top == null) { // Guarda valor del nodo superior
                notEmptyCondition.await(); // WAIT
            }
            return top.value; // Devuelve el valor del nodo superior

        } finally {
            lock.unlock(); // UNLOCK
        }
    }

    // isEMPTY - Compueba si la pila está vacía
    public boolean isEmpty() {

        // LOCK
        lock.lock();
        try {
            return top == null; // Devuelve si la pila está vacía

        } finally {
            lock.unlock(); // UNLOCK
        }
    }
}

public class lab3prob07 {

   public static void main(String[] args) {
      SynchronizedStack stack = new SynchronizedStack(); // Pila sincronizada
     
      
      int numThreads = 2; // DOS hilos para push y DOS hilos para pop
      int numElements = 10;//Cada hilo hace push/pop de 10 elementos
      
      startPushThreads(stack, numThreads, numElements); // Lanza hilos PUSH
      startPopThreads(stack, numThreads, numElements); // Lanza hilos POP
   }

    // Crea e inicializa hilos que hagan POP de elementos de la pila
    private static void startPopThreads(SynchronizedStack stack, int numThreads, int numElements) {
        List<Thread> threads = new ArrayList<>(); // Lista de hilos

        for (int i = 0; i < numThreads; i++) { // Por cada hilo de los 2, crea un hilo
            Thread thread = new Thread(() -> { // LO QUE HACE cada HILO

                for (int j = 0; j < numElements; j++) { // Hacer POP de 10 elementos

                    // POP de elemento de la pila
                    try {
                        int poppedValue = stack.pop(); // POP
                        System.out.println("Thread " + Thread.currentThread().getName() + " popped: " + poppedValue);
                        Thread.sleep(100); // Simulate some delay

                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                }
            });

            threads.add(thread); // Añade hilo a la lista
            thread.setName("PopThread-" + i); // Nombre hilo
            thread.start(); // Inicializa hilo
        }
    }

    // Crea e inicializa hilos que hagan PUSH de elementos de la pila
    private static void startPushThreads(SynchronizedStack stack, int numThreads, int numElements) {
        List<Thread> threads = new ArrayList<>(); // Lista de hilos

        for (int i = 0; i < numThreads; i++) { // Por cada hilos de los 2, crea un hilo
            int threadNum = i; // For lambda expression
            Thread thread = new Thread(() -> { // LO QUE HACE cada HILO

                for (int j = 0; j < numElements; j++) { // Hacer PUSH de 10 elementos

                    // PUSH 
                    stack.push(threadNum * numElements + j);
                    System.out.println("Thread " + Thread.currentThread().getName() + " pushing: " + (threadNum * numElements + j));
                    
                    try {
                        Thread.sleep(100); // Simulate some delay
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });

            threads.add(thread); // Añade el hilo a la lisat
            thread.setName("PushThread-" + i); // Nombre del hilo
            thread.start(); // Inicializa el hilo
        }
    }
}