import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;
import java.util.ArrayList;
import java.util.List;


// Clase MAIN
public class lab3prob04 {
    public static void main(String[] args) {
        final int numberOfThreads = 5; 
        ReentrantLock lock = new ReentrantLock(); // Bloqueo reentrante
        List<Thread> threads = new ArrayList<>(); // Array de hios

        // Crea hilos y los añade al array
        for (int i = 1; i <= numberOfThreads; i++) {
            Thread thread = new Thread(new WorkerThread(i, numberOfThreads, lock));
            threads.add(thread);
        }

        // Inicializa los hilos en orden inverso
        for (int i = numberOfThreads - 1; i >= 0; i--) {
            threads.get(i).start();
        }

        // Señaliza al primer hilo para que empiece
        lock.lock(); // Bloquea
        try {
            if (numberOfThreads > 0) { // Si hay hilos
                WorkerThread.getCondition(numberOfThreads).signal(); // Señaliza al último hilo
            }
        } finally {
            lock.unlock(); // Desbloquea
        }

        // Espera a que todos los hilos terminen
        for (Thread thread : threads) {
            try {
                thread.join(); // Join
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        System.out.println("All threads have executed.");
    }
}


// Clase WORKERTHREAD
class WorkerThread implements Runnable {
    private final int threadId; // ID del hilo actual
    private static ReentrantLock lock; // bloqueo reentrante
    private static Condition[] conditions; // array de condiciones
    private static int currentMaxId; // ID del hilo que tiene permiso para ejecutar

    public WorkerThread(int id, int maxId, ReentrantLock lock) {
        this.threadId = id;
        currentMaxId = maxId;
        WorkerThread.lock = lock; // Se le asigna el bloqueo que se pasa en main

        // UNA CONDICIÓN POR CADA HILO
        if (conditions == null) {  // Si no se han inicializado las condiciones
            conditions = new Condition[maxId + 1]; // Se crea un array de condiciones
            for (int i = 1; i <= maxId; i++) { 
                conditions[i] = lock.newCondition(); // Se asigna una condicion a cada hilo para el lock
            }
        }
    }

    // Getter para condiciones
    public static Condition getCondition(int index) {
        return conditions[index];
    }

    // Método run
    @Override
    public void run() {
        lock.lock(); // Bloquea

        // TRY
        try {
            // Mientras no sea el turno del hilo actual
            while (threadId != currentMaxId) {
                conditions[threadId].await();  // ESPERAR (no es el turno)
            }
            // SECCIÓN CRÍTICA
            System.out.println("Thread with ID "  + threadId + " entering critical section.");
            Thread.sleep(1000); // Simulate work
            System.out.println("Thread with ID "  + threadId + " leaving critical section.");

            currentMaxId--; // SIGUIENTE hilo (el de un ID menor)

            // NOTIFICA SOOOOOLO al SIGUIENTE HILO
            if (currentMaxId > 0) {
                conditions[currentMaxId].signal(); // Notify the next thread
            }
        
        // CATCH
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();

        // FINALLY
        } finally {
            lock.unlock(); // Desbloquea
        }
    }
}


