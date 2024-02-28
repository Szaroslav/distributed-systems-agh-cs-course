import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.Arrays;

public class UdpServer {

    public static void main(String args[])
    {
        System.out.println("Java UDP server");

        DatagramSocket socket = null;
        int portNumber        = 9009;

        try {
            socket               = new DatagramSocket(portNumber);
            byte[] receiveBuffer = new byte[1024];

            while (true) {
                Arrays.fill(receiveBuffer, (byte) 0);
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);
                String msg = new String(receivePacket.getData());
                System.out.println("Received message: " + msg);

                byte[] sendBuffer = "Liar!".getBytes();
                if (msg.startsWith("J")) {
                    sendBuffer = "Java UDP pong!".getBytes();
                }
                else if (msg.startsWith("P")) {
                    sendBuffer = "Python UDP pong!".getBytes();
                }

                DatagramPacket sendPacket = new DatagramPacket(
                    sendBuffer, sendBuffer.length, receivePacket.getSocketAddress());
                socket.send(sendPacket);
            }
        }
        catch(Exception e) {
            e.printStackTrace();
        }
        finally {
            if (socket != null) {
                socket.close();
            }
        }
    }

}
