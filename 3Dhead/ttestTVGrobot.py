import threading
import time
import serial
import math

class TVGserial(threading.Thread):
    """
    机器人姿态：
    A: 末端向量在XOY平面投影与x的夹角，正负与Y同号　[-180,180]
    B: 末端向量与Z的夹角　[-180,180]
    C: 末端向量自身的旋转角度  [-359,359]
    """
    def __init__(self, com="COM5", baud=115200):
        threading.Thread.__init__(self)
        self.currdata = []
        self.data = ""
        self.com = com
        self.baud = baud
        self.ser = None
        self.flag = False
        self.moving = False

    def set_com(self, com):
        # 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
        self.com = com

    def set_baud(self, baud):
        # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
        self.baud = baud

    def send_cmd(self, cmd):
        # 暂停 退出 示教 重启 复位 运行
        if cmd == "zt":
            self.pauseTVG()
        elif cmd == "tc":
            self.exitTVG()
        elif cmd == "sj":
            self.teachTVG()
        elif cmd == "cq":
            self.restartTVG()
        elif cmd == "fw":
            self.resetTVG()
        elif cmd == "yx":
            self.runTVG()

    def restartTVG(self):
        # 重启   将当前位置作为初始位
        self.DWritePort('\x18')

    def pauseTVG(self):
        # 暂停
        self.DWritePort('\x30')

    def exitTVG(self):
        # 退出
        self.DWritePort('\x10')

    def teachTVG(self):
        # 示教   进入示教模式
        self.DWritePort('\x14')

    def resetTVG(self):
        # 复位   机器人回到初始位
        self.DWritePort('\x15')

    def runTVG(self):
        # 运行   跑机器人内部写好的程序
        self.DWritePort('\x13')

    def intofollowTVG(self, speed=5):
        # 进入跟随模式
        self.pauseTVG()
        time.sleep(0.05)
        self.exitTVG()
        time.sleep(0.05)
        self.teachTVG()
        time.sleep(0.05)
        self.setSpeedTVG(speed)
        time.sleep(0.05)
        self.DWritePort("G14 G15 FOLLOW CMP G15 FOLLOW")  # 成功返回YYYY, 异常返回NNNN

    def exitfollowTVG(self):
        self.pauseTVG()
        time.sleep(0.05)
        self.DWritePort("G15 EXIT FOLLOW")

    def setSpeedTVG(self, speed):
        # 设置速度 speed% * vpp （示教模式）
        self.DWritePort("G07 VP="+str(speed))

    def movepGlineTVG(self, pos, Gline="G21", wait=True):
        # 走直线 (需要进入示教模式)
        # G21  G10  G40  G41
        cmd = ""
        # if not wait:
        #     cmd += "\14"
        cmd += Gline
        cmd += " X=" + str(round(pos[0], 1))
        cmd += " Y=" + str(round(pos[1], 1))
        cmd += " Z=" + str(round(pos[2], 1))
        if len(pos) > 3:
            cmd += " A=" + str(round(pos[3], 0))
            cmd += " B=" + str(round(pos[4], 0))
            cmd += " C=" + str(round(pos[5], 0))
            # pass
        self.moving = True
        self.DWritePort(cmd)

    def jogTVG(self, joint, dir):
        # 点动 （示教模式）
        # joint = ”J0“, "J1", "J2"..."TX", "TZ", "TA"...
        # dir = "+", "-"
        if joint[0] in ("J", "T") and dir in ("+", "-"):
            self.moving = True
            cmd = joint + dir
            self.DWritePort(cmd)
            # time.sleep(0.07)
            # self.pauseTVG()

    def eeNormal2ABC(self, normal):
        nx, ny, nz = normal[0], normal[1], normal[2]
        A = math.atan2(ny, nx)
        lxy = math.sqrt(nx*nx + ny*ny)
        # lxyz = math.sqrt(nz*nz + lxy*lxy)
        B = math.acos(nz)

        C = 0

        A, B, C = round(A*180/math.pi, 1), round(B*180/math.pi, 1), round(C*180/math.pi, 1)
        return [A, B, C]

    def get_data(self):
        # return list(self.q)
        return self.data

    def stop(self):
        self.flag = False

    # 读串口数据
    def run(self):
        self._DOpenPort(timeout=3)
        # 循环接收数据
        print(":::")
        while self.flag:
            if self.ser is not None and self.ser.in_waiting:
                self.data = self.ser.read(self.ser.in_waiting)
                self.moving = False
                # print(self.data)
            else:
                time.sleep(0.2)
        print("serial stop")

    # 打开串口
    # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
    def _DOpenPort(self, timeout):
        if self.ser is not None and self.ser.is_open:
            return True
        try:
            # 打开串口，并得到串口对象
            print("打开串口 port:", self.com, " baud:", self.baud, "timeout:", timeout)
            self.ser = serial.Serial(self.com, self.baud, timeout=timeout)
            # 判断是否打开成功
            if (self.ser.is_open):
                self.flag = True
                print("---成功---")
                return True
        except Exception as e:
            print("---异常---：", e)
        return False

    # 关闭串口
    def DColsePort(self):
        self.flag = False
        if self.ser:
            self.ser.close()
        print("关闭串口")
        self.ser = None

    # 写串口数据
    def DWritePort(self, text):
        if not self.ser.is_open:
            return -1
        text += "\r\n"
        result = self.ser.write(text.encode("utf-8"))  # 写数据
        return result


if __name__ == "__main__":
    tvg = TVGserial("COM5", 115200)

    tvg.start()
    time.sleep(1)
    while True:
        cmd = input("输入指令 暂停z 退出t 复位f 重启c 示教s 运行r 走直线m：")
        print()
        if cmd == 'z':
            tvg.pauseTVG()
        elif cmd == 't':
            tvg.exitTVG()
        elif cmd == 'f':
            tvg.resetTVG()
        elif cmd == 'c':
            tvg.restartTVG()
        elif cmd == 's':
            tvg.teachTVG()
        elif cmd == 'r':
            tvg.runTVG()
        elif cmd == 'm':
            pos = [300.9996, -100.0137, 269.6439, -0.9037, 160.6188, 0.0037, 0]
            tvg.movepGlineTVG(pos)
        elif cmd == 'q':
            tvg.stop()
            break
    print("end")
