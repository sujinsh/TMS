using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Sockets;
using System.IO;
using System.Threading;
using NbtRobot;
using System.Diagnostics;

namespace InexRobot
{
    public struct MyPos
    {
        public double x, y, z, rx, ry, rz;
        public MyPos(double tx, double ty, double tz, double trx, double t_ry, double trz)
        {
            x = tx; y = ty; z = tz; rx = trx; ry = t_ry; rz = trz;
        }
        public override String ToString()
        {
            return x + "," + y + "," + z + "," + rx + "," + ry + "," + rz;
        }
    }
 
    public partial class Form1 : Form
    {
        const double pi = Math.PI;
        const string tcp_ip = "127.0.0.1";
        const int tcp_port = 9000;
        const string robot_ip = "192.168.1.13";
        const int coord = 2;    //直角坐标系
        public int speed = 10;         // 插值速度
        NetworkStream sendStream;
        TcpClient client;
        MyPos target_position;
        FT300 sensor;
        MyPos init_position = new MyPos(474.0, -54.0, 325.0, pi, 0, -0.251);
        private static object obj = new object();   // 互斥锁
        private bool server_connected_flag = false; // 连接服务器标志
        private bool robot_follow_flag = false;    // 启动跟踪标志
        private bool robot_connect_flag = false;  // 机器人连接标志
        private bool is_use_force_sensor_flag = false; // 启用力传感器标志

        public Form1()
        {
            InitializeComponent();
            target_position = init_position;
            txt_x.Text = init_position.x + "";
            txt_y.Text = init_position.y + "";
            txt_z.Text = init_position.z + "";
            txt_rx.Text = init_position.rx + "";
            txt_ry.Text = init_position.ry + "";
            txt_rz.Text = init_position.rz + "";
            refreshWindows();
        }
        /// <summary>
        /// 点击事件 连接机器人
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnConnnect_Click(object sender, EventArgs e)
        {
            if(robot_connect_flag)
            {
                MessageBox.Show("Robot Already Connected");
                return;
            }
            if (Nrc.connect_robot(robot_ip))
            {
                Debug.WriteLine("连接成功");
                robot_connect_flag = true;
            }
            else
            {
                Debug.WriteLine("连接失败");
                MessageBox.Show("robot connecte failed!");
                robot_connect_flag = false;
                return;
            }
            if (Nrc.get_current_coord() != coord)
            {
                Nrc.set_current_coord(coord);
            }
            Nrc.set_jogging_speed(25);
            Nrc.set_current_mode(0); // 示教模式
            Nrc.servo_power_on();
            refreshWindows();
            MessageBox.Show("robot connected!");
            
        }
        /// <summary>
        /// 点击事件 启动跟踪线程
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnMove_Click(object sender, EventArgs e)
        {
            if (robot_follow_flag || !robot_connect_flag)
            {
                MessageBox.Show("Turn on Robot Connect Or Robot is Moving");
                return;
            }
            // 启动跟踪前 检测传感器是否打开
            if( !is_use_force_sensor_flag )
            {
                MessageBox.Show("Turn on Force Sensor");
                return;
            }
            Thread th = new Thread(Run);
            robot_follow_flag = true;
            th.Start();         
            robot_connect_flag = true;
            refreshWindows();
        }
        /// <summary>
        /// 点击事件  退出程序
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnClosed(object sender, EventArgs e)
        {
            stop_all();
            MessageBox.Show("stop all !");
        }

        public MyPos lerp_hand(MyPos current_pos, MyPos target_pos)   // 目标位置与当前位置之间的插值 插值因子为intervel
        {
            double intervel = 0.5;
            double dist = distance(current_pos, target_pos);
            if( dist <50)   // 移动距离小于5 cm 
            {
                speed = 50;
                Nrc.set_jogging_speed(10);
                return target_pos;
            }
            else    // 移动距离 大于5 cm
            {
                speed = 75;
                Nrc.set_jogging_speed(30);
                intervel = 0.2;
               
            }
            current_pos.x += intervel * (target_pos.x - current_pos.x);
            current_pos.y += intervel * (target_pos.y - current_pos.y);
            current_pos.z += intervel * (target_pos.z - current_pos.z);
            return current_pos;   
        }
        /// <summary>
        /// 两个pos之间的距离
        /// </summary>
        /// <param name="current_pos"></param>
        /// <param name="target_pos"></param>
        /// <returns></returns>
        public double distance(MyPos current_pos, MyPos target_pos)
        {
            refreshWindows();
            double dx = target_pos.x - current_pos.x;
            double dy = target_pos.y - current_pos.y;
            double dz = target_pos.z - current_pos.z;
            double dist = Math.Sqrt(dx*dx + dy*dy + dz*dz);
            return dist;
        }
 
        /// <summary>
        /// 机器人跟踪程序 线程
        /// </summary>
        public void Run()  
        {
            MyPos p = new MyPos();
            MyPos tar_copy = new MyPos();
            MyPos next_position;
            MyPos current_position;
            while (robot_follow_flag)
            {
                // 目标位置 => tar_copy
                //Debug.WriteLine(sensor.isCalflag.ToString());
                refreshWindows();
                if (sensor.isCalflag)
                {
                    robot_follow_flag = false;                                      
                    Debug.WriteLine("发生碰撞");
                }
                else
                {
                    
                    lock (obj)
                    {
                        tar_copy = target_position;
                    }
                    Debug.WriteLine("target_position:" + tar_copy.ToString());

                    if (tar_copy.x == 0 && tar_copy.y == 0 && tar_copy.z == 0)
                    {
                        Debug.WriteLine("error -0-0-0-");
                        Thread.Sleep(200);
                        continue;
                    }
                    // 当前位置 => current_position
                    double[] cur_pos = new double[6];
                    Nrc.get_current_position(cur_pos, coord);
                    current_position.x = cur_pos[0]; current_position.y = cur_pos[1]; current_position.z = cur_pos[2];
                    current_position.rx = cur_pos[3]; current_position.ry = cur_pos[4]; current_position.rz = cur_pos[5];
                    Debug.WriteLine("current_position:" + current_position.ToString());
                    double dis = distance(current_position, tar_copy);
                    if (dis < 20)
                    {
                        Debug.WriteLine("--");
                        Thread.Sleep(200);
                        continue;
                    }
                    //Debug.WriteLine("Distance between Cur & Tar"+ dis);
                    // 插值 => next_position => position
                    next_position = lerp_hand(current_position, tar_copy);

                    double[] position = new double[6];
                    position[0] = next_position.x; position[1] = next_position.y; position[2] = next_position.z;
                    position[3] = next_position.rx; position[4] = next_position.ry; position[5] = next_position.rz;

                    if (Nrc.get_robot_running_state() != 2)
                    {
                        Debug.WriteLine("走");
                        Debug.WriteLine("next_position:" + next_position.ToString());
                        Nrc.robot_movl(position, speed, coord);
                    }
                    else
                    {
                        Debug.WriteLine("不走");
                    }
                    Thread.Sleep(200);
                    //current_position.x = next_position.x; current_position.y = next_position.y; current_position.z = next_position.z;

                }

            }
            Debug.WriteLine("机器人跟踪线程 退出");
            //stateDisplayLabel.Text = "结束跟踪";
        }


        /// <summary>
        /// 读取server消息 线程
        /// </summary>
        public void Read_TCPClient()
        {
            try
            {
                while (server_connected_flag)
                {
                    byte[] readbyte = new byte[1024];
                    sendStream.Read(readbyte, 0, 4);
                    int len = BitConverter.ToInt32(readbyte, 0);
                    sendStream.Read(readbyte, 0, len);

                    //sendStream.Read(readbyte, 0, 1024);
                    //string recMes = Encoding.ASCII.GetString(readbyte);
                    string recMes = Encoding.ASCII.GetString(readbyte, 0, len);
                    string[] res = recMes.Split(',');
                    float x = Convert.ToSingle(res[0]) * 1000;
                    float y = Convert.ToSingle(res[1]) * 1000;
                    float z = Convert.ToSingle(res[2]) * 1000;
                    float rx = Convert.ToSingle(res[3]);
                    float ry = Convert.ToSingle(res[4]);
                    float rz = Convert.ToSingle(res[5]);
                    //Debug.WriteLine("读数据");
                    //Debug.WriteLine(x);
                    lock (obj)
                    {
                        target_position.x = x;
                        target_position.y = y;
                        target_position.z = z;
                        target_position.rx = rx;
                        target_position.ry = ry;
                        target_position.rz = rz;
 
                    }
                    Debug.WriteLine(target_position.ToString());

                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"TCP Read error: {ex.Message}");
            }
            Debug.WriteLine("读数据线程退出");
        }

        private void button4_Click(object sender, EventArgs e)
        {
            Nrc.servo_power_on();
            robot_connect_flag = true;
        }
        /// <summary>
        /// 急停
        /// </summary>
        private void btn_emergencyStop(object sender, EventArgs e)
        {
            Nrc.servo_power_off();
            
        }

        /// <summary>
        /// 点击关闭按钮
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            stop_all();
            //MessageBox.Show("close!");
        }

        /// <summary>
        /// 点击事件 连接服务器
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btn_connect_server_Click(object sender, EventArgs e)
        {
            try
            {
                if (!server_connected_flag)
                {
                    client = new TcpClient(tcp_ip, tcp_port);
                    sendStream = client.GetStream();
                    server_connected_flag = true;
                    Thread th = new Thread(Read_TCPClient);
                    th.Start();
                    MessageBox.Show("Server connected!");
                    btn_connect_server.Text = "服务器断开";
                }
                else
                {
                    sendStream.Close();
                    client.Close();
                    server_connected_flag = false;
                    btn_connect_server.Text = "服务器连接";
                    MessageBox.Show("Server connect closed!");
                }
                refreshWindows();
            }
            catch
                {
                    server_connected_flag = false;
                    MessageBox.Show("server connect ERROR!");
                }
            }
        /// <summary>
        ///  刷新界面
        /// </summary>
        private void refreshWindows()
        {
                if(server_connected_flag)
                {
                    label8.Text = "连接";
                }
                else
                {
                    label8.Text = "断开";
                }
                if(robot_connect_flag)
                {
                    label10.Text = "连接";
                }
                else
                {
                    label10.Text = "断开";
                }
                if(robot_follow_flag)
                {
                    label12.Text = "跟踪";
                }
                else
                {
                    label12.Text = "非跟踪";
                }
                if(is_use_force_sensor_flag)
                {
                    label14.Text = "打开";
                }
                else
                {
                    label14.Text = "关闭"; 
                }
                //Thread.Sleep(100);
        }

        /// <summary>
        /// 点击事件 连接或启用传感器
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btn_close_connect_Click(object sender, EventArgs e)
        {
            try
            {
                if (!is_use_force_sensor_flag)
                {
                    // 传感器初始化
                    sensor = new FT300();
                    sensor.ConvertMode();
                    sensor.Init();
                    sensor.flag = true;
                    sensor.isCalflag = false;
                    Thread sh = new Thread(sensor.ReadRegister);
                    sh.Start();                    
                    is_use_force_sensor_flag = true;
                    btn_close_connect.Text = "关闭传感器";
                    MessageBox.Show("开启传感器");
                }
                else
                {
                    sensor.flag = false;
                    is_use_force_sensor_flag = false;
                    btn_close_connect.Text = "传感器打开";               
                    MessageBox.Show("关闭传感器");
                }
                refreshWindows();
            }
            catch
            {
                is_use_force_sensor_flag = false;
                MessageBox.Show("Force sensor is closed");   
            }
        }
        // 关闭所有
        public void stop_all()
        {
            if (server_connected_flag)
            {
                sendStream.Close();
                client.Close();
                server_connected_flag = false;
                btn_connect_server.Text = "服务器连接";
            }
            robot_follow_flag = false;
            if(is_use_force_sensor_flag)
            {
                sensor.flag = false;
                is_use_force_sensor_flag = false;
                btn_close_connect.Text = "传感器打开";
                MessageBox.Show("关闭传感器");
            }
            
            while (robot_connect_flag)
            {
                if (Nrc.get_robot_running_state() != 2)
                {

                    Nrc.servo_power_off(); // 关闭电机使能
                    robot_connect_flag = false;
                }
            }
           
        }
        // 点动到指定点
        private void button6_Click(object sender, EventArgs e)
        {
            if(!robot_connect_flag || robot_follow_flag)
            { return; }
            float x = Convert.ToSingle(txt_x.Text) ;
            float y = Convert.ToSingle(txt_y.Text) ;
            float z = Convert.ToSingle(txt_z.Text) ;
            float rx = Convert.ToSingle(txt_rx.Text);
            float ry = Convert.ToSingle(txt_ry.Text);
            float rz = Convert.ToSingle(txt_rz.Text);
            if (Nrc.get_robot_running_state() != 2)
            {
                Debug.WriteLine("走");
                double[] position = { x, y, z, rx, ry, rz };
                Nrc.set_jogging_speed(30);
                Nrc.robot_movl(position, speed, coord);
            }
            else
            {
                Debug.WriteLine("不走");
            }
        }
        // 点动到初始位
        private void btn_reset_Click(object sender, EventArgs e)
        {
            if (!robot_connect_flag || robot_follow_flag)
            { return; }
            if (Nrc.get_robot_running_state() != 2)
            {
                Debug.WriteLine("走初始位");
               
                double[] position = { init_position.x, init_position.y, init_position.z,
                    init_position.rx, init_position.ry, init_position.rz };
                Nrc.set_jogging_speed(35);
                Nrc.robot_movl(position, speed, coord);
            }
            else
            {
                Debug.WriteLine("不走");
            }
        }
        // 结束跟踪
        private void button7_Click(object sender, EventArgs e)
        {
            robot_follow_flag = false;
            refreshWindows();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void label7_Click(object sender, EventArgs e)
        {

        }

        private void label11_Click(object sender, EventArgs e)
        {

        }

        private void label10_Click(object sender, EventArgs e)
        {

        }

        //public void Write_TCPClient(string data)  //写回TCP
        //{
        //    if (flag == false)
        //        return;
        //    byte[] sendBytes = Encoding.Default.GetBytes(data);
        //    sendStream.Write(sendBytes, 0, sendBytes.Length);
        //}
    }
}
