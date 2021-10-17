using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Data;
using System.Threading;

namespace InexRobot
{
    class Log
    {
        private string path;
        public bool flag;
        StreamWriter sw;
        public Log(string filepath)
        {
            flag = false;
            if (!filepath.IsNormalized())
            {
                filepath = "./log.txt";
            }
            path = filepath;
            try
            {
                sw = new StreamWriter(path);

            }
            catch(Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(ex.ToString());
            }
        }
        public void generateLog(string info)
        {
            while(true)
            {
                if(flag)
                {
                    if (info.Length != 0)
                    {
                        string str = $"{DateTime.Now.ToLongDateString()}   info ";
                        sw.WriteLine(str);
                    }
                }
            }
        }

        public void closeLog()
        {
            try
            {
                sw.Flush();
                sw.Close();
            }catch(Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(ex.ToString());
            }
        }

    }
}
