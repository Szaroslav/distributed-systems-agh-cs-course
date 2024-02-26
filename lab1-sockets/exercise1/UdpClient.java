import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Arrays;

public class UdpClient {

    public static void main(String args[]) throws Exception
    {
        System.out.println("Java UDP client");

        DatagramSocket socket = null;
        int portNumber        = 9008;

        try {
            socket              = new DatagramSocket();

            InetAddress address = InetAddress.getByName("localhost");
            byte[] sendBuffer   = "UDP client message".getBytes();
            DatagramPacket sendPacket = new DatagramPacket(
                sendBuffer, sendBuffer.length, address, portNumber);
            socket.send(sendPacket);

            byte[] receiveBuffer = new byte[1024];
            Arrays.fill(receiveBuffer, (byte) 0);
            DatagramPacket receivePacket = new DatagramPacket(
                receiveBuffer, receiveBuffer.length);
            socket.receive(receivePacket);
            String msg = new String(receivePacket.getData());
            System.out.println("Received message: " + msg);
            System.out.println("Sender address:   " + receivePacket.getSocketAddress());
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
