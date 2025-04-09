// Trata de SERIALIZAR (objeto-->bytestream) los flujos
// Luego DESERIALIZAR (bytestream-->objeto) los flujos
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.io.FileInputStream;
import java.io.ObjectInputStream;
import java.io.Serializable;

public class lab5prog02 {

    // -------------------------------------------------------------------------
    // Constructor
    public static class Message implements Serializable {
        public String msg = null;
        public int code = 0;
        public Message(String msg, int code) {
            this.msg = msg;
            this.code = code;
        }
    }
    
    // -------------------------------------------------------------------------
    // Serialize and Deserialize the Message object
    public static void serializeMessage() {
        Message message = new Message("Hello, World!", 1); 

        // SERIALIZE the Message object
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("message.ser"))) {
            oos.writeObject(message); // Write the object to the file (oos es un bytestream, message.ser)
            System.out.println("Serialization done.");
        } catch (Exception e) {
            e.printStackTrace();
        }

        // DESERIALIZE the Message object
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream("message.ser"))) {
            Message readMessage = (Message) ois.readObject(); // Read the object from the file (ois es un bytestream, message.ser)
            System.out.println("Deserialization done. Message: " + readMessage.msg 
               + ", Code: " + readMessage.code);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // -------------------------------------------------------------------------
    // Main method
    public static void main(String[] args) {
        serializeMessage();
    }
}