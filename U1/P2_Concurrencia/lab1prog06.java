// THREAD class
class NewThread implements Runnable {

    String name;
    Thread t;
    
    NewThread(String threadName) {
        name = threadName;
        t = new Thread(this, name);
        System.out.println("New thread created: " + t);
    }

    public void startThread() {
        t.start();
    }

    public void run() { // RUN METHOD
        try {
            for (int i = 5; i > 0; i--) {
                System.out.println(name + " Child Thread: " + i);
                Thread.sleep(500);
            }
        } catch (InterruptedException e) {
            System.out.println(name + " interrupted.");
        }
        System.out.println(name + " exiting.");
    }
}


// MAIN class
class lab1prog06 { 

    public static void main(String[] args) {

        // Creo y lanzo tres threads
        NewThread nt1 = new NewThread("One");
        NewThread nt2 = new NewThread("Two");
        NewThread nt3 = new NewThread("Three");

        nt1.startThread();
        nt2.startThread();
        nt3.startThread();

        // Main thrad que hace join con los tres threads
        // Si comentamos los join, el main thread termina antes que los otros threads
        try { 
            nt1.t.join();
            nt2.t.join();
            nt3.t.join();
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            System.out.println("Main thread interrupted");
        }

        System.out.println("Main thread exiting");
    }
}
