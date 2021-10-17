using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO.Ports;
using EasyModbus;
using NbtRobot;
using System.IO;
using System.Threading;
using System.Numerics;
namespace InexRobot
{
    class FT300
    {
        ModbusClient modbusClient;
        private int BYTESIZE;
        private int TIMEOUT;
        private string PORTNAME;
        private int BAUDRATE = 19200;   // 波特率
        private float Fx, last_fx, Fy, last_fy, Fz, last_fz, Mx, last_mx, My, last_my, Mz, last_mz, tempFx, tempFy, tempFz, tempMx, tempMy, tempMz;
        public bool flag, isCalflag;
        private static object obj = new object();
        private Queue<Vector3> sensorValue = new Queue<Vector3>();
        private int maxCount = 10;
        public FT300()
        {
            BYTESIZE = 8;
            TIMEOUT = 500;
            PORTNAME = "COM11";
            BAUDRATE = 19200;
            Fx = 0.0F; Fy = 0.0F; Fz = 0.0F;
            Mx = 0.0F; My = 0.0F; Mz = 0.0F;
            tempFx = 0.0F; tempFy = 0.0F; tempFz = 0.0F;
            tempMx = 0.0F; tempMy = 0.0F; tempMz = 0.0F;
            flag = isCalflag = false;
            last_fx = last_fy = last_fz = last_mx = last_my = last_mz = 0.0F;

            // 队列初始化
            for(int i = 0; i<10;i++)
            {
                sensorValue.Enqueue(new Vector3(0.0f, 0.0f, 0.0f));
            }
        }

        // 使用FT300传感器前需调用以下方法，传感器数据模式为458
        public void ConvertMode()
        {
            SerialPort port = new SerialPort(PORTNAME);
            port.BaudRate = BAUDRATE;
            port.Parity = Parity.None;
            port.StopBits = StopBits.One;
            try
            {
                byte[] off = new byte[] { 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff };
                port.Open();
                port.Write(off, 0, off.Length);
                port.Close();
                System.Diagnostics.Debug.WriteLine("转换模式");

            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine("FT300 转换模式失败");
                System.Diagnostics.Debug.WriteLine(ex.ToString());
            }

        }

        // 寄存器数据CRC校验
        public static void CRCgenerate(byte[] message, int length, out byte CRCHigh, out byte CRCLow)
        {
            ushort CRCFull = 0xFFFF;
            for (int i = 0; i < length; i++)
            {
                CRCFull = (ushort)(CRCFull ^ message[i]);
                for (int j = 0; j < 8; j++)
                {
                    if ((CRCFull & 0x0001) == 0)
                        CRCFull = (ushort)(CRCFull >> 1);
                    else
                    {
                        CRCFull = (ushort)((CRCFull >> 1) ^ 0xA001);
                    }
                }
            }
            CRCHigh = (byte)((CRCFull >> 8) & 0xFF);
            CRCLow = (byte)(CRCFull & 0xFF);
        }

        //　读寄存器数据
        public static byte[] readHoldingRegister(int id, int startAddress, int Length)
        {
            byte[] data = new byte[8];
            byte High, Low;

            data[0] = Convert.ToByte(id);
            data[1] = Convert.ToByte(3);

            byte[] _adr = BitConverter.GetBytes(startAddress);

            data[2] = _adr[1];
            data[3] = _adr[0];

            byte[] _length = BitConverter.GetBytes(Length);

            data[4] = _length[1];
            data[5] = _length[0];

            CRCgenerate(data, 6, out High, out Low);

            data[6] = Low;
            data[7] = High;

            //Array.Reverse(data);
            return data;
        }

        // 数据提取
        public byte[] ReadExact(Stream s, int nbytes)
        {
            byte[] buf = new byte[nbytes];
            var readpos = 0;

            while (readpos < nbytes)
            {
                readpos += s.Read(buf, readpos, nbytes - readpos);
            }
            return buf;
        }

        //　写寄存器
        public void writeRegister()
        {
            ModbusClient modbusClient = new ModbusClient(PORTNAME);
            try
            {
                modbusClient.UnitIdentifier = 9;   //SLAVEADDRESS
                modbusClient.Baudrate = BAUDRATE;   //BAUDRATE
                modbusClient.Parity = Parity.None;
                modbusClient.StopBits = StopBits.One;
                modbusClient.ConnectionTimeout = 1;
                modbusClient.Connect();
                modbusClient.WriteSingleRegister(410, 0x0200);
                modbusClient.Disconnect();
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine("初始化错误");
                System.Diagnostics.Debug.WriteLine(ex.ToString());
            }

        }

        //　传感器数据初始化
        public void Init()
        {

            try
            {
                modbusClient = new ModbusClient(PORTNAME);
                modbusClient.UnitIdentifier = 9;   //SLAVEADDRESS
                modbusClient.Baudrate = BAUDRATE;   //BAUDRATE
                modbusClient.Parity = Parity.None;
                modbusClient.StopBits = StopBits.One;
                modbusClient.ConnectionTimeout = TIMEOUT;
                modbusClient.Connect();
                int[] temp = modbusClient.ReadHoldingRegisters(180, 6); // ReadHoldingRegister from 180, Total registers read = 6
                tempFx = Convert.ToSingle(temp[0]) / 100;
                tempFy = Convert.ToSingle(temp[1]) / 100;
                tempFz = Convert.ToSingle(temp[2]) / 100;
                tempMx = Convert.ToSingle(temp[3]) / 1000;
                tempMy = Convert.ToSingle(temp[4]) / 1000;
                tempMz = Convert.ToSingle(temp[5]) / 1000;
                System.Diagnostics.Debug.WriteLine("传感器初始化结束");
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(ex.ToString());
            }
        }

        //　读取寄存器数据
        public void ReadRegister()
        {
            int[] recdata = new int[6] { 0, 0, 0, 0, 0, 0 };
            while (flag)
            {
                try
                {
                    if (isCalib())
                    {
                        Thread.Sleep(500);
                    }
                    lock (obj)
                    {
                        last_fx = Fx; last_fy = Fy; last_fz = Fz;
                        recdata = modbusClient.ReadHoldingRegisters(180, 6); // ReadHoldingRegister from 180, Total registers read = 6
                        Fx = Convert.ToSingle(recdata[0]) / 100 - tempFx;
                        Fy = Convert.ToSingle(recdata[1]) / 100 - tempFy;
                        Fz = Convert.ToSingle(recdata[2]) / 100 - tempFz;
                        Mx = Convert.ToSingle(recdata[3]) / 1000 - tempMx;
                        My = Convert.ToSingle(recdata[4]) / 1000 - tempMy;
                        Mz = Convert.ToSingle(recdata[5]) / 1000 - tempMz;
                    }
                    Thread.Sleep(10);
                    System.Diagnostics.Debug.Write($"\tfx:" + Fx.ToString());
                    System.Diagnostics.Debug.Write($"\tfy:" + Fy.ToString());
                    System.Diagnostics.Debug.Write($"\tfz:" + Fz.ToString());
                    System.Diagnostics.Debug.Write($"\tmx:" + Mx.ToString());
                    System.Diagnostics.Debug.Write($"\tmy:" + My.ToString());
                    System.Diagnostics.Debug.Write($"\tmz:" + Mz.ToString());
                    System.Diagnostics.Debug.Write($"\n");
                    if(sensorValue.Count <= maxCount)
                    {
                        sensorValue.Enqueue(new Vector3(Fx, Fy, Fz));
                    }
                    else
                    {
                        sensorValue.Dequeue();
                        sensorValue.Enqueue(new Vector3(Fx, Fy, Fz));
                    }
                    
                }
                catch (Exception ex)
                {
                    System.Diagnostics.Debug.WriteLine("从传感器获取数据失败");
                    System.Diagnostics.Debug.WriteLine(ex.ToString());
                }
            }

        }

        // 获取当前力
        public void getForce(double[] force)
        {
            if (force.Length == 5)
            {
                force[0] = Fx;
                force[1] = Fy;
                force[2] = Fz;
                force[3] = Mx;
                force[4] = My;
                force[5] = Mz;

            }
            else if (force.Length == 3)
            {
                force[0] = Fx;
                force[1] = Fy;
                force[2] = Fz;
            }
            else
            {
                System.Diagnostics.Debug.WriteLine("形参错误");
                return;
            }
            
        }

        //　检测是否发生碰撞
        public bool isCalib()
        {
            //double value = 0;
            //List<double> values = new List<double>();
            //foreach (Vector3 force in sensorValue)
            //{
            //    value = Math.Pow(force.X,2)+ Math.Pow(force.Y , 2)+ Math.Pow(force.Z , 2);
            //    values.Add(value);
            //}
            //if((values.Max() - values.Min())> 2 && (values.IndexOf(values.Max())- values.IndexOf(values.Min()))>0)
            //// t 时刻中 队列中的最大最小值之间的差值大于2 且 最大值的index 大于 最小值的index
            //{
            //    isCalflag = true;
            //    return true;
            //}
            //else
            //{
            //    isCalflag = false;
            //    return false;
            //}
            lock (obj)
            {
                if (Math.Abs(Fz) > 2)
                {
                    isCalflag = true;
                    return true;
                }
                else
                {
                    isCalflag = false;
                    return false;
                }
            }
        }
    }


    //class Program
    //{
    //    static void Main(string[] args)
    //    {
    //        string path = "./record.txt";
    //        FT300 ft300 = new FT300();
    //        ft300.ConvertMode();
    //        Nrc.connect_robot("192.168.1.13");
    //        Thread.Sleep(200);
    //        Nrc.servo_power_on();
    //        Thread.Sleep(200);
    //        Nrc.set_jogging_speed(40);
    //        Thread.Sleep(200);
    //        double[] loc = new double[6];
    //        double[] pos = new double[6];
    //        String str;
    //        //double[] force = new double[6];
    //        Nrc.set_current_coord(0);
    //        //Nrc.get_current_position(loc, 0);
    //        double[] init = new double[6] { 60.0, 0, 0, 0, 0, 0 };
    //        using (StreamWriter sw = new StreamWriter(path))
    //        {
    //            Nrc.robot_movj(init, 20, 0);
    //            //loc = init;
    //            Thread.Sleep(2000);
    //            ft300.Init();
    //            ft300.Start();          // 获取力                  
    //            Nrc.get_current_position(loc, 0);  //获取关节坐标系下的位置
    //            Thread.Sleep(2000);
    //            Nrc.get_current_position(pos, 1);  //获取直角坐标系下的位置
    //            str = pos[0].ToString() + "//" + pos[1].ToString() + "//" + pos[2].ToString() + "//" + pos[3].ToString() + "//" + pos[4].ToString() + "//" + pos[5].ToString()
    //                + "//" + loc[0].ToString() + "//" + loc[1].ToString() + "//" + loc[2].ToString() + "//" + loc[3].ToString() + "//" + loc[4].ToString() + "//" + loc[5].ToString()
    //                + "//" + ft300.Fx.ToString() + "//" + ft300.Fy.ToString() + "//" + ft300.Fz.ToString() + "//" + ft300.Mx.ToString() + "//" + ft300.My.ToString() + "//" + ft300.Mz.ToString();
    //            Console.WriteLine(str);
    //            sw.WriteLine(str);
    //            for (int j = 0; j < 2; j++)
    //            {
    //                init[4] = init[5] = 0;
    //                for (int i = 0; i < 10; i++)
    //                {
    //                    init[4 + j] = 18 * i;
    //                    Nrc.robot_movj(init, 20, 0);
    //                    Thread.Sleep(12000);
    //                    ft300.Start();          // 获取力     
    //                    Thread.Sleep(2000);
    //                    Nrc.get_current_position(loc, 0);
    //                    Thread.Sleep(2000);
    //                    Nrc.get_current_position(pos, 1);
    //                    var rx = Matrix4x4.CreateRotationX((float)pos[3]);
    //                    var ry = Matrix4x4.CreateRotationY((float)pos[4]);
    //                    var rz = Matrix4x4.CreateRotationZ((float)pos[5]);
    //                    var rot = rz * ry * rx;
    //                    var G = new Vector4(-0.37659331f, -0.09286962f, 3.50626647f, 1);
    //                    var F0 = new Vector4(2.18981988f, -0.05260437f, 4.52892189f, 0);
    //                    Console.WriteLine(Vector4.Transform(G, rot) + F0);
    //                    Console.WriteLine(Vector4.Transform(G, Matrix4x4.Transpose(rot)) + F0);
    //                    Thread.Sleep(2000);
    //                    str = $"{string.Join("//", pos)}//{string.Join("//", loc)}//{ft300.Fx}//{ft300.Fy}//{ft300.Fz}//{ft300.Mx}//{ft300.My}//{ft300.Mz}";
    //                    //Console.WriteLine(str);
    //                    //sw.WriteLine(str);
    //                }
    //            }
    //            sw.Flush();
    //            sw.Close();
    //        }

    //        //while (true)
    //        //{
    //        //    ft300.Start();
    //        //}
    //        Nrc.servo_power_off();

    //    }
    //}
}

