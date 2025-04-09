
class SharedResource {
    final Object lock = new Object();
    boolean flag = false;  
}


class FirstThread extends Thread {
    static int iInteger;
    private final SharedResource sharedResource;

    public FirstThread(SharedResource sharedResource) {
        this.sharedResource = sharedResource;
    }

    @Override
    public void run() {
        System.out.println("Inside FirstThread");
        while (true) {
            firstCoffee();
            try {
                Thread.sleep(2000); // Simulate work
            } catch (InterruptedException e) {
                // Handle interruption
            }
        }
    }

    void firstCoffee() {
        synchronized (sharedResource.lock) {
            while (sharedResource.flag) {
                try {
                    sharedResource.lock.wait();
                } catch (InterruptedException e) {
                    // Handle interruption
                }
            }
            // Added output to indicate action in FirstThread
            System.out.println(Thread.currentThread().getName() + " preparing coffee, iInteger=" + iInteger);
            
            sharedResource.flag = true;
            sharedResource.lock.notifyAll();
        }
    }
}

class SecondThread extends Thread {
    private final SharedResource sharedResource;

    public SecondThread(SharedResource sharedResource) {
        this.sharedResource = sharedResource;
    }

    @Override
    public void run() {
        System.out.println("Inside SecondThread");
        while (true) {
            secondCoffee();
        }
    }

    void secondCoffee() {
        synchronized (sharedResource.lock) {
            while (!sharedResource.flag) {
                try {
                    sharedResource.lock.wait();
                } catch (InterruptedException e) {
                    // Handle interruption
                }
            }
            System.out.println(Thread.currentThread().getName() + " " + (++FirstThread.iInteger));
            sharedResource.flag = false;
            sharedResource.lock.notifyAll();
        }
    }
}
public class lab2prob08 {
    public static void main(String[] args) {
        SharedResource sharedResource = new SharedResource();
        FirstThread a = new FirstThread(sharedResource);
        SecondThread b = new SecondThread(sharedResource);
        a.start();
        b.start();
    }
}