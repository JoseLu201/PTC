#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 16:05:30 2023

@author: aulas
"""
from tkinter import messagebox
import vrep


class VrepManager:
    def __init__(self):
        self.clientID = -1
        self.robothandle = None
        self.camhandle = None
        self.left_motor_handle = None
        self.right_motor_handle = None
        self.datosLaserComp  = None
        self.camhandle = None
        self.personhandle  = None
        self.resolution = None
        self.image = None

    def conectar_vrep(self):
        vrep.simxFinish(-1)
        self.clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
        ok = False
        if self.clientID != -1:
            messagebox.showinfo("Conexión", "Conexión establecida con VREP")
            # Obtener las referencias necesarias
            _, self.robothandle = vrep.simxGetObjectHandle(self.clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
            ok = True
        else:
            messagebox.showerror("Error de conexión", "No se puede conectar a VREP. Inicia la simulación antes de llamar a este script.")
        return ok
    def desconectar_vrep(self):
        if self.clientID != -1:
            # Cerrar la conexión con VREP
            vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_oneshot_wait)
            vrep.simxFinish(self.clientID)
            messagebox.showinfo("Desconexión", "Desconexión de VREP realizada")

    def begin(self):
        #Guardar la referencia de los motores
        _, self.left_motor_handle=vrep.simxGetObjectHandle(self.clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
        _, self.right_motor_handle=vrep.simxGetObjectHandle(self.clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
         
        #acceder a los datos del laser
        _, self.datosLaserComp = vrep.simxGetStringSignal(self.clientID,'LaserData',vrep.simx_opmode_streaming)

        # obtenermos la referencia a la persona sentada Bill para moverla
        _, self.personhandle = vrep.simxGetObjectHandle(self.clientID, 'Bill#0', vrep.simx_opmode_oneshot_wait)
         
        #Iniciar la camara y esperar un segundo para llenar el buffer
        _, self.camhandle = vrep.simxGetObjectHandle(self.clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
       # _, self.resolution, self.image = vrep.simxGetVisionSensorImage(self.clientID, self.camhandle, 0, vrep.simx_opmode_streaming)
        
    def readLaser(self):
        _, self.datosLaserComp = vrep.simxGetStringSignal(self.clientID,'LaserData',vrep.simx_opmode_streaming)
        return self.datosLaserComp
        