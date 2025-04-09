
class CounterThread extends Thread {
    private SharedCounter sharedCounter;

    public CounterThread(SharedCounter sharedCounter) {
        this.sharedCounter = sharedCounter;
    }

    @Override
    public void run() {
        for (int i = 0; i < 1000; i++) {
            sharedCounter.increment();
        }
    }
}
class SharedCounter {
    private int count = 0;

    public void increment() {
        count++;
    }

    public int getCount() {
        return count;
    }
}



public class lab2prob04 {
    public static void main(String[] args) throws InterruptedException {
        SharedCounter sharedCounter = new SharedCounter();
        Thread[] threads = new Thread[10];

        // Create and start threads
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new CounterThread(sharedCounter);
            threads[i].start();
            threads[i].join(); // Si no, se van a ir pisando los hilos, "robando" la variable compartida
        }

        // Wait for all threads to finish
        for (Thread thread : threads) {
            thread.join();
        }
        System.out.println("Final Counter Value: " + sharedCounter.getCount());
    }
}

