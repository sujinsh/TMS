# # import ctypes
# # import time
# # # 需要C# Demo下的dll和platforms文件夹
# # # 外面的dll直接放到此文件夹下
# # # platforms文件夹部署到conda环境的python.exe同一个目录下
# # # 此时为D:\Anaconda\envs\robot32
# # nrc = ctypes.CDLL("./nrc_dll.dll")
# #
# # nrc.connect_robot.argtypes = ctypes.c_char_p,
# # nrc.connect_robot.restype = ctypes.c_bool
# # def connect_robot(ip) -> ctypes.c_bool:
# #     #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# #     #  public static extern bool connect_robot([MarshalAs(UnmanagedType.LPStr)]string ip);
# #     return nrc.connect_robot(ctypes.c_char_p(bytes(ip, encoding="ansi")))
# #
# # nrc.servo_power_on.argtypes = None
# # nrc.servo_power_on.restype = ctypes.c_bool
# # def servo_power_on() -> ctypes.c_bool:
# #     #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# #     #  public static extern bool servo_power_on();
# #     return ctypes.c_bool(nrc.servo_power_on())
# #
# #
# # nrc.servo_power_off.argtypes = None
# # nrc.servo_power_off.restype = None
# # def servo_power_off() -> None:
# #     #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# #     #  public static extern void servo_power_off();
# #     return nrc.servo_power_off()
# #
# # nrc.get_current_position.argtypes = ctypes.POINTER(ctypes.c_double), ctypes.c_int
# # nrc.get_current_position.restype = None
# # def get_current_position(coord: int) -> "list[float]":
# #     #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# #     #  public static extern void get_current_position([MarshalAs(UnmanagedType.LPArray,SizeConst = 6)] double[] pos, int coord);
# #     pos = (ctypes.c_double * 6)()
# #     nrc.get_current_position(pos, coord)
# #     return list(pos)
# #
# #
# # if connect_robot("192.168.1.13"):
# #     print("connected")
# #     time.sleep(1)
# #     print("power =", servo_power_on())
# #     time.sleep(1)
# #     print("pos =", get_current_position(0))
# #
# # else:
# #     print("failed to connect")
# #
# #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void get_current_sync_position([MarshalAs(UnmanagedType.LPArray, SizeConst = 5)] double[] pos);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void robot_movj([MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos, int vel, int coord);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void robot_movl([MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos, int vel, int coord);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void robot_movc([MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos1, [MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos2, [MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos3, int vel, int coord);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void robot_movca([MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos1, [MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos2, [MarshalAs(UnmanagedType.LPArray, SizeConst = 6)] double[] pos3, int vel, int coord);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void start_jogging(int axis ,bool dir);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void stop_jogging(int axis);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern int get_robot_running_state();
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void set_jogging_speed(int speed);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern int get_jogging_speed();
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void set_dout(int port, int value);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void set_aout(int port, double value);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void get_dout(double[] dout);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void get_din(double[] din);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void get_aout(double[] aout);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void get_ain(double[] ain);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern int get_current_mode();
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void set_current_mode(int mode);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern int get_current_coord();
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void set_current_coord(int coord);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void upload_job();
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void run_job(string job);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void stop_job();
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void continuous_motion_mode(int on);
# # #
# # #  [DllImport(NBT_CON_DLL_NAME, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
# # #  public static extern void send_continuous_motion_queue([In, Out]cmdPara[] cmd , int size);
# # #
# # #
# # #  [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
# # #  public struct cmdPara
# # #  {
# # #      public enum Type { MOVJ = 1, MOVL, MOVC, MOVCA, MOVJEXT, MOVLEXT, MOVCEXT};
# # #      public double m_velocity;
# # #      public double m_acc;
# # #      public double m_dec;
# # #      public double m_pl;
# # #      public int m_spin;
# # #      [MarshalAs(UnmanagedType.ByValArray, SizeConst = 7)]
# # #      public double[] m_coord;
# # #      [MarshalAs(UnmanagedType.ByValArray, SizeConst = 7)]
# # #      public double[] m_position;
# # #      [MarshalAs(UnmanagedType.ByValArray, SizeConst = 5)]
# # #      public double[] m_syncPosition;
# # #      public Type cmdType;
# # #  }
# # import socket
# #
# # HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# # PORT = 9000        # Port to listen on (non-privileged ports are > 1023)
# #
# # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# #     s.connect((HOST, PORT))
# #     print('Connected')
# #     while True:
# #         data = s.recv(1024)
# #         if not data:
# #             break
# #             # conn.sendall(data)
# #         print(data.decode())
# from scipy.spatial.transform import Rotation as R
# import numpy as np
# import math
#
# # Rot = np.array ([[0.07984568, 0.02159776, -0.99657323],
# #                            [-0.99670678, 0.01592323, -0.07951129],
# #                            [0.0141514, 0.99963993, 0.02279803]])
# # T= np.array([1545.91381457,
# #                            87.11509335,
# #                            -63.98532546])
# #
# # point = np.array([181.09996033, -153.09481812, 1064.52304688])
# #
# # print(np.dot(point,Rot.T) +T)
# # print(np.dot(Rot,point) +T)
#
# # r = R.from_matrix([[-0.99925817, 0.00798237, -0.03767486],
# #                    [0., 0.97828295, 0.2072739],
# #                    [0.03851121, 0.20712014, -0.97755723]])
# # z = np.array([0, -math.sqrt(2) / 2, -math.sqrt(2) / 2])
# z = np.array([0, -math.sqrt(2) / 2, -math.sqrt(2) / 2])
# x = np.array([1, 0, 0])
# y = np.cross(z,x)
#
# T1 = np.array([x, y, z]).T
# print(T1)
# print("\n")
# r = R.from_matrix(T1)
# # r = R.from_rotvec([-np.pi / 4, 0, 0])
# path = ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']
#
# for str in path:
#     print(str.upper(), r.as_euler(str.upper(), degrees=False))
# # euler = r.as_euler('xyz', degrees=False)
# # print(euler)
# # euler = r.as_euler('xyz', degrees=False)
# # print(euler)

from vtk import *

# reader the dicom file
reader = vtkDICOMImageReader()
reader.SetDataByteOrderToLittleEndian()
reader.SetFileName("00efb2fedf64b867a36031a394e5855a.dcm")
reader.Update()

# show the dicom flie
imageViewer = vtkImageViewer2()
imageViewer.SetInputConnection(reader.GetOutputPort())
renderWindowInteractor = vtkRenderWindowInteractor()
imageViewer.SetupInteractor(renderWindowInteractor)
imageViewer.Render()
imageViewer.GetRenderer().ResetCamera()
imageViewer.Render()
renderWindowInteractor.Start()