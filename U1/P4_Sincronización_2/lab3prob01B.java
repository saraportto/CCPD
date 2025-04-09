// Clase principal
class TickTockToe {
    String state="toed";

	// TICK
    synchronized void tick (boolean running){
		if (!running) {   //stop clock
			state="ticked";
			notifyAll(); // notify any waiting threads
			return;
		}

		try {
			while(!state.equals("toed")) {
				wait(); // wait for toed to complete
			}
		} catch (InterruptedException exc) {
			System.out.println("interrupted");
		}

		System.out.print("Tick... ");
		state="ticked";
		notifyAll(); 
		
    }

	// TOCK
    synchronized void tock (boolean running){
		if (!running) { //stop clock
			state="tocked";
			notifyAll(); // notify any waiting threads
			return;
		}

		try {
			while(!state.equals("ticked")) {
				wait(); // wait for tock to complete
			}
		} catch (InterruptedException exc) {
			System.out.println("interrupted");
		}

		System.out.print("Tock... ");
		state="tocked";
		notifyAll(); 
    }

	// TOE
	synchronized void toe (boolean running){
		if (!running) { //stop clock
			state="toed";
			notifyAll(); // notify any waiting threads
			return;
		}

		try {
			while(!state.equals("tocked")) {
				wait(); // wait for tock to complete
			}
		} catch (InterruptedException exc) {
			System.out.println("interrupted");
		}

		System.out.println("Toe!");
		state="toed";
		notifyAll();	
	}
}



// Clase hilo
class MyThread implements Runnable{
    Thread thrd;
    TickTockToe ttOb;
    
    // constructor of new thread
    MyThread(String name, TickTockToe tt){
		thrd = new Thread(this, name);
		ttOb = tt;
    }

    public void run() {
		if(thrd.getName().compareTo("Tick") == 0){
			for (int i=0; i<=5; i++) ttOb.tick(true);
			ttOb.tick(false);
		
		}else if(thrd.getName().compareTo("Tock") == 0){
			for (int i=0; i<=5; i++) ttOb.tock(true);
			ttOb.tock(false);	

		} else {
			for (int i=0; i<=5; i++) ttOb.toe(true);
			ttOb.toe(false);
		}
    }
}


// Main
public class lab3prob01B{
    public static void main(String agrs[]){
		TickTockToe tt = new TickTockToe();
	
		MyThread mt1 = new MyThread("Tick", tt);
		MyThread mt2 = new MyThread("Tock", tt);	
		MyThread mt3 = new MyThread("Toe", tt);    
		
		mt1.thrd.start();
		mt2.thrd.start();
		mt3.thrd.start();
	
		try {
			mt1.thrd.join();
			mt2.thrd.join();
			mt3.thrd.join();
		} catch (InterruptedException exc){
			System.out.println("main thread interrupted");
		}
    }
}
