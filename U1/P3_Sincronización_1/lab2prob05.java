class SharedResource {       

    public synchronized void methodOne() {
        System.out.println(Thread.currentThread().getName());
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("Thread " + Thread.currentThread().getName() + " done executing methodOne");
    }

    public synchronized void methodTwo() {
        System.out.println(Thread.currentThread().getName());
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("Thread " + Thread.currentThread().getName() + " done executing methodTwo");
    }
}

class MyTaskThread extends Thread {
    private SharedResource sharedResource;
    private boolean runFirstMethod;

    public MyTaskThread(SharedResource sharedResource, boolean runFirstMethod) {
        this.sharedResource = sharedResource;
        this.runFirstMethod = runFirstMethod;
    }

    @Override
    public void run() {
        if (runFirstMethod) {
            sharedResource.methodOne();
        } else {
            sharedResource.methodTwo();
        }
    }
}

public class lab2prob05 {
    public static void main(String[] args) {
        SharedResource sharedResource = new SharedResource();

        MyTaskThread thread1 = new MyTaskThread(sharedResource, true);
        MyTaskThread thread2 = new MyTaskThread(sharedResource, false);

        thread1.start();
        thread2.start();
    }
}