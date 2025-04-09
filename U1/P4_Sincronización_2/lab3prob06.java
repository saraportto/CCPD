import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

// Clase BOUNDEDBUFFER
class BoundedBuffer {
    // Lock para proteger el acceso al buffer
    final Lock lock = new ReentrantLock();

    // Variables de condiciones para esperar a que el buffer no esté lleno o vacío
    final Condition notFull = lock.newCondition();
    final Condition notEmpty = lock.newCondition();

    // Buffer y metadatos
    final Object[] items = new Object[100]; // Tamaño del buffer
    int putptr, takeptr, count; // Índices para putting and taking items, y el current number of items

    // AÑADIR UN ÚTEM AL BUFFER
    public void put(Object x) throws InterruptedException {
        lock.lock(); // LOCK antes de modificar el buffer
        try {
            // Esperar mientras el buffer esté lleno
            while (count == items.length) {
                notFull.await(); // AWAIT
            }
            // Añade un ítem al buffer
            items[putptr] = x; // Añade el ítem
            if (++putptr == items.length) putptr = 0; // Incremento circular del puntero de añadir
            ++count; // Incrementa el número de ítems en el buffer
            notEmpty.signal(); // SIGNAL a los productores indicando que hay espacio
        } finally {
            lock.unlock(); // UNLOCK
        }
    }

    // ELIMINAR Y DEVOLVER UN ITEM DEL BUFFER
    public Object take() throws InterruptedException {
        lock.lock(); // LOCK antes de modificar el buffer
        try {
            // Esperar mientras el buffer esté vacío
            while (count == 0) {
                notEmpty.await(); // AWAIT
            }
            // Elimina un ítem del buffer
            Object x = items[takeptr]; // Quita el ítem
            if (++takeptr == items.length) takeptr = 0; // Incremento circular del puntero de quitar
            --count; // Decrementa el número de ítems en el buffer
            notFull.signal(); // SIGNAL any waiting producers that there is space
            return x;
        } finally {
            lock.unlock(); // UNLOCK
        }
    }
}

// Clase CONSUMER
class Consumer implements Runnable {
    private final BoundedBuffer buffer; // Buffer compartido

    public Consumer(BoundedBuffer buffer) {
        this.buffer = buffer;
    }

    @Override
    public void run() {
        try {
            while (true) { // Bucle infinito para consumir continuamente ítems
                Object item = buffer.take(); // Consumir un ítem
                System.out.println(Thread.currentThread().getName() + " consumed " + item);
                Thread.sleep(1000); // Simulate time to consume an item
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.out.println("Consumer was interrupted.");
        }
    }
}

// Clase PRODUCER
class Producer implements Runnable {
    private final BoundedBuffer buffer; // Buffer compartido

    public Producer(BoundedBuffer buffer) {
        this.buffer = buffer;
    }

    @Override
    public void run() {
        try {
            while (true) { // Bucle infinito para producir continuamente ítems
                Object item = produceItem(); // Producir un ítem
                buffer.put(item); // Añadir un ítem al buffer
                System.out.println(Thread.currentThread().getName() + " produced " + item);
                Thread.sleep(1000); // Simulate time to produce an item
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.out.println("Producer was interrupted.");
        }
    }

    // Simulate producing an item
    private Object produceItem() {
        return "item" + Math.random(); // Return a random item
    }
}


// Clase MAIN
public class lab3prob06 {
    public static void main(String[] args) {
        BoundedBuffer buffer = new BoundedBuffer(); // Crea BounderBuffer

        // Crea e inicializa 3 hilos productores
        int numberOfProducers = 3;
        for (int i = 0; i < numberOfProducers; i++) {
            Thread producerThread = new Thread(new Producer(buffer), "Producer-" + i);
            producerThread.start();
        }

        // Crea e inicializa 3 hilos consumidores
        int numberOfConsumers = 3;
        for (int i = 0; i < numberOfConsumers; i++) {
            Thread consumerThread = new Thread(new Consumer(buffer), "Consumer-" + i);
            consumerThread.start();
        }
    }
}


/*   Alternative
public class lab3prob06 {
    public static void main(String[] args) {
        BoundedBuffer buffer = new BoundedBuffer();

        // Create and start multiple producer threads.
        int numberOfProducers = 3;
        for (int i = 0; i < numberOfProducers; i++) {
            new Thread(() -> {
                try {
                    while (true) { // Infinite loop to continuously produce items.
                        Object item = produceItem();
                        buffer.put(item);
                        System.out.println(Thread.currentThread().getName() + " produced " + item);
                        Thread.sleep(1000); // Simulate time to produce an item.
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }, "Producer-" + i).start();
        }

        // Create and start multiple consumer threads.
        int numberOfConsumers = 3;
        for (int i = 0; i < numberOfConsumers; i++) {
            new Thread(() -> {
                try {
                    while (true) { // Infinite loop to continuously consume items.
                        Object item = buffer.take();
                        System.out.println(Thread.currentThread().getName() + " consumed " + item);
                        Thread.sleep(1000); // Simulate time to consume an item.
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }, "Consumer-" + i).start();
        }
    }

    //   Method to simulate producing an item. In a real scenario, 
    ///  this could be replaced with actual item production logic.
    private static Object produceItem() {
        return "item" + Math.random();
    }
}
*/