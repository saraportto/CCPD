// ENTER AND WAIT
class TaskExecutor {

    // Método que simula la entrada y espera de un thread
    public void EnterAndWait(int threadNumber){

        try{
            System.out.println("Starting Thread " + threadNumber); // Imprime inicio del thread
            Thread.sleep((int)(Math.random() * 100)); // Simula un tiempo de espera aleatorio (por eso está en sleep)
            System.out.println("Finishing Thread " + threadNumber); // Imprime fin del thread
        
        } catch(InterruptedException e){
            System.out.println(e.getMessage());
        }   
    }
}


// HILO
class TaskRunnable implements Runnable{

    TaskExecutor taskExecutor; // Con parámetro TaskExecutor
    int threadNumber; // Con parámetro threadNumber
    
    // Constructor
    TaskRunnable(int threadNumber,  TaskExecutor taskExecutor){
        this.threadNumber = threadNumber;
        this.taskExecutor = taskExecutor;    
    }
    
    // Llama a EnterAndWait del objeto TaskExecutor de la construcción
    public void run() {
        taskExecutor.EnterAndWait(threadNumber);
	}  
}


// MAIN
public class lab2prob09 {
    public static void main(String[] args) {

        TaskExecutor taskExecutor = new TaskExecutor(); // Un único TaskExecutor
        int threadNumber = 5; // Número determiado de threads
        TaskRunnable taskRunnables[] = new TaskRunnable[threadNumber]; // Varios taskRunnable
        Thread threads[] = new Thread[threadNumber]; // Varios threads
    
        // Para cada TaskRunnable, se crea un thread y se inicializa
        for(int i = 0; i < threadNumber; i++){
            taskRunnables[i] = new TaskRunnable(i, taskExecutor); // Se crea un TaskRunnable, con el número de thread y el TaskExecutor
            threads[i] = new Thread(taskRunnables[i]); // Se crea un thread con el TaskRunnable correspondiente
            threads[i].start(); // Inicializa
        }
        
        try{
            // Asegura que todos los threads terminen
            for(int i = 0; i < threadNumber; i++){
                threads[i].join();
            }
        }catch(InterruptedException e){
            System.out.println(e.getMessage());
        }

        System.out.println("Finished.");}
}