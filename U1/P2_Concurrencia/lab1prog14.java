import java.util.concurrent.TimeUnit;
import java.util.Date;
import java.util.ArrayList;
import java.util.List;


// Clase HILO (inseguro)
class UnsafeTask implements Runnable {

    private Date startDate;

    @Override
    public void run() {

        startDate = new Date();

        // Imprime la fecha de inicio del hilo
        System.out.printf("Starting Thread: %s : %s\n", Thread.currentThread().getId(), startDate);
        
        // Espera un tiempo aleatorio
        try {
            TimeUnit.SECONDS.sleep((int) Math.rint(Math.random() * 10));
        
         // Imprime la pila de llamadas si se interrumpe
        } catch (InterruptedException e) {
            e.printStackTrace(); 
        }

        // Imprime la fecha de finalización del hilo
        System.out.printf("Thread Finished: %s : %s\n", Thread.currentThread().getId(), startDate);
    }
}

// Clase MAIN
public class lab1prog14 {
    public static void main(String[] args) {

        UnsafeTask task = new UnsafeTask(); // Crea un objeto de la clase UnsafeTask
        List<Thread> threads = new ArrayList<>(); // Crea una lista de hilos

        // Crea 10 hilos y los inicia
        for (int i = 0; i < 10; i++) {

            Thread thread = new Thread(task);
            thread.start();
            threads.add(thread);

            // Sleep durante dos segundos
            try {
                TimeUnit.SECONDS.sleep(2);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        // Optionally, wait for all threads to finish
        for (Thread thread : threads) {
            try {
                thread.join();

            // Imprime la fecha de finalización del hilo
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}