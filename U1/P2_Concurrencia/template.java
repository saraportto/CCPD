// Main class
class MyMainClass {
    public static void main(String args[]) {
        NewThread nt = new NewThread("Demo Thread");
        nt.startThread(); // Start the thread using the method (el método startThread() llama a start())

        // El sleep HA DE ESTAR dentro del try-catch
        try {
            for (int i = 5; i > 0; i--) {
                System.out.println(Thread.currentThread().getName() + ": " + i);
                Thread.sleep(1000);
            }
        } catch (InterruptedException e) {
            System.out.println("Main thread interrupted");
        }
        System.out.println("Main thread exiting");
    }
}

class NewThread implements Runnable {
    Thread t;

    NewThread(String threadName) {
        t = new Thread(this, threadName);
    }

    public void startThread() {
        t.start();
    }

    public void run() {
        // El sleep HA DE ESTAR dentro del try-catch
        try { 
            for (int i = 5; i > 0; i--) {
                System.out.println(Thread.currentThread().getName() + ": " + i);
                Thread.sleep(500);
            }
        } catch (InterruptedException e) {
            System.out.println(Thread.currentThread().getName() + " interrupted.");
        }
        System.out.println(Thread.currentThread().getName() + " exiting and will be destroyed.");
    }
}