import java.util.LinkedList; 


// SHARED BUFFER CLASS
class SharedBuffer {
    private LinkedList<Integer> buffer = new LinkedList<>();
    private int capacity = 10;

    // ADD method
    public void add(int value){
        synchronized(this) {
            while (buffer.size() == capacity){
                try {
                    wait();
                } catch (Exception e) {
                    Thread.currentThread().interrupt();
                }
            }
            buffer.add(value);
            notifyAll();
        }
    }

    // REMOVE method
    public int remove() {
        synchronized (this) {
            while (buffer.isEmpty()) {
                try {
                    wait(); // Busy-waiting when buffer is empty
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
            int value = buffer.removeFirst();
            notifyAll();
            return value;
        }
    }
}


// PRODUCER (Thread)
class Producer extends Thread {
    private SharedBuffer buffer;

    public Producer(SharedBuffer buffer) {
        this.buffer = buffer;
    }

    @Override
    public void run() {
        for (int i = 0; i < 50; i++) {
            buffer.add(i);
            System.out.println("Produced: " + i);
        }
    }
}


// CONSUMER (Thread)
class Consumer extends Thread {
    private SharedBuffer buffer;

    public Consumer(SharedBuffer buffer) {
        this.buffer = buffer;
    }

    @Override
    public void run() {
        for (int i = 0; i < 50; i++) {
            int value = buffer.remove();
            System.out.println("Consumed: " + value);
        }
    }
}


// MAIN
public class lab2prob12 {
    public static void main(String[] args) {
        SharedBuffer buffer = new SharedBuffer();

        Producer producer = new Producer(buffer);
        Consumer consumer = new Consumer(buffer);

        producer.start();
        consumer.start();
    }
}