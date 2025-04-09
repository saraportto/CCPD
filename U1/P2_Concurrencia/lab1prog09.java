import java.util.ArrayList;
import java.util.List;

// Clase HILO
class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Mi nombre es: " + this.getName());
        System.out.println("Finalizado el proceso " + this.getName());
    }
}

// Clase MAIN
public class lab1prog09 {

    public static void main(String[] args) {
        final int NUMERO_THREADS = 32;
        List<Thread> threadList = new ArrayList<>(NUMERO_THREADS); // Lista dinámica de threads

        // Create and start threads
        for (int i = 1; i <= NUMERO_THREADS; ++i) {
            MyThread myThread = new MyThread();
            myThread.start();
            threadList.add(myThread); // Es como un append de un nuevo hilo
        }

        // Check if threads are alive and join
        for (Thread t : threadList) { // For element in threadList
            
            try {
                System.out.println("Thread " + t.getName() + " is alive: " + t.isAlive());
                t.join();
                System.out.println("Thread " + t.getName() + " has completed.");

            } catch (InterruptedException e) {
                System.out.println("Thread " + t.getName() + " interrupted.");
            }
        }

        System.out.println("El programa ha terminado");
    }
}