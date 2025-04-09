class TransThread extends Thread {
    private FinTrans ft;
    private Object lock; // Lock object shared between threads

    TransThread(FinTrans ft, String name, Object lock) {
        super(name);
        this.ft = ft;
        this.lock = lock; // Use a shared lock object
    }

    public void run() {
        for (int i = 0; i < 100; i++) {
            synchronized (lock) {
                if (getName ().equals ("Deposit Thread")){
                    ft.transName = "Deposit Thread";
                    try {
                        Thread.sleep ((int) (Math.random () * 1000));
                    } catch (InterruptedException e) {}
                    
                    ft.amount = 2000.0;
                    System.out.println (ft.transName + " " + ft.amount);
                
                } else {
                    ft.transName = "Withdrawal Thread";
                    try {
                        Thread.sleep ((int) (Math.random () * 1000));
                    } catch (InterruptedException e)  {}
                    ft.amount = 250.0;
                    System.out.println (ft.transName + " " + ft.amount);
                }
            }
        }
    }
}

class lab2prob03 {
    public static void main (String [] args)  {
	 FinTrans ft = new FinTrans();
       // Shared lock object
       Object lock = new Object();
	   TransThread tt1 = new TransThread(ft, "Deposit Thread", lock);
       TransThread tt2 = new TransThread(ft, "Withdrawal Thread", lock);
       tt1.start ();
       tt2.start ();
    }
 }