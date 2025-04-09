import java.util.concurrent.TimeUnit;

// Clase HILO
// Clase que genera números primos
class PrimeGenerator extends Thread {

    @Override
    public void run() {
        long number = 1L;

        // Mientras no se interrumpa el hilo
        while (!isInterrupted()) {

            // Si el número es primo, se imprime
            if (isPrime(number)) {
                System.out.printf("Number %d is Prime\n", number);
            }

            number++; // se suma el contador
        }

        // Cuando se interrumpe el hilo --> se imprime
        System.out.println("The Prime Generator has been Interrupted");
    }

    // Función que verifica si un número es primo
    private boolean isPrime(long number) {
        if (number <= 2) {
            return true;
        }
        for (long i = 2; i <= Math.sqrt(number); i++) {
            if (number % i == 0) {
                return false;
            }
        }
        return true;
    }
}


// Clase MAIN
public class lab1prog12 {
    
    public static void main(String[] args) {

        // Crea, pone nombre y arranca el hilo 
        Thread task = new PrimeGenerator();
        task.setName("PrimeGeneratorThread");
        task.start();

        // Espera 5 segundos e interrumpe el hilo
        try {
            TimeUnit.SECONDS.sleep(5);

        } catch (InterruptedException e) {
            System.out.println("Main thread interrupted while sleeping.");
        }
        
        // Interrumpe el hilo
        task.interrupt();

        // Imprime el estado del hilo
        System.out.printf("Main: Status of the Thread: %s\n", task.getState());
        System.out.printf("Main: isInterrupted: %s\n", task.isInterrupted());
        System.out.printf("Main: isAlive: %s\n", task.isAlive());
    }
}