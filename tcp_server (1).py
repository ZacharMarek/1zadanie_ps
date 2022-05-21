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
    do=do.split(":")
    
    if((not do[0].isascii())or(do[0].find(":")!=-1)or(len(do)!=2)):
        return(hlav,obsah)

    hlav=do[0]
    obsah=do[1]
    return(hlav,obsah)


def ls(hl):
    s_cislo=100
    s_txt="OK"
    ob=os.listdir('aaa')

    obsah = str(ob)
    hlavicka = (f,'Lines:{len(obsah)}\n')

    return(s_cislo,s_txt,hlavicka,obsah)


def read(hl):
    s_cislo=100
    s_txt="OK"
    obsah=""
    hlavicka=""
    try:
        with open(f'aaa/{hl["File"]}','r') as fe:
            obsah=fe.readlines()
            dlzka = len(obsah)
            if (int(hl["To"])>(dlzka-1)):
                s_cislo,s_txt=(201,'Bad line number.')
            if(int(hl["From"])>int(hl["To"]) or (int(hl["To"])<1)or(int(hl["From"])<0)):
                s_cislo,s_txt=(200,'Bad Request.')
    except FileNotFoundError:
        s_cislo,s_txt=(202,'No such file.')
    except OSError:
        s_cislo,s_txt=(203,'Read error.')
    except KeyError:
        s_cislo,s_txt=(200,'Bad Request.')

    if (s_cislo != 100):
        return(s_cislo,s_txt,hlavicka,obsah)
    else:
        hlavicka = (f'Lines: {int(hl["To"])-int(hl["From"])}\n')
        obsah =""
        return(s_cislo,s_txt,hlavicka,obsah)


def length(hl):
    s_cislo=100
    s_txt="OK"
    obsah=""
    hlavicka=""
    try:
        with open(f'aaa/{hl["File"]}','r') as fe:
            nacit=fe.readline()
            obsah=len(nacit)

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
#

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
            odp_hlav=""
            method=f.readline().strip()
            if not method:
                break
            d=f.readline()
            while d != "\n":
                prve,druhe=dopln(d)
                pole_hl[prve]=druhe
                d=f.readline()

            if method=="LS":
                s_cislo,s_txt,odp_hlav,odp_obsah = ls(pole_hl)
            elif method=="READ":
                s_cislo,s_txt,odp_hlav,odp_obsah = read(pole_hl)
            elif method=="LENGTH":
                s_cislo,s_txt,odp_hlav,odp_obsah = length(pole_hl)
            else:
                s_cislo,s_txt=(204,'Unknown method.')
                    
                f.write(f'{s_cislo} {s_txt}')
                f.write('\n')
                f.flush()
                sys.exit(0)

            f.write(f'{s_cislo} {s_txt}')
            f.write('\n')
            f.write(str(odp_hlav))
            f.write('\n')
            f.write(str(odp_obsah))
            f.flush()
        print(f'uzavretie spojenie {address}')
        sys.exit(0)
    else:
        connected_socket.close()
