
class SharedResource {
    final Object lock = new Object();
    boolean flag = false;  
}


class CoffeeThread extends Thread {
    static int iInteger;
    private final SharedResource sharedResource;
    private boolean isfirst;

    public CoffeeThread(SharedResource sharedResource) {
        this.sharedResource = sharedResource;
    }

    @Override
    public void run() {
        while(true) {
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                // Handle interruption
            }

            if (Thread.currentThread().getName().equals("Thread-0")) {
                firstCoffee();
            } else {
                secondCoffee();
            }
        }
    }

    public void firstCoffee() {
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

    public void secondCoffee() {
        synchronized (sharedResource.lock) {
            while (!sharedResource.flag) {
                try {
                    sharedResource.lock.wait();
                } catch (InterruptedException e) {
                    // Handle interruption
                }
            }
            System.out.println(Thread.currentThread().getName() + " " + (++iInteger));
            sharedResource.flag = false;
            sharedResource.lock.notifyAll();
        }
    }
}

public class lab2prob08B {
    public static void main(String[] args) {
        SharedResource sharedResource = new SharedResource();
        CoffeeThread first_coffee = new CoffeeThread(sharedResource);
        CoffeeThread second_coffee = new CoffeeThread(sharedResource);
        first_coffee.start();
        second_coffee.start();
    }
}