import java.util.Random;

// Clase HILO
class NewThread implements Runnable {

    String name;
    Thread t;
    Random rand = new Random();

    NewThread(String threadName) {
        name = threadName;
        t = new Thread(this, name);
        System.out.println("New thread created: " + t);
    }

    public void startThread() {
        t.start();
    }

    public void run() {
        // Simulate some CPU expensive task
        for (int i = 0; i < 1000000000; i++) {
            rand.nextInt();
        }
        System.out.println("[" + Thread.currentThread().getName() + "] finished!");
    }
}

// Clase MAIN
class lab1prog08 {
    public static void main(String[] args) {
        NewThread[] threads = new NewThread[5]; // Array estático de threads (tamaño fijo!)
        
        // Crea hilos en el array y los lanza!
        for(int i = 0; i < threads.length; i++) {
            threads[i] = new NewThread("Thread" + i);
            threads[i].startThread();
        }

        // Espera a que todos los hilos terminen
        for(int i = 0; i < threads.length; i++) {
            try {
                threads[i].t.join();
            } catch (InterruptedException e) {
                System.out.println("Thread " + threads[i].t.getName() + " interrupted");
            }
        }
        System.out.println("[" + Thread.currentThread().getName() + "] All threads done!");
    }
}
