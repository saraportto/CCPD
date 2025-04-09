import java.util.ArrayList;
import java.util.List;

// Clase HILO que calcula los números primos entre 1 y 20000
class ThreadCalculator implements Runnable {

    // Run que calcula los números primos
    @Override
    public void run() {
        long current = 1L;
        long max = 20000L;
        long numPrimes = 0L;
        System.out.printf("Thread '%s': START\n", Thread.currentThread().getName());
        while (current <= max) {
            if (isPrime(current)) {
                numPrimes++;
            }
            current++;
        }
        System.out.printf("Thread '%s': END. Number of Primes: %d\n", Thread.currentThread().getName(), numPrimes);
    }

    // Función que calcula si un número es primo o no (devuelve SI/NO)
    private boolean isPrime(long number) {
        if (number <= 2) { 
            return true;
        }
        for (long i = 2; i < number; i++) {
            if ((number % i) == 0) {
                return false;
            }
        }
        return true;
    }
}

// Clase MAIN
public class lab1prog10 {

    // Main
    public static void main(String[] args) {

        // Imprime las prioridades de los hilos (mínima, normal, máxima)
        System.out.printf("Minimum Priority: %s\n", Thread.MIN_PRIORITY);
        System.out.printf("Normal Priority: %s\n", Thread.NORM_PRIORITY);
        System.out.printf("Maximum Priority: %s\n", Thread.MAX_PRIORITY);

        // Crea una lista de hilos y una lista de estados
        List<Thread> threads = new ArrayList<>();
        List<Thread.State> status = new ArrayList<>();

        // Crea 10 hilos y les asigna prioridades (según sean pares o impares)
        for (int i = 0; i < 10; i++) {
            Thread thread = new Thread(new ThreadCalculator());

            // LOS PARES --> PRIORIDAD MÁXIMA
            if ((i % 2) == 0) { 
                thread.setPriority(Thread.MAX_PRIORITY);

            // LOS IMPARES --> PRIORIDAD MÍNIMA
            } else { 
                thread.setPriority(Thread.MIN_PRIORITY);
            }

            thread.setName("My Thread " + i); // Nombre del hilo
            threads.add(thread); // Añade hilo a la LISTA DE HILOS
            status.add(thread.getState()); // Añade estado a la LISTA DE ESTADOS
        }

        // Bucle que imprime el estado de los hilos 
        for (int i = 0; i < threads.size(); i++) {
            System.out.println("Main : Status of Thread " + i + " : " + threads.get(i).getState());
        }

        // Bucle que inicia los hilos
        for (int i = 0; i < threads.size(); i++) {
            System.out.println("Main : Starting Thread " + i);
            threads.get(i).start(); // Inicia los hilos
        }

        // threads.forEach(Thread::start); // Inicia los threads

        // Bucle que espera a que los hilos terminen
        boolean finish = false;

        // Itera sobre los hilos mientras no hayan terminado
        while (!finish) {
            for (int i = 0; i < threads.size(); i++) {
                Thread thread = threads.get(i); // Obtiene el hilo

                // Si el estado del hilo ha cambiado, imprime la info
                if (thread.getState() != status.get(i)) {
                    writeThreadInfo(thread, status.get(i)); // Imprime info
                    status.set(i, thread.getState()); // Actualiza el estado
                }
            }

            // Acaba si todos los threads han terminado
            finish = threads.stream().allMatch(t -> t.getState() == Thread.State.TERMINATED);
        }
    }

    // Función que imprime la información de un hilo
    private static void writeThreadInfo(Thread thread, Thread.State state) {
        System.out.printf("Main : Id %d - %s\n", thread.getId(), thread.getName());
        System.out.printf("Main : Priority: %d\n", thread.getPriority());
        System.out.printf("Main : Old State: %s\n", state);
        System.out.printf("Main : New State: %s\n", thread.getState());
        System.out.printf("Main : ************************************\n");
    }
} 

