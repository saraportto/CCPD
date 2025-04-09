// "Simulacro" de CAS

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class lab2prob07 { // Non-reentrant lock (CAS lock)
    private AtomicBoolean locked = new AtomicBoolean(false);
    
    public void lock() {
        while (!this.locked.compareAndSet(false, true)) {
            // busy wait - until compareAndSet() succeeds
        }
    }

    public void unlock() {
        this.locked.set(false);
    }

    public static void main(String[] args) {
        final lab2prob07 lock = new lab2prob07(); // Create a lock object
        final AtomicInteger counter = new AtomicInteger(0);
        final int numberOfThreads = 10;
        Thread[] threads = new Thread[numberOfThreads];

        long startTime = System.nanoTime(); // Start time measurement

        for (int i = 0; i < threads.length; i++) {
            threads[i] = new Thread(new Runnable() {
                @Override
                public void run() {
                    for (int j = 0; j < 1000; j++) {
                        lock.lock();
                        try {
                            // Critical section 
                            //- only one thread can increment the counter at a time
                            counter.incrementAndGet();
                        } finally {
                            lock.unlock();
                        }
                    }
                }
            });
            threads[i].start();
        }
        
        for (Thread t : threads) {
            try {
                t.join(); // Wait for all threads to finish
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        long endTime = System.nanoTime(); // End time measurement
        long duration = endTime - startTime; // Calculate the duration

        System.out.println("Final counter value: " + counter.get());
        System.out.println("Duration: " + duration + " ns");
    }
}