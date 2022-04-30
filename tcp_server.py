#!/usr/bin/env python3
import socket
import os
import sys
import signal
import hashlib


def dopln(do):
    hlav=""
    obsah=""
    do=do.strip()

    if not do.isascii():
        return(hlav,obsah)
    if do.isspace():
        return(hlav,obsah)
    if do.find(":") != -1:
        do=do.split(":")
        if len(do)!=2:
            return(hlav,obsah)
        if do[0].find("/")==-1:
            hlav=do[0]
            obsah=do[1]
        else:
            return(hlav,obsah)
    else:
        return(hlav,obsah)
    return(hlav,obsah)

        

def metoda(hl):
    s_cislo=100
    s_txt="OK"
    for i in hl:
        if hl[i]=="":
            s_cislo,s_txt=(200,'Bad request.')
        if i=="":
            s_cislo,s_txt=(200,'Bad request.')
        if s_cislo==200:
            return s_cislo,s_txt
    return s_cislo,s_txt            

def ls(hl):
    s_cislo=100
    s_txt="OK"
    obsah = os.listdir('data')
    hlavicka = (f,'Lines:{len(obsah)}\n')

    return(s_cislo,s_txt,hlavicka,obsah)


def read(hl):
    s_cislo=100
    s_txt="OK"
    obsah=""
    hlavicka=""
    try:
        with open(f'data/{hl["File"]}','r') as fe:
            obsah=fe.readlines()
            if (dict["To"]>(len(obsah)-1)):
                s_cislo,s_txt=(201,'Bad line number.')
                     
    except FileNotFoundError:
        s_cislo,s_txt=(202,'No such file.')
    except OSError:
        s_cislo,s_txt=(203,'Read error.')
    except KeyError:
        s_cislo,s_txt=(200,'Bad Request.')

    if (s_cislo != 100):
        return(s_cislo,s_txt,hlavicka,obsah)
    else:
        hlavicka = (f'Lines: {hl["To"]-hl["From"]}\n')
        obsah =""
        return(s_cislo,s_txt,hlavicka,obsah)

def length(hl):
    s_cislo=100
    s_txt="OK"
    obsah=""
    hlavicka=""
    try:
        with open(f'data/{hl["File"]}','r') as fe:
            nacit=fe.readline()
            
    except KeyError:
        s_cislo,s_txt=(200,'Bad Request.')
    except FileNotFoundError:
        s_cislo,s_txt=(202,'No such file.')
    except OSError:
        s_cislo,s_txt=(203,'Read error.')

    if (s_cislo != 100):
        return(s_cislo,s_txt,hlavicka,obsah)
    else:
        hlavicka = (f'Lines:1\n')
        obsah =len(nacit)
        return(s_cislo,s_txt,hlavicka,obsah)


        

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('',9999))
s.listen(5)
signal.signal(signal.SIGCHLD,signal.SIG_IGN)
#print('spojenie ')

while True:
    connected_socket,address=s.accept()
    print(f'spojenie z {address}')
    pid_chld=os.fork()
    if pid_chld==0:
        s.close()
        f=connected_socket.makefile(mode='rw',encoding = 'utf-8')

        while True:
            pole_hl={}
            odp_hlav=""
            odp_obsah=""
            #print('1while')
            method=f.readline().strip()
            if not method:
                break
            #print('metoda nacit')
            d=f.readline()
            while d != "\n":
                hlav,obsah=dopln(d)
                pole_hl[hlav]=obsah
                d=f.readline()
                #print('2while')
            s_cislo,s_txt=metoda(pole_hl)
            if s_cislo==100:
                #print('metoda sedi')
                if method=="LS":
                    s_cislo,s_txt,odp_hlav,odp_obsah = ls(pole_hl)
                elif method=="READ":
                    s_cislo,s_txt,odp_hlav,odp_obsah = read(pole_hl)
                elif method=="LENGTH":
                    s_cislo,s_txt,odp_hlav,odp_obsah = length(pole_hl)
                else:
                    s_cislo,s_txt=(204,'Unknown method.')
            
                f.write(f'{s_cislo}{s_txt}')         
                f.write('\n')
                f.write(odp_hlav)
                f.write('\n')
                f.write(odp_obsah)
                f.flush()
            print(f'uzavretie spojenie {address}')
            sys.exit(0)
    else:
        connected_socket.close()
