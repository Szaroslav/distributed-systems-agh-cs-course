import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
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
                DatagramPacket receivePacket = new DatagramPacket(
                    receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);
                int msg = ByteBuffer.wrap(receivePacket.getData())
                    .order(ByteOrder.LITTLE_ENDIAN)
                    .getInt();
                System.out.println("Received message: " + msg);

                byte[] sendBuffer   = ByteBuffer.allocate(4)
                    .order(ByteOrder.LITTLE_ENDIAN)
                    .putInt(msg + 1)
                    .array();
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
