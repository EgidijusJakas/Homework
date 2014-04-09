import serial
import time
import binascii
import struct
import matplotlib.pyplot as plt
import matplotlib.widgets
from collections import deque
import numpy as np
import sys
from Tkinter import *
import random
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA


#Funkcija nustatanti Error koda
def errorCode(receivedBits):
	print "\n"
	if receivedBits[-5]=='00':		
		return "Program executed properly"
	if receivedBits[-5]=='01':		
		return "Error code - protocol timeout"
	if receivedBits[-5]=='02':
		return "Error code - format error"
	if receivedBits[-5]=='03':
		return "Error code - CRC32 error"
	if receivedBits[-5]=='04':
		return "Error code - bad address"
	if receivedBits[-5]=='05':
		return "Error code - not allowed in current mode"

#Nurodoma gautu baitu paskirtis			
def bytesPurpose(receivedBits):	
	return ("\nBytes to start communication: " + receivedBits[0] + " " + receivedBits[1] + 
	"\nCommand byte: " + receivedBits[2] + 		
	"\nData size field bytes: " + receivedBits[3] + " " + receivedBits[4] + 		
	"\nLast written record: " + receivedBits[-10]  + " " +  receivedBits[-9] + " " + receivedBits[-8]+
	"\nStatus register byte: " + receivedBits[-7] +
	"\nmode register byte: " + receivedBits[-6] +
	"\nError code byte: " + receivedBits[-5] +
	"\nCRC32 bytes: " + receivedBits[-4] + " " + receivedBits[-3] + " " + receivedBits[-2] + " " + receivedBits[-1])

#CRC32 algoritmas
def crc2hex(crc):
    res=''
    for i in range(4):
        t=crc & 0xFF
        crc >>= 8
        res='%02X%s' % (t, res)
    return res
#if receivedBits[i]!='00':			
#print "x0" + str(hex(s+address)[2:])+ ": " + receivedBits[i]
#Nurodomi gauti duomenys
def dataFieldBytes(receivedBits, address):
    a = ''
    for i in range (5, len(receivedBits)-11):
        a += str(receivedBits[i])
    return a
		
#Komandos irasymas ir gautu duomenu masyvo sukurimas
def	modeSetReset(bytes, receivedBits):
    a=binascii.unhexlify(bytes)
    ser.write(a)
    i = 0
    we_have_data = False
    while we_have_data == False:
        i += 0.001
        time.sleep(i)
        ch = ser.read(size=500)
        if len(ch) == 18 or i >= 0.02:
            print i
            we_have_data = True
    atsakymas = ch.encode('hex')
    ats=list(atsakymas)
    receivedBits=[]
    a=0
    s=''
    x=0
    for x in ats:
        s+=x
        if a%2==0:
            s=x	
        if len(s)==2:
            receivedBits.append(s)
            s=''
        a+=1
    return receivedBits

#CRC32 	
def crc32(test):
	a = binascii.unhexlify(test)
	crc=binascii.crc32(a)
	finalCrc32=crc2hex(crc)
	
	return finalCrc32
#Komanda skirta pakeisti baitus LSB formatu
def changeToLSBFormat(unreversed):	
	b=unreversed[::-1]
	s=0
	c=''
	d=''
	crc32LSB=''
	for i in b:	
		if s%2==0:
			c+=i
		else:
			d+=i
		if d!='':
			crc32LSB+=d+c
			c=''
			d=''
		s+=1
	return crc32LSB
#Komanda skirta adreso vietai nurodyti i kuria kreipiames
def startAddress(address):
	if address <=65535 and address >=0:
		a=str(hex(address)[2:])
		count=0
		finalAddress=a
		for i in range(1, 5):
			if len(finalAddress)<=3:
				finalAddress='0'+finalAddress
		newAddress = changeToLSBFormat(finalAddress)
	if address <=16777215 and address >=65536:
		a=str(hex(address)[2:])
		count=0
		finalAddress=a
		for i in range(1, 8):
			if len(finalAddress)<=6:
				finalAddress='0'+finalAddress
		newAddress = changeToLSBFormat(finalAddress)	
		
				
	return newAddress
#informacijos nuskaitymo komanda(01)	
def readCommand(address, bytesToRead):
	extraNumber='00'
	if address <=16777215 and address >=65536:
		extraNumber=''
	if bytesToRead <=255 and bytesToRead >=16:		
		a=str(hex(bytesToRead)[2:])
		code='A55A010400' + startAddress(address) + extraNumber + a
		
	elif bytesToRead<=15 and bytesToRead >=0:
		a=str(hex(bytesToRead)[2:])
		code='A55A010400' +  startAddress(address) + extraNumber + '0' + a
		
	elif bytesToRead >=256:		
		code='A55A010400' + startAddress(address) + extraNumber + '00'		
		
	#print "nuskaitymo kodas: " + code
	return code

#0x2 - Write data to additional NV memory
def writeCommand(address, byteNumber):
	if byteNumber <=255 and byteNumber >= 0:
		byteNumberHex=str(hex(byteNumber)[2:])
		if len(byteNumberHex)==1:
			byteNumberHex='0'+byteNumberHex
		code='A55A02' +  startAddress(byteNumber+3) + startAddress(address) + byteNumberHex
		print "\ndata to", startAddress(address), "was written\n\n"
		print "irasymo kodas: " + code
		return code

def float_hex4(f):
	return ''.join(('%2.2x'%ord(c)) for c in struct.pack('f', f))

def change_x_scale_value(x):
	masyvas = []
	writeCode=writeCommand(32,4)
	finalWriteCode=writeCode + changeToLSBFormat(x)
	writeCRC=crc32(finalWriteCode)
	writeCodeLast=finalWriteCode + changeToLSBFormat(writeCRC)
	modeList1 = modeSetReset(writeCodeLast, masyvas)
	print "irasem"
	

def float_hex4(f):
	return changeToLSBFormat(''.join(('%2.2x'%ord(c)) for c in struct.pack('f', f)))

def write_data(start_address, bytes_number, data_to_write):
	masyvas = []
	writeCode=writeCommand(start_address, bytes_number)
	data_to_write_final = str(hex(data_to_write))
	finalWriteCode=writeCode + changeToLSBFormat(data_to_write_final[2:]) 
	print "finalWriteCode: " + finalWriteCode
	writeCRC=crc32(finalWriteCode)
	writeCodeLast=finalWriteCode + changeToLSBFormat(writeCRC)
	modeList1 = modeSetReset(writeCodeLast, masyvas)

def read_data(start_address, bytes_number):
	a=readCommand(start_address,bytes_number)
	b = crc32(a)
	bytes= a + changeToLSBFormat(b)
	masyvas= []
	modeList = modeSetReset(bytes, masyvas)
	a = dataFieldBytes(modeList,start_address)
	result = changeToLSBFormat(a)
	#result_last = int(result, 16)
	#print result_last
	print result
	return result
	


#Serial porto initalizacija 
ser = serial.Serial(
    port='COM3',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)




def textF():
	mtext1 = x_scale_value.get()
	change_x_scale_value(float_hex4(float(mtext1)))
	mtext = absolute_position_scale_value.get()
	mlabel2 = Label(mGui, text=mtext).pack()
	return

def quit():
    mGui.quit()
	
	
####################################
#Create button to change parameters#
####################################	


mGui = Tk()
absolute_position_scale_value = StringVar()
x_scale_value = StringVar()
mGui.geometry('300x200+200+200')
mGui.title('Parametru keitimas')

x_scale_label = Label(mGui, text = 'Keisti x_scale verte (distance to surface)').pack()
x_scale_field = Entry(mGui, textvariable = x_scale_value).pack()
set_x_scale = Button(mGui, text = 'Pasirinkti', command = textF, fg = 'red', bg = 'blue').pack()


absolute_position_scale_label = Label(mGui, text = 'Keisti absolute_position_scale verte (absolute position)').pack()
absolute_position_scale_field = Entry(mGui, textvariable = absolute_position_scale_value).pack()
set_absolute_position_scale = Button(mGui, text = 'Pasirinkti', command = textF, fg = 'red', bg = 'blue').pack()

mbutton = Button(mGui, text = 'Brezti grafika', command = quit, fg = 'red', bg = 'blue').pack()


def distance_to_surface():
    count = 0
    crc_error = 0
    while True:
        a=readCommand(16776970,3)
        b = crc32(a)
        baitai1= a + changeToLSBFormat(b)
        masyvas = []
        modeList = modeSetReset(baitai1, masyvas)
        dataFieldBytes(modeList,16776970)
        response = modeList[:14]
        responseString = ''.join([str(x) for x in response])
        crc32response = crc32(responseString)
        theoricalCrc32responseLSB = changeToLSBFormat(crc32response).lower()
        practicalCrc32responseLSB = ''.join([str(x) for x in modeList[14:]])
        if theoricalCrc32responseLSB != practicalCrc32responseLSB:
            crc_error += 1
            print "distance ... CRC error" + str(crc_error)
        if len(modeList) == 18 and theoricalCrc32responseLSB == practicalCrc32responseLSB:
            val = int(changeToLSBFormat(str(modeList[5]+modeList[6])), 16)
            error_distance_to_surface = False
            if (val >= 2000):
                print modeList
            yield val
        else:
            print val
            error_distance_to_surface = True
            count +=1
            print "distance to surface" + str(count)
            yield val
        time.sleep(0.00005)


		
def absoulute_position():
    crc_error = 0
    count = 0
    while True:
        a=readCommand(16776968,3)
        b = crc32(a)
        baitai1= a + changeToLSBFormat(b)
        masyvas = []
        modeList = modeSetReset(baitai1, masyvas)
        dataFieldBytes(modeList,16776968)
        response = modeList[:14]
        responseString = ''.join([str(x) for x in response])
        crc32response = crc32(responseString)
        theoricalCrc32responseLSB = changeToLSBFormat(crc32response).lower()
        practicalCrc32responseLSB = ''.join([str(x) for x in modeList[14:]])
        if theoricalCrc32responseLSB != practicalCrc32responseLSB:
            crc_error += 1
            print "absolute ... CRC error" + str(crc_error)      
        if len(modeList) == 18 and theoricalCrc32responseLSB == practicalCrc32responseLSB:
            val = int(changeToLSBFormat(str(modeList[5]+modeList[6])), 16)   
            error_absoulute_position = False
            if (val <= 2200):
                print modeList			
            yield val
        else: 
            print val
            error_absoulute_position = True
            count +=1
            print "absolute_position" + str(count)
            yield val
        time.sleep(0.00005)
		
class Index:
    ind = 0
    def next(self, event):
        mGui.mainloop()

		
callback = Index()	

distance_to_surface_curve = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(right=0.75)

absolute_position_curve = distance_to_surface_curve.twinx()


offset = 60

distance_to_surface_store = deque([0]*200)
abolute_position_store = deque([0]*200)



distance_to_surface_curve.set_xlim(0, 200)
distance_to_surface_curve.set_ylim(0, 5000)

distance_to_surface_curve.set_xlabel("Distance")
distance_to_surface_curve.set_ylabel("Distance to surface")
absolute_position_curve.set_ylabel("Abosulute position")


get_distance_to_surface = distance_to_surface()
get_absolute_position = absoulute_position()


distance_to_surface_plot, = distance_to_surface_curve.plot(distance_to_surface_store, 'g', label="Distance to surface")
absolute_position_plot, = absolute_position_curve.plot(abolute_position_store, label="Abosulute position")


absolute_position_curve.set_ylim(0, 5000)

distance_to_surface_curve.legend()

#distance_to_surface_curve.axis["left"].label.set_color(distance_to_surface_plot.get_color())
absolute_position_curve.axis["right"].label.set_color(absolute_position_plot.get_color())
	



########################################
# Activate button for parameter change #
########################################

#bnext = matplotlib.widgets.Button(ax, '')
#bnext.on_clicked(callback.next)
plt.ion()
plt.show()
buttons_on = True
for i in range(0,1000):
    distance_to_surface_store.appendleft(next(get_distance_to_surface))
    datatoplot1 = distance_to_surface_store.pop()
    distance_to_surface_plot.set_ydata(distance_to_surface_store)
    abolute_position_store.appendleft(next(get_absolute_position))
    datatoplot2 = abolute_position_store.pop()
    absolute_position_plot.set_ydata(abolute_position_store)
    print "Distance to surface: " + str(distance_to_surface_store[0])
    print "Absolute position: " + str(abolute_position_store[0])
    plt.draw()
    i += 1
    time.sleep(0.00005) 
    plt.pause(0.00005)
    if buttons_on == True:
		buttons_on = False
	

ser.close()


