import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class DuvarKac(Node):

    def __init__(self):
        super().__init__('duvar_kac')

        self.yayinci = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )

        self.abone = self.create_subscription(
            Pose, '/turtle1/pose', self.konum_al, 10
        )

        self.x = 5.5
        self.y = 5.5
        self.aci = 0.0
        self.donuyor = False
        self.declare_parameter('hiz', 2.0)
        self.declare_parameter('sinir', 1.0)

        self.hiz = self.get_parameter('hiz').value
        self.sinir = self.get_parameter('sinir').value

        self.zamanlayici = self.create_timer(0.1, self.hareket_et)

    def konum_al(self, mesaj):
        self.x = mesaj.x
        self.y = mesaj.y
        self.aci = mesaj.theta

    def hareket_et(self):
        hiz = Twist()

        if self.x < self.sinir or self.x > 11.0 - self.sinir or self.y < self.sinir or self.y > 11.0 - self.sinir:
            if not self.donuyor:
                self.get_logger().info("Duvara yaklastim, yon degistiriyorum!")
            self.donuyor = True

        if self.donuyor:
            hedef_aci = math.atan2(5.5 - self.y, 5.5 - self.x)

            fark = math.atan2(
                math.sin(hedef_aci - self.aci),
                math.cos(hedef_aci - self.aci)
            )

            if abs(fark) > 0.1:
                hiz.linear.x = 0.0
                hiz.angular.z = 2.0 if fark > 0 else -2.0
            else:
                self.donuyor = False
                hiz.linear.x = self.hiz
                hiz.angular.z = 0.0
                self.get_logger().info("Yon degistirdim, ilerliyorum!")

        else:
            hiz.linear.x = self.hiz
            hiz.angular.z = 0.0

        self.yayinci.publish(hiz)

def main(args=None):
    rclpy.init(args=args)

    dugum = DuvarKac()
    rclpy.spin(dugum)

    dugum.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()