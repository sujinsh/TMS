using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;   //必须添加，不然DllImport报错

namespace NbtRobot
{
    public class Nrc
    {
        private const String NBT_CON_DLL_NAME = "nrc_dll.dll";

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern bool connect_robot([MarshalAs(UnmanagedType.LPStr)]string ip);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern bool servo_power_on();

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void servo_power_off();

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void get_current_position([MarshalAs(UnmanagedType.LPArray,SizeConst = 6)] double[] pos, int coord); 

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void get_current_sync_position([MarshalAs(UnmanagedType.LPArray, SizeConst = 5)] double[] pos);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void robot_movj([MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos, int vel, int coord);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void robot_movl([MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos, int vel, int coord);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void robot_movc([MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos1, [MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos2, [MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos3, int vel, int coord);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void robot_movca([MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos1, [MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos2, [MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos3, int vel, int coord);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void start_jogging(int axis ,bool dir);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void stop_jogging(int axis);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern int get_robot_running_state();

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void set_jogging_speed(int speed);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern int get_jogging_speed();

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void set_dout(int port, int value);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void set_aout(int port, double value);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void get_dout(double[] dout);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void get_din(double[] din);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void get_aout(double[] aout);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void get_ain(double[] ain);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern int get_current_mode();

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void set_current_mode(int mode);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern int get_current_coord();

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void set_current_coord(int coord);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void upload_job();

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void run_job(string job);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void stop_job();

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void continuous_motion_mode(int on);

        [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void send_continuous_motion_queue([In, Out]cmdPara[] cmd , int size);


        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
        public struct cmdPara
        {
            public enum Type { MOVJ = 1, MOVL, MOVC, MOVCA, MOVJEXT, MOVLEXT, MOVCEXT};
            public double m_velocity;
            public double m_acc;
            public double m_dec;
            public double m_pl;
            public int m_spin;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 7)]
            public double[] m_coord;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 7)]
            public double[] m_position;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 5)]
            public double[] m_syncPosition;
            public Type cmdType;
        }
    }
}
