import java.util.LinkedList; 

// SHARED BUFFER
class SharedBuffer {
    private LinkedList<Integer> buffer = new LinkedList<>();
    private int capacity = 10;

    // ADD method
    public synchronized void add(int value){
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


    // REMOVE method
    public synchronized int remove() {
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


// PRODUCER Thread
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


// CONSUMER Thread
class Consumer extends Thread {
    private SharedBuffer buffer;

    public Consumer(SharedBuffer buffer) {
        this.buffer = buffer;
    }

    @Override
    public void run() {
        for (int i = 0; i < 50; i++) {
          int value;
          value = buffer.remove();

          StringBuilder stringBuilder = new StringBuilder();
          System.out.println("Consumed: " + value);
        }
    }
}


// MAIN
public class lab2prob13 {
    public static void main(String[] args) {
        SharedBuffer buffer = new SharedBuffer();
        Producer producer = new Producer(buffer);
        Consumer consumer = new Consumer(buffer);
        producer.start();
        consumer.start();
    }
}