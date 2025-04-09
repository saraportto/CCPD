public class lab1prog03 implements Runnable {
    
    @Override
    public void run() { 
        System.out.println("Executing thread " + Thread.currentThread().getName());

        // Se puede añadir más código aquí para demostrar la funcionalidad del hilo
        System.out.println("Priority thread " + Thread.currentThread().getName() + ": " + Thread.currentThread().getPriority());
    }

    public static void main(String[] args) {
        // Create a Thread object using Lab1Prog03, which implements Runnable
        Thread myThread = new Thread(new lab1prog03(), "myRunnable");
        Thread myThread2 = new Thread(new lab1prog03(), "myRunnable2");

        // Start the thread
        myThread.start(); // Hace lo que hay dentro del run() -- CURRENTTHREAD!!
        myThread2.start();

    }
}