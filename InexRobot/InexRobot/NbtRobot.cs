using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Diagnostics;


namespace NbtRobot
{
    public class NbtRobot
    {
        private string IP;
        public bool jog;

        public NbtRobot(string ip)
        {
            this.IP = ip;
            if (Nrc.connect_robot(IP))
            {
                Debug.WriteLine("连接机器人成功");
            }
            else
            {
                Debug.WriteLine("连接机器人失败");
            }
        }


        public void servo_power_on()
        {
            if (Nrc.servo_power_on())
            {
                Debug.WriteLine("server on");
            }
            else
            {
                Debug.WriteLine("error: server not on");
            }
        }

        public void servo_power_off()
        {
            Nrc.servo_power_off();
        }
        
        public void start_jogging_n(int axis)
        {
            // 反向jog

            Nrc.start_jogging(axis,false);
        }

        public void start_jogging_p(int axis)
        {
            // 正向jog
            Nrc.start_jogging(axis,true);
        }

        public void stop_jogging(int axis)
        {
            Nrc.stop_jogging(axis);
        }

        public void get_current_position(double[] d,int coord)
        {
            Nrc.get_current_position(d,coord);
        }

        public void get_current_sync_position(double[] d)
        {
            Nrc.get_current_sync_position(d);
        }

        public int get_robot_state()
        {
            return Nrc.get_robot_running_state();
        }

        public void set_jogging_speed(int speed)
        {
            Nrc.set_jogging_speed(speed);
        }

        public int get_jogging_speed()
        {
            return Nrc.get_jogging_speed();
        }


        // 不使用
        public void set_dout(int port, int value)
        {
            Nrc.set_dout(port, value);
        }

        public void set_aout(int port, double value)
        {
            Nrc.set_aout(port, value);
        }

        public void get_dout(double[] dout)
        {
            Nrc.get_dout(dout);
        }

        public void get_din(double[] din)
        {
            Nrc.get_din(din);
        }

        public void get_aout(double[] aout)
        {
            Nrc.get_aout(aout);
        }

        public void get_ain(double[] ain)
        {
            Nrc.get_ain(ain);
        }

        // 连续运动？
        public void continuous_motion_mode(int on)
        {
            Nrc.continuous_motion_mode(on);
        }

        public void send_continuous_motion_queue(Nrc.cmdPara[] cmd,int size)
        {
            Nrc.send_continuous_motion_queue(cmd, size);
        }

        public bool MovJ(JointPos pos,int vel,int coord)
        {
            Nrc.robot_movj(pos.TranArray(),vel,coord);
            return true;
        }

        public bool MovL(JointPos pos,int vel,int coord)
        {
            Nrc.robot_movl(pos.TranArray(),vel ,coord);
            return true;
        }

        public bool MovC(double[] pos1, double[] pos2, double[] pos3, int vel, int coord)
        {
            Nrc.robot_movc(pos1, pos2, pos3, vel, coord);
            return true;
        }

        public bool MovCA(double[] pos1, double[] pos2, double[] pos3, int vel, int coord)
        {
            Nrc.robot_movca(pos1, pos2, pos3, vel, coord);
            return true;
        }

        public void upload_job()
        {
            Nrc.upload_job();
        }

        public int get_mode()
        {
            return Nrc.get_current_mode();
        }

        public void set_mode(int mode)
        {
            Nrc.set_current_mode(mode);
        }

        public int get_coord()
        {
            return Nrc.get_current_coord();
        }

        public void set_coord(int coord)
        {
            Nrc.set_current_coord(coord);
        }

        public void run_job(string job)
        {
            Nrc.run_job(job);
        }
        
        public void stop_job()
        {
            Nrc.stop_job();
        }
    }

    public class JointPos
    {
        public JointPos() { }

        public JointPos(double[] arr)
        {
            if (arr.Length < 6) return;
            this.J1 = arr[0];
            this.J2 = arr[1];
            this.J3 = arr[2];
            this.J4 = arr[3];
            this.J5 = arr[4];
            this.J6 = arr[5];
        }
        public JointPos(double j1, double j2, double j3, double j4, double j5, double j6)
        {
            this.J1 = j1;
            this.J2 = j2;
            this.J3 = j3;
            this.J4 = j4;
            this.J5 = j5;
            this.J6 = j6;
        }
        public double J1=0;
        public double J2=0;
        public double J3=0;
        public double J4=0;
        public double J5=0;
        public double J6=0;

        public double[] TranArray()
        {
            return new double[6] { this.J1, this.J2, this.J3, this.J4, this.J5, this.J6 };
        }

        public int[] TranArray(int precision)
        {
            return new int[6] { (int)(this.J1 * (Math.Pow(10, precision))), (int)(this.J2 * (Math.Pow(10, precision))), (int)(this.J3 * (Math.Pow(10, precision))), (int)(this.J4 * (Math.Pow(10, precision))), (int)(this.J5 * (Math.Pow(10, precision))), (int)(this.J6 * (Math.Pow(10, precision))) };
        }
    }
}
