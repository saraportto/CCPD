public class lab1prog02 extends Thread {

    public lab1prog02(String name) {
        super(name); // Constructor que indica que el nombre es lo que se indica en Name
    }

    @Override
    public void run() {
        System.out.println("Executing thread: " + Thread.currentThread().getName());
        
        // You can add more code here to demonstrate the thread's functionality
        System.out.println("Priority " +  Thread.currentThread().getName() + ": " + Thread.currentThread().getPriority());
    }

    public static void main(String[] args) {  // Método main
        lab1prog02 myThread = new lab1prog02("myThread"); // Variable myThread de tipo lab1prog02
        lab1prog02 myThread2 = new lab1prog02("myThread2");

        myThread.setPriority(Thread.MAX_PRIORITY); // Asigna la prioridad máxima al hilo
        myThread2.setPriority(Thread.MIN_PRIORITY); // Asigna la prioridad mínima al hilo

        myThread.start();  // Inicia el hilo
        myThread2.start();
    }
}
