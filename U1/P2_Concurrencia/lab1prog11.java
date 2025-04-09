// Clase HILO
class MyInterruptThread implements Runnable {
 
    // Run que hace sleep
    @Override
    public void run() {
    
    // Hilo hace sleep 
        try {
            // Thread goes to sleep for a long duration
            Thread.sleep(Long.MAX_VALUE); // Hilo sleepea demasiado

        } catch (InterruptedException e) {
            // Handling the interrupt exception
            System.out.println("[" + Thread.currentThread().getName() + "] Interrupted by exception!");
        }
        
        // Loop continues until the thread is interrupted again
        while (!Thread.interrupted()) {
            // Loop body is empty
        }

        // El hilo se interrumpe por segunda vez
        System.out.println("[" + Thread.currentThread().getName() + "] Interrupted for the second time.");
    }
}

// Clase MAIN
public class lab1prog11 {

    // Main
    public static void main(String[] args) throws InterruptedException {
        
        // Crea e inicializa un hilo
        Thread myThread = new Thread(new MyInterruptThread(), "myThread");
        myThread.start();
         
        // Main thread sleeps for a while
        System.out.println("[" + Thread.currentThread().getName() + "] Sleeping in main thread for 5s...");
        Thread.sleep(5000);
         
        // Main thread interrupts 'myThread'
        System.out.println("[" + Thread.currentThread().getName() + "] Interrupting myThread");
        myThread.interrupt();
         
        // Main thread sleeps again
        System.out.println("[" + Thread.currentThread().getName() + "] Sleeping in main thread for 5s...");
        Thread.sleep(5000);
         
        // Main thread interrupts 'myThread' a second time
        System.out.println("[" + Thread.currentThread().getName() + "] Interrupting myThread");
        myThread.interrupt();
    }
}

