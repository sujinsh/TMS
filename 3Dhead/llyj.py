import sys
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import threading
import time

from lyj import Ui_MainWindow

# global ren


class MyStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        print("init")
        self.last_picked_actor = None
        self.AddObserver("LeftButtonPressEvent", self.leftButtonDown)
        self.AddObserver("RightButtonPressEvent", self.rightButtonDown)
        self.AddObserver("RightButtonReleaseEvent", self.rightButtonUp)

    def leftButtonDown(self, *arg):
        inter1 = self.GetInteractor()
        click_pos = inter1.GetEventPosition()
        picker = vtk.vtkCellPicker()
        # picker.Pick(click_pos[0], click_pos[1], 0, ren)
        picker.Pick(click_pos[0], click_pos[1], 0, ren)
        pos = picker.GetPickPosition()
        print('pos:', pos)
        if self.last_picked_actor is not None:
            ren.RemoveActor(self.last_picked_actor)
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetCenter(pos[0], pos[1], pos[2])
        sphereSource.SetRadius(0.003)
        sphereMapper = vtk.vtkPolyDataMapper()
        sphereMapper.SetInputConnection(sphereSource.GetOutputPort())
        sphereActor = vtk.vtkActor()
        sphereActor.SetMapper(sphereMapper)
        sphereActor.GetProperty().SetColor(255.0, 0.0, 0.0)

        self.last_picked_actor = sphereActor

        if self.last_picked_actor is not None:
            ren.AddActor(sphereActor)
        # 主要是为了刷新标记点
        vtkWidget.GetRenderWindow().Render()

    def rightButtonDown(self, *arg):
        self.OnLeftButtonDown()

    def rightButtonUp(self, *args):
        self.OnLeftButtonUp()


class mythread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.view = MainWindow()

    def run(self):
        while 1:
            pass


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.testpb1_func)
        self.ui.pushButton_2.clicked.connect(self.testpb2_func)

        global ren, vtkWidget
        # self.vtkWidget = QVTKRenderWindowInteractor(self.ui.label)
        vtkWidget = QVTKRenderWindowInteractor(self.ui.label)

        # filename = 'C:/Users/10401/Desktop/00.3DS'
        # filename = "D:/lyj/pyrender/examples/models/fuze.obj"
        filename = 'D:/lyj/flame-fitting/output/hello_flame.obj'
        # filename = "./output/fit_lmk3d_result.obj"
        reader = vtk.vtkOBJReader()
        reader.SetFileName(filename)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        # self.ren = vtk.vtkRenderer()
        # self.ren.AddActor(actor)
        # self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        # global ren
        ren = vtk.vtkRenderer()
        # print('ren1:', ren)
        ren.AddActor(actor)
        vtkWidget.GetRenderWindow().AddRenderer(ren)
        # self.vtkWidget.GetRenderWindow().AddRenderer(ren)


        self.iren = vtkWidget.GetRenderWindow().GetInteractor()
        # self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        style = MyStyle()
        self.iren.SetInteractorStyle(style)
        self.iren.Start()

        # 显示原点
        '''
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetCenter(0, 0, 0)
        sphereSource.SetRadius(0.01)
        sphereMapper = vtk.vtkPolyDataMapper()
        sphereMapper.SetInputConnection(sphereSource.GetOutputPort())
        sphereActor = vtk.vtkActor()
        sphereActor.SetMapper(sphereMapper)
        sphereActor.GetProperty().SetColor(0.0, 255.0, 0.0)     # green
        ren.AddActor(sphereActor)
        vtkWidget.GetRenderWindow().Render()
        '''
        '''
        reader = vtk.vtkOBJReader()
        reader.SetFileName(filename)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        # Assign actor to the renderer
        # Create a rendering window and renderer
        self.ren = vtk.vtkRenderer()
        self.ren.AddActor(actor)
        # Enable user interface interactor
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
        # renWin.Render()
        self.iren.Start()
        '''

    def testpb1_func(self):
        print(ren.GetActors().GetNumberOfItems())
        ren.RemoveAllViewProps()
        print(ren.GetActors().GetNumberOfItems())
        # self.vtkWidget.GetRenderWindow().AddRenderer(ren)
        vtkWidget.GetRenderWindow().Render()

    def testpb2_func(self):
        filename = "./output/hello_flame.obj"
        reader = vtk.vtkOBJReader()
        reader.SetFileName(filename)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        ren.AddActor(actor)
        vtkWidget.GetRenderWindow().Render()
        # a = np.load('C:/Users/10401/Desktop/ttt/data/lmk.npy')
        # print(a)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logi = MainWindow()
    logi.show()
    sys.exit(app.exec_())
