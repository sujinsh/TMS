namespace InexRobot
{
    partial class Form1
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.button1 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.button3 = new System.Windows.Forms.Button();
            this.button4 = new System.Windows.Forms.Button();
            this.button5 = new System.Windows.Forms.Button();
            this.btn_reset = new System.Windows.Forms.Button();
            this.btn_connect_server = new System.Windows.Forms.Button();
            this.btn_close_connect = new System.Windows.Forms.Button();
            this.button6 = new System.Windows.Forms.Button();
            this.txt_x = new System.Windows.Forms.TextBox();
            this.txt_y = new System.Windows.Forms.TextBox();
            this.txt_z = new System.Windows.Forms.TextBox();
            this.txt_rx = new System.Windows.Forms.TextBox();
            this.txt_ry = new System.Windows.Forms.TextBox();
            this.txt_rz = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.button7 = new System.Windows.Forms.Button();
            this.state = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.label10 = new System.Windows.Forms.Label();
            this.label11 = new System.Windows.Forms.Label();
            this.label12 = new System.Windows.Forms.Label();
            this.label13 = new System.Windows.Forms.Label();
            this.label14 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(63, 91);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(100, 40);
            this.button1.TabIndex = 0;
            this.button1.Text = "连接机器人";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.btnConnnect_Click);
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(398, 406);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(100, 40);
            this.button2.TabIndex = 1;
            this.button2.Text = "退出";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.btnClosed);
            // 
            // button3
            // 
            this.button3.Location = new System.Drawing.Point(63, 229);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(100, 40);
            this.button3.TabIndex = 2;
            this.button3.Text = "启动跟踪";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.btnMove_Click);
            // 
            // button4
            // 
            this.button4.Location = new System.Drawing.Point(212, 406);
            this.button4.Name = "button4";
            this.button4.Size = new System.Drawing.Size(100, 40);
            this.button4.TabIndex = 3;
            this.button4.Text = "上电";
            this.button4.UseVisualStyleBackColor = true;
            this.button4.Click += new System.EventHandler(this.button4_Click);
            // 
            // button5
            // 
            this.button5.BackColor = System.Drawing.Color.Red;
            this.button5.CausesValidation = false;
            this.button5.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.button5.Font = new System.Drawing.Font("宋体", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.button5.Location = new System.Drawing.Point(22, 390);
            this.button5.Name = "button5";
            this.button5.Size = new System.Drawing.Size(100, 68);
            this.button5.TabIndex = 4;
            this.button5.Text = "紧急停止";
            this.button5.UseVisualStyleBackColor = false;
            this.button5.Click += new System.EventHandler(this.btn_emergencyStop);
            // 
            // btn_reset
            // 
            this.btn_reset.Location = new System.Drawing.Point(488, 21);
            this.btn_reset.Name = "btn_reset";
            this.btn_reset.Size = new System.Drawing.Size(100, 40);
            this.btn_reset.TabIndex = 0;
            this.btn_reset.Text = "回初始位";
            this.btn_reset.UseVisualStyleBackColor = true;
            this.btn_reset.Click += new System.EventHandler(this.btn_reset_Click);
            // 
            // btn_connect_server
            // 
            this.btn_connect_server.Location = new System.Drawing.Point(63, 25);
            this.btn_connect_server.Name = "btn_connect_server";
            this.btn_connect_server.Size = new System.Drawing.Size(100, 40);
            this.btn_connect_server.TabIndex = 0;
            this.btn_connect_server.Text = "服务器";
            this.btn_connect_server.UseVisualStyleBackColor = true;
            this.btn_connect_server.Click += new System.EventHandler(this.btn_connect_server_Click);
            // 
            // btn_close_connect
            // 
            this.btn_close_connect.Location = new System.Drawing.Point(63, 157);
            this.btn_close_connect.Name = "btn_close_connect";
            this.btn_close_connect.Size = new System.Drawing.Size(100, 40);
            this.btn_close_connect.TabIndex = 0;
            this.btn_close_connect.Text = "传感器";
            this.btn_close_connect.UseVisualStyleBackColor = true;
            this.btn_close_connect.Click += new System.EventHandler(this.btn_close_connect_Click);
            // 
            // button6
            // 
            this.button6.Location = new System.Drawing.Point(488, 327);
            this.button6.Name = "button6";
            this.button6.Size = new System.Drawing.Size(97, 40);
            this.button6.TabIndex = 0;
            this.button6.Text = "go";
            this.button6.UseVisualStyleBackColor = true;
            this.button6.Click += new System.EventHandler(this.button6_Click);
            // 
            // txt_x
            // 
            this.txt_x.Location = new System.Drawing.Point(488, 88);
            this.txt_x.Name = "txt_x";
            this.txt_x.Size = new System.Drawing.Size(97, 21);
            this.txt_x.TabIndex = 5;
            // 
            // txt_y
            // 
            this.txt_y.Location = new System.Drawing.Point(488, 129);
            this.txt_y.Name = "txt_y";
            this.txt_y.Size = new System.Drawing.Size(97, 21);
            this.txt_y.TabIndex = 5;
            // 
            // txt_z
            // 
            this.txt_z.Location = new System.Drawing.Point(488, 172);
            this.txt_z.Name = "txt_z";
            this.txt_z.Size = new System.Drawing.Size(97, 21);
            this.txt_z.TabIndex = 5;
            // 
            // txt_rx
            // 
            this.txt_rx.Location = new System.Drawing.Point(488, 208);
            this.txt_rx.Name = "txt_rx";
            this.txt_rx.Size = new System.Drawing.Size(97, 21);
            this.txt_rx.TabIndex = 5;
            // 
            // txt_ry
            // 
            this.txt_ry.Location = new System.Drawing.Point(488, 248);
            this.txt_ry.Name = "txt_ry";
            this.txt_ry.Size = new System.Drawing.Size(97, 21);
            this.txt_ry.TabIndex = 5;
            // 
            // txt_rz
            // 
            this.txt_rz.Location = new System.Drawing.Point(488, 285);
            this.txt_rz.Name = "txt_rz";
            this.txt_rz.Size = new System.Drawing.Size(97, 21);
            this.txt_rz.TabIndex = 5;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(471, 91);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(11, 12);
            this.label1.TabIndex = 6;
            this.label1.Text = "x";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(471, 132);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(11, 12);
            this.label2.TabIndex = 6;
            this.label2.Text = "y";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(471, 176);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(11, 12);
            this.label3.TabIndex = 6;
            this.label3.Text = "z";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(471, 212);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(17, 12);
            this.label4.TabIndex = 6;
            this.label4.Text = "rx";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(471, 252);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(17, 12);
            this.label5.TabIndex = 6;
            this.label5.Text = "ry";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(471, 289);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(17, 12);
            this.label6.TabIndex = 6;
            this.label6.Text = "rz";
            // 
            // button7
            // 
            this.button7.Location = new System.Drawing.Point(63, 304);
            this.button7.Name = "button7";
            this.button7.Size = new System.Drawing.Size(100, 40);
            this.button7.TabIndex = 2;
            this.button7.Text = "结束跟踪";
            this.button7.UseVisualStyleBackColor = true;
            this.button7.Click += new System.EventHandler(this.button7_Click);
            // 
            // state
            // 
            this.state.AutoSize = true;
            this.state.Font = new System.Drawing.Font("Cambria", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.state.Location = new System.Drawing.Point(215, 51);
            this.state.Name = "state";
            this.state.Size = new System.Drawing.Size(61, 22);
            this.state.TabIndex = 9;
            this.state.Text = "STATE";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Cambria", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(241, 103);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(64, 19);
            this.label7.TabIndex = 10;
            this.label7.Text = "SERVER";
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Font = new System.Drawing.Font("Cambria", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label8.Location = new System.Drawing.Point(339, 103);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(46, 19);
            this.label8.TabIndex = 11;
            this.label8.Text = "None";
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Font = new System.Drawing.Font("Cambria", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label9.Location = new System.Drawing.Point(241, 157);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(62, 19);
            this.label9.TabIndex = 12;
            this.label9.Text = "ROBOT ";
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Font = new System.Drawing.Font("Cambria", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label10.Location = new System.Drawing.Point(339, 157);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(46, 19);
            this.label10.TabIndex = 13;
            this.label10.Text = "None";
            this.label10.Click += new System.EventHandler(this.label10_Click);
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Font = new System.Drawing.Font("Cambria", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label11.Location = new System.Drawing.Point(241, 217);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(71, 19);
            this.label11.TabIndex = 14;
            this.label11.Text = "FOLLOW";
            this.label11.Click += new System.EventHandler(this.label11_Click);
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.Font = new System.Drawing.Font("Cambria", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label12.Location = new System.Drawing.Point(339, 217);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(46, 19);
            this.label12.TabIndex = 15;
            this.label12.Text = "None";
            // 
            // label13
            // 
            this.label13.AutoSize = true;
            this.label13.Font = new System.Drawing.Font("Cambria", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label13.Location = new System.Drawing.Point(241, 275);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(65, 19);
            this.label13.TabIndex = 16;
            this.label13.Text = "SENSOR";
            // 
            // label14
            // 
            this.label14.AutoSize = true;
            this.label14.Font = new System.Drawing.Font("Cambria", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label14.Location = new System.Drawing.Point(339, 275);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(46, 19);
            this.label14.TabIndex = 17;
            this.label14.Text = "None";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(618, 484);
            this.Controls.Add(this.label14);
            this.Controls.Add(this.label13);
            this.Controls.Add(this.label12);
            this.Controls.Add(this.label11);
            this.Controls.Add(this.label10);
            this.Controls.Add(this.label9);
            this.Controls.Add(this.label8);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.state);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.txt_z);
            this.Controls.Add(this.txt_y);
            this.Controls.Add(this.txt_rz);
            this.Controls.Add(this.txt_ry);
            this.Controls.Add(this.txt_rx);
            this.Controls.Add(this.txt_x);
            this.Controls.Add(this.button5);
            this.Controls.Add(this.button4);
            this.Controls.Add(this.button7);
            this.Controls.Add(this.button3);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.button6);
            this.Controls.Add(this.btn_reset);
            this.Controls.Add(this.btn_close_connect);
            this.Controls.Add(this.btn_connect_server);
            this.Controls.Add(this.button1);
            this.Name = "Form1";
            this.Text = "robot control";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form1_FormClosing);
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.Button button3;
        private System.Windows.Forms.Button button4;
        private System.Windows.Forms.Button button5;
        private System.Windows.Forms.Button btn_reset;
        private System.Windows.Forms.Button btn_connect_server;
        private System.Windows.Forms.Button btn_close_connect;
        private System.Windows.Forms.Button button6;
        private System.Windows.Forms.TextBox txt_x;
        private System.Windows.Forms.TextBox txt_y;
        private System.Windows.Forms.TextBox txt_z;
        private System.Windows.Forms.TextBox txt_rx;
        private System.Windows.Forms.TextBox txt_ry;
        private System.Windows.Forms.TextBox txt_rz;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Button button7;
        private System.Windows.Forms.Label state;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.Label label14;
    }
}

