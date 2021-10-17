import urx
import threading
import time


from Filters import MeanFilter, WeightedFilter

class UR3(threading.Thread):
    def __init__(self,ip, track_threshold=0.1, payload=0.5):
        """

        :param ip: robot ip
        :param track_threshold: 跟踪间隔 s
        :param payload: 负载 kg
        """
        threading.Thread.__init__(self)
        # self.filter = WeightedFilter(0.80)
        self.filter = MeanFilter(20)
        self.robot = urx.Robot(str(ip))
        self.robot.set_tcp((0, 0, 0.0, 0, 0, 0))
        self.robot.set_payload(payload, (0, 0, 0))
        self.th = track_threshold
        self.canrun = False
        self.Flag = True


    def addpoint(self, point):
        self.filter.add(point)

    def pos(self):
        return self.robot.getl()

    def stop(self):
        self.Flag = False

    def run(self):
        while self.Flag:

            if self.canrun:
                point = self.filter.get()
                if point is None or not any(point):
                    time.sleep(self.th)
                    continue
                pos = self.robot.getl()
                dis = sum([(point[i]-pos[i])**2 for i in range(3)])
                dis = (dis)**0.5

                # ang = sum([(point[i]-pos[i])**2 for i in range(3,6)])
                # ang = (ang)**0.5
                if dis > 0.008:  # 小于 x m 不跟踪
                    # print(dis)
                    a = 0.15
                    v = 0.30
                    # a = 16*dis/(3*self.th**2)
                    # v = 4*dis/(3*self.th)
                    # print("a", a)
                    # print("v", v)
                    # a = min(max(0.01, a), 0.15)
                    # v = min(max(0.01, v), 0.3)
                    # pos[0] = point[0]
                    # pos[1] = point[1]
                    # pos[2] = point[2]
                    self.robot.movep(point, acc=a, vel=v, wait=False)
                    # print(point)
                    time.sleep(self.th)
                else:
                    time.sleep(0.1)
            else:
                # self.robot.stopl(0.5)
                time.sleep(0.2)
        self.robot.stopl(0.5)
        self.robot.close()
        print("robot stop")


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    #
    # robot = urx.Robot("192.168.1.3")
    # # rob = urx.Robot("localhost", use_simulation=True)
    #
    # robot.set_tcp((0, 0, 0, 0, 0, 0))
    # robot.set_payload(0.5, (0, 0, 0))
    # try:
    #     v = 0.5
    #     a = 0.3
    #     r = 0.01
    #
    #     init_position = robot.getj()
    #     print("Initial joint position is ", init_position)
    #
    #     transform = robot.get_pose()
    #     print("Transformation from base to tcp is: ", transform)
    #
    #     pos = robot.getl()
    #     pos[2] -= 0.02
    #
    #     print("Moving to position 1")
    #     robot.movel(pos, acc=a, vel=v, wait=False, relative=False)
    #
    #     pos[2] += 0.02
    #     print("Moving to position 2")
    #     robot.movel(pos, acc=a, vel=v)
    #     pos[2] -= 0.02
    #
    #     print("Moving to position 1")
    #     robot.movel(pos, acc=a, vel=v)
    #
    #     pos[2] += 0.02
    #     print("Moving to position 2")
    #     robot.movel(pos, acc=a, vel=v)
    #     pos[2] -= 0.02
    #     print("Moving to position 1")
    #     robot.movel(pos, acc=a, vel=v)
    #
    #     pos[2] += 0.02
    #     print("Moving to position 2")
    #     robot.movel(pos, acc=a, vel=v)
    # #
    # finally:
    #     robot.close()

    #
    robot = UR3("192.168.1.3", track_threshold=0.1, payload=0.5)
    robot.start()
    time.sleep(1)
    print(robot.robot.getl())
    time.sleep(3)
    robot.stop()


