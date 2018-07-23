
import smbus
import time
import math
import cv2


class Point:
    #""" Point class represents and manipulates x,y coords. """

    def __init__(self):
     #   """ Create a new point at the origin """
        self.x = 0
        self.y = 0
        self.z = 0
        
pt_garra = Point()
pt_garra_Origem = Point()
pt_garra_Destino = Point()

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x20
 

SERVO = [00, 01, 02, 03, 04, 05]
juntas_int = [0,0,0,0,0,0]
juntas_dec = [0,0,0,0,0,0]

def writeNumber(value):
    bus.write_byte(address, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    return number
    
   

def fCinematicaInversa_(pto,giro_pulso,abre_garra):    
    link_0=9
    link_1=10
    link_2=6
    garra=18.8
    q0=0
    q1=0
    q2=0
    q3=0
    print("x Ponta da Garra ",pto.x)
    print("y Ponta da Garra ",pto.y)
    print("z Ponta da Garra ",pto.z)
    
    
    x_j01 = round(math.sqrt(pto.x **2 + pto.y **2),2)
    y_j01 = pto.z

    print ("x_junta03->",x_j01)
    print ("y_Junta03->",y_j01)

    
    # Calculo do angulo inicial da Garra
    # posicao da Garra
    
    a=round(math.sqrt((x_j01-0)**2 + (y_j01-link_0)**2),2)
    print ("a->",a)
    b= garra
    print ("b->",b)
    c= link_1 + link_2
    print ("c->",c)

    x_ponta_garra = a
    y_ponta_garra = y_j01


    # Lei do cosseno

    ang_beta_garra_j01= round(math.atan2((link_0-y_j01),x_j01),2)
    print("Angulo Beta Garra - Junta 01 ",ang_beta_garra_j01 )
    ang_psi_garra_j01 = round(math.acos(-((c**2-a**2-b**2)/(2*a*b))) - 0.0524,2)
    print("Angulo PSI Garra - Junta 01 ",ang_psi_garra_j01)
    ang_garra = (ang_beta_garra_j01 + ang_psi_garra_j01)
    print ("Angulo da Garra",ang_garra)
    # Calculo das coordanadas da junta 03
    
    x_j03 = round(garra*math.cos(ang_garra+math.pi) + x_j01,2)
    y_j03 = round(garra*math.sin(ang_garra) + y_j01,2)

    print("x Junta 03 ",x_j03)
    print("y Junta 03 ",y_j03)
    

    # Calculo para achar angulos da junta 01 e junta 02
    
    print("---------------------------------------------")
    _x=x_j03
    _y=y_j03 - link_0  

    beta=math.atan2(_y,_x)  
    
    print(_x)
    print(_y)
    print(link_1)
    print(link_2)
    _dividendo = (_x**2)+(_y**2)+(link_1**2)-(link_2**2)
    _divisor = ((2*((_x **2) +(_y**2)) ** 0.5) * link_1 )
    print("Dividendo ",_dividendo)
    print("Divisor ",_divisor)
    
    psi=math.acos(_dividendo/_divisor)
    q1= beta + psi
    print("Beta ",beta)
    print("PSI ", psi)
    #print("Q1 ", math.degrees(q1))
    print("---------------------------------------------")
    
    print("_X", _x)
    print("_Y", _y)
    
    x_Junta_2 = math.cos(math.radians(q1)) * link_1
    y_Junta_2 = (math.sin(math.radians(q1)) * link_1) + link_0
    q2 = math.acos((_x**2 + _y**2 - link_1**2 - link_2**2) / (2*link_1*link_2))
    print("q2----->",q2)
    # Calculo para Junta 0
    print("Ponto X ", pto.x)
    print("Ponto y ", pto.y)
    if (pto.x < 0):
        q0 = math.atan2(pto.x,pto.y)
        print("X negativo ****************")
    else:     
        q0 = math.atan2(pto.x,pto.y)
        print("X Positivo ****************")
    print(pto.x)
    print(pto.y)
    
    print(q0)
    q0 = math.degrees(abs(q0))
    #q0 = round((q0*0.888)+20,2)
    q0 = round((q0*0.888)+20,2)
    print ("Q0 ->", q0)
    q3 = (q1 - q2) + ang_garra
    print("Q1: real-> ",q1)
    print("Q2: real-> ",q2)
    print("Q3: real-> ",q3)
    q1=math.degrees(q1) +15
    q2=math.degrees(q2)
    q3=math.degrees(q3)
    #q1=50 -(90-q1)
    q2=(65+q2*0.722)
    q3=(180-q3)*0.666 + 60
    q1=round(q1, 2)
    q2=round(q2, 2)
    q3=round(q3, 2)
    q4=giro_pulso
    q5=abre_garra
    print("Garra ---------------------->")
    print(abre_garra)
    #q5=90
    print("Q1 ->", q1)
    print("Q2 ->", q2)
    print("Q3 ->", q3)
    print("---------------------------------------------")

    
    juntas_int[0] = int(q0)
    juntas_int[1] = int(q1)
    juntas_int[2] = int(q2)
    juntas_int[3] = int(q3)
    juntas_int[4] = int(q4)
    juntas_int[5] = int(q5)

    juntas_dec[0] = int((q0 - juntas_int[0]) * 100)
    juntas_dec[1] = int((q1 - juntas_int[1]) * 100)
    juntas_dec[2] = int((q2 - juntas_int[2]) * 100)
    juntas_dec[3] = int((q3 - juntas_int[3]) * 100)
    juntas_dec[4] = int((q4 - juntas_int[4]) * 100)
    juntas_dec[5] = int((q5 - juntas_int[5]) * 100)
    
    print("*********************************************")

    move_braco(SERVO,juntas_int,juntas_dec)
 
    
############################################################
# Polinomio de Lagrange
# Interpolacao de conjuntos de pontos na forma de Lagrange
############################################################
# p(x) = f(x0).L0(x) + f(x1).L1(x) + f(x2).L2(x)
#
# L0(x) = (x-x1).(x-x2)
#         -------------
#        (x0-x1).(x0-x2)
#
# L1(x) = (x-x0).(x-x2)
#         -------------
#        (x1-x0).(x0-x2)
#
# L2(x) = (x-x0).(x-x1)
#         -------------
#        (x2-x0).(x2-x1)
############################################################

def fTrajetoria(Pt_Origem = Point(), Pt_Destino = Point()):

    x0=1
    f0=Pt_Origem.z
    x2=round(math.sqrt((Pt_Destino.x - Pt_Origem.x) ** 2 + (Pt_Destino.z - Pt_Origem.z) ** 2),2)
    print("X2: ",x2)
    f2=Pt_Destino.z
    print(Pt_Origem.x, " - ", Pt_Origem.z) 
    print(Pt_Destino.x, " - ", Pt_Destino.z) 
    print (round(x2, 2))                 
    fator_x = (Pt_Destino.x - Pt_Origem.x)/x2
    fator_y = (Pt_Destino.z - Pt_Origem.z)/x2
    print(fator_x)
    print(fator_y)           
    
    x1=((x2-x0)/2)+x0
    f1=26
    print("x1: ",x1)
    print("f1: ",f1)
    
    l0_Divisor= (x0-x1)*(x0-x2)
    l1_Divisor= (x1-x0)*(x1-x2)
    l2_Divisor= (x2-x0)*(x2-x1)

    l0_Dividendo_a = f0
    l1_Dividendo_a = f1
    l2_Dividendo_a = f2
    
    l0_Dividendo_b = (-x2-x1)*f0
    l1_Dividendo_b = (-x2-x0)*f1
    l2_Dividendo_b = (-x1-x0)*f2
    
    l0_Dividendo_c = (x1*x2)*f0
    l1_Dividendo_c = (x0*x2)*f1
    l2_Dividendo_c = (x0*x1)*f2

    l_A= (l0_Dividendo_a/l0_Divisor) + (l1_Dividendo_a/l1_Divisor) + (l2_Dividendo_a/l2_Divisor)
    l_B= (l0_Dividendo_b/l0_Divisor) + (l1_Dividendo_b/l1_Divisor) + (l2_Dividendo_b/l2_Divisor)
    l_C= (l0_Dividendo_c/l0_Divisor) + (l1_Dividendo_c/l1_Divisor) + (l2_Dividendo_c/l2_Divisor)
    print("---------------------------------------------")
    print("          Polinomio de Lagrange")
    print("---------------------------------------------")
    print(l_A)
    print(l_B)
    print(l_C)

    print("")
    pto_intermediario = (x2)/10
    while (x0 <= x2):
        
        pt_garra.x = round(pt_garra.x + fator_x*2,2)
        pt_garra.y = round(pt_garra.y + fator_y*2,2)
        z_tr= (l_A * (x0 ** 2)) + (l_B * x0) + l_C
        print("X0: ",x0)
        print("Tr Z: ", z_tr)
        pt_garra.z = round(z_tr,2)                 
        print(pt_garra.x," - ", pt_garra.y, " - ", pt_garra.z)                 
        fCinematicaInversa_(pt_garra,90,60)
        time.sleep(0.01)
        x0=x0+2
        #x0=x2
        

    
def move_braco(servos,_ang,_decimal):
    i=0
    for x in (servos): #reversed
        print("Servo: ", x ," Angulo",_ang[i], " Decimais ",_decimal[i])
        writeNumber(x)
        time.sleep(0.01)
        writeNumber(_ang[i])
        time.sleep(0.01)
        writeNumber(_decimal[i])
        time.sleep(0.01)       
        i=i+1
    print("Enviados para Arduino......................")

#pt_garra_Destino.x = -20
#pt_garra_Destino.y = 5
#pt_garra_Destino.z = 10
#fCinematicaInversa_(pt_garra_Destino,90,45)

time.sleep(1)

print("Carregado Cinematica......")
time.sleep(0.8)



