# -*- coding: cp1252 -*-
import cv2
import numpy as np
import time
import math
import cinematica



global pto_Destino
pto_Destino = cinematica.Point()
bRetira = False
drawing = False # para calibrar as coordenadas
_Status = "Calibrar - Selecione o primeiro ponto"
bManual = False # Se Manual, onde clicar move braço a uma altura de 15cm 'm'
global iPulso
bPulso = False # Girar Pulso
iPulso = 0
global bGarra # Para Abrir e fechar a garra
bGarra = False
global iGarra
iGarra = 45
bDesce_Sobe = False
iDesce_Sobe = 15
global fator_x
global fator_y
fator_x = 1
fator_y = 1
global ix,iy
ix,iy = -1,-1
global jx,jy
jx,jy = -1,-1
global i_x,i_y
i_x,i_y = -1,-1
global j_x,j_y
j_x,j_y = -1,-1
global frame
frame  =  np . zeros (( 704, 480 , 3 ),  np . uint8 )
global bCalibrar
bCalibrar = True
global bCoordenadas
global coord_x,coord_y
coord_x,coord_y = 0,0
bCoordenadas = False
global bMalha
bMalha = True
global iTop_x
iTop_x=0
global iTop_y
iTop_y=0
global iBottom_x
iBottom_x=0
global iBottom_y
iBottom_y=0
global bInterresse
bInterresse=False
global _x_destino
global _y_destino
inicio = time.time()
fim = time.time()


captura = cv2.VideoCapture()
captura.open("rtsp://192.168.0.2/stream1")
FONTE = cv2.FONT_HERSHEY_TRIPLEX
vermelho = (0, 0, 255)

# mouse callback function

def draw_(event,x,y,flags,param):
    global inicio,rastrear,_Status, bInterresse,iTop_x,iTop_y,iBottom_x,iBottom_y,iGarra,iPulso,iDesce_Sobe,coord_x,coord_y,ix,iy,jx,jy,i_x,i_y,j_x,j_y,pto_Destino,bCoordenadas,bCalibrar,frame

    #if event == cv2.EVENT_LBUTTONDBLCLK:
        
    if event == cv2.EVENT_MOUSEMOVE:
        coord_x,coord_y = calcula_coordenadas(x,y)
        if drawing == True:
            cv2.rectangle(frame,(ix,iy),(x,y),(0,255,0),2)        
            
    if event == cv2.EVENT_LBUTTONDOWN:
        if bCalibrar == True:
            if ix < 0:
                ix,iy = x,y                
                _Status = "Calibrar - Selecione o segundo ponto"
            else:
                _Status = "Calibrado! i->Para selecionar area de interesse m-> Manual:"
                jx,jy=x,y
                cv2.rectangle(frame,(ix,iy),(jx,jy),(0,255,0),2)
                bCoordenadas = True
                bCalibrar = False
        coord_x,coord_y = calcula_coordenadas(x,y)
        # Desenha área de interresse
        if bInterresse == True:
            if iTop_x == 0:
                iTop_x = x
                iTop_y = y
                print(iTop_x," ",iTop_y)
                _Status = "Segundo ponto:"
            else:
                bInterresse=False
                iBottom_x = x
                iBottom_y = y
                print(iBottom_x," ",iBottom_y)
                _Status = "Rastrear? Digite r para começar!"
                inicio = time.time()                
                
        if bManual == True:            
            pto_Destino.x = coord_x
            pto_Destino.y = coord_y
            pto_Destino.z = iDesce_Sobe
            
            cinematica.fCinematicaInversa_(pto_Destino,iPulso,iGarra)
            _x,_y = calcula_coordenadas_real(0,0)
            _xx,_yy = calcula_coordenadas_real(round((math.sqrt((coord_x **2)+(coord_y**2))),2),0)
            distancia = abs(_x-_xx)
            print("Distância: ",(math.sqrt((coord_x **2)+(coord_y**2))))
            print("Distancia: ",distancia)
            cv2.circle(frame, (_x, _y), distancia, preto)
            
        #if drawing == True:
            #cv2.rectangle(frame,(ix,iy),(x,y),(0,255,0),2)

def calcula_coordenadas(x,y):    
    return round((i_x+(x-ix)*fator_x),2),round((i_y+(iy-y)*fator_y),2)
def calcula_coordenadas_real(_x,_y):
    return int(((_x-i_x)/fator_x) +ix),int((((_y-i_y)/fator_y)-iy)*-1)

cv2.namedWindow('Video')
cv2.setMouseCallback('Video',draw_)
rastrear = 0

while(1):
    ret, frame = captura.read()
    azul = (255, 0, 0)
    amarelo = (0, 255, 255)    
    if rastrear == 1:
        imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 100, 255, cv2.THRESH_BINARY)
    
        contours, hierarchy=cv2.findContours(thresh,cv2.RETR_LIST ,cv2.CHAIN_APPROX_NONE)
        #contours, hierarchy=cv2.findContours(thresh,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_NONE)
        #contours, hierarchy=cv2.findContours(thresh,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
        #print("Numeros de contornos: ", len(contours))        
        _x=0
        _y=0
        for c in contours:
        
            x,y,w,h = cv2.boundingRect(c)
            
            if (x > iTop_x and y > iTop_y and x+w < iBottom_x and y+h < iBottom_y):
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
                
                if area < w*h:
                    area = w*h
                    _x = round((x + w/2),2)
                    _y = round((y + h/2),2)
                    _x_destino,_y_destino = calcula_coordenadas(_x,_y)
                    print('X: ',_x,' Y: ',_y)
                    print('X: ',_x_destino,' Y: ',_y_destino)
                    print('Maior Area: ',area)
                    cv2.rectangle(frame,(int(_x),int(_y)),(int(_x),int(_y)),(0,255,255),3)
                print(_y_destino) 
                fim = time.time()
                print('Enviado: ',_x_destino,',',_y_destino)
            else:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),3)
        if (fim-inicio > 5):
            pto_Destino.x = _x_destino
            pto_Destino.y = _y_destino
            pto_Destino.z = 15
            #input("Pressione <enter> para continuar")
            bRetira = True
            rastrear = 0
            fim=0
            inicio=0
            _Status = 'Encontrado...'

        cv2.rectangle(frame, (iTop_x, iTop_y), (iBottom_x, iBottom_y), vermelho, 3)
        cv2.imshow('thresh',thresh)        
        cv2.imshow('imgray',imgray)
    if bRetira == True:
        print(_x_destino)
        print(_y_destino)
        iGarra = 15
        iPulso = 90
        iTempo = 2.5
        cinematica.fCinematicaInversa_(pto_Destino,iPulso,iGarra)
        time.sleep(iTempo)
        pto_Destino.z = 0 #Desce para pegar objeto
        cinematica.fCinematicaInversa_(pto_Destino,iPulso,iGarra)
        time.sleep(iTempo/4)
        iGarra = 85        #Fecha Garra
        cinematica.fCinematicaInversa_(pto_Destino,iPulso,iGarra)
        time.sleep(iTempo/4)
        pto_Destino.z = 15 #Sobe com objeto
        cinematica.fCinematicaInversa_(pto_Destino,iPulso,iGarra)
        time.sleep(iTempo/4)
        pto_Destino.x = 0 # Transporta objeto para um lugar determinado
        pto_Destino.y = 20
        cinematica.fCinematicaInversa_(pto_Destino,iPulso,iGarra)
        time.sleep(iTempo)
        pto_Destino.z = 2 #Desce para soltar objeto
        cinematica.fCinematicaInversa_(pto_Destino,iPulso,iGarra)
        time.sleep(iTempo/4)
        iGarra = 15        #Abre Garra
        cinematica.fCinematicaInversa_(pto_Destino,iPulso,iGarra)
        time.sleep(iTempo/4)        
        pto_Destino.z = 20        
        cinematica.fCinematicaInversa_(pto_Destino,iPulso,iGarra)
        time.sleep(iTempo/4)
        
        bRetira = False
        rastrear=0
    if iBottom_x > 0:        
        cv2.rectangle(frame,(iTop_x,iTop_y),(iBottom_x,iBottom_y),(azul),5)        
        
    if bPulso == True:
        bPulso = False
        cinematica.writeNumber(04)
        time.sleep(0.1)
        if iPulso == 90:
            cinematica.writeNumber(00)
            iPulso = 0
        else:            
            cinematica.writeNumber(90)
            iPulso=90
        time.sleep(0.1)
        cinematica.writeNumber(00)
        time.sleep(0.5)
    if bGarra == True:
        bGarra = False        
        cinematica.writeNumber(05)
        if iGarra == 45:
            iGarra=85 # Fechada
        else:
            iGarra=45 # aberta
        print(iGarra)
        cinematica.writeNumber(iGarra)
        time.sleep(0.1)
        cinematica.writeNumber(00)
        time.sleep(0.5)
    if bDesce_Sobe == True:
        bDesce_Sobe=False
        if iDesce_Sobe == 3:
            iDesce_Sobe = 15
        else:
            iDesce_Sobe = 3
            
        pto_Destino.z = iDesce_Sobe
        cinematica.fCinematicaInversa_(pto_Destino,90,60)
    if bMalha == True:
        # Desenha Malha
        for i in range(0,10):
            _x,_y = calcula_coordenadas_real(-50,i*5)
            _xx,_yy = calcula_coordenadas_real(0,i*5)
            cv2.line(frame, (_x, _y), (_xx,_yy), amarelo)
            _x,_y = calcula_coordenadas_real(i*5-40,35)
            _xx,_yy = calcula_coordenadas_real(i*5-40,-5)
            cv2.line(frame, (_x, _y), (_xx,_yy), amarelo)

        preto = (0, 0, 0)
        _x,_y = calcula_coordenadas_real(0,0)
        _xx,_yy = calcula_coordenadas_real(33,0)
        distancia = _xx-_x
        cv2.circle(frame, (_x, _y), distancia, preto)
        
        
                #cv2.putText(imagem, forma,(x, y), FONTE, 0.5,(0,255,0),1,2)
    cv2.putText(frame, "Coordenadas X: " + str(coord_x) + " Y: " + str(coord_y), (10, 460 ), FONTE, 0.5,(0,255,255),1,1)
    cv2.putText(frame, "Status: " + _Status, (10,10), FONTE, 0.5,(255,255,255),1,1)
    cv2.imshow("Video", frame)
        
    if bCoordenadas == True:
        print("Coordenadas")
        bCoordenadas = False
        i_x = input("Digite a coordenadas Para Esquerda X:")
        i_y = input("Digite a coordenadas Para Esquerda Y:")
        j_x = input("Digite a coordenadas Para Direita X:")
        j_y = input("Digite a coordenadas Para Direita Y:")
        jix_=abs(j_x-i_x)
        jiy_=abs(j_y-i_y)
        jix=abs(jx-ix)      
        jiy=abs(jy-iy)
        print("jix_: ",jix_)
        print("jiy_: ",jiy_)
        print("jix: ",jix)
        print("jiy: ",jiy)
        print("ix: ",ix)
        print("iy: ",iy)
        print("jx: ",jx)
        print("jy: ",jy)
        fator_x = (float(jix_)/float(jix))
        fator_y = (float(jiy_)/float(jiy))
        print("%.5f" % fator_x)
              
        print(fator_y)        
        

    k = cv2.waitKey(1) & 0xFF    
    if k == ord('m'):
        bManual = not bManual
        if bManual == True:
            _Status = 'Manual'
            rastrear = 0            
        else:
            _Status = 'Automatico'
            
    elif k == ord('p'):
        bPulso = True
    elif k == ord('g'):
        bGarra = True
    elif k == ord('d'):
        bDesce_Sobe = True
    elif k == ord('i'):
        bInterresse = True
        _Status = 'Selecione a area de interresse, primeiro ponto!'
        iTop_x = 0
        iTop_y = 0
        rastrear = 0
        bManual = False        
    elif k == ord('1'):
        bMalha = not bMalha
    elif k == ord('r'):                
        if rastrear == 1:            
            rastrear = 0
            _Status = 'r -> rastrear, i -> Area de Interresse m -> Manual!'
        else:
            area = 0
            rastrear = 1
            inicio=time.time()
            bManual = False        
            _Status = 'Ratreando!'            
    elif k == 27:
        break
captura.release()
cv2.destroyAllWindows()
