#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys, os, subprocess, time, hashlib
from Savoir import Savoir

try:
    from Tkinter import *
    import tkFileDialog
    import tkMessageBox
except ImportError:
    from tkinter import *
    from tkinter import filedialog as tkFileDialog
    from tkinter import tkmessagebox as tkMessageBox

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

if py3==1:
    print("Danger ! need python 2.7. Do you launched the jupyter_envs_change_2.7.bat batch ?")

Debug = True
chunk_size = 4*1024*1024 # maxmultichain stream size 64 MBytes = 32*1024*1024 in hexadecimal format
stream = "streamvcf"

def advice():
    tkMessageBox.showwarning( "Not already built !","This function is WIP Work in Progress !" )

def printD(m):
    if Debug:
        print(m)
        sys.stdout.flush()

def checkFileNotExist(f):
    result = True
    if os.path.exists(f):
        result = tkMessageBox.askokcancel(
            "File already exist !",
            "File '"+f+"' already exists on the destination folder. Sure you want to overwrite ?")
    return result

def hash(infile):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(infile, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()       

def generate_private_key(outfile):
    cmd = ['openssl', 'genrsa']
    cmd += ['-out', outfile]
    # print cmd
    # print " ".join(cmd)
    subprocess.Popen(cmd).wait()
    with open(outfile,"rb") as f:
        result = f.readline().rstrip()
    return result

def generate_public_key(infile,outfile):
    cmd = ['openssl', 'rsa']
    cmd += ['-pubout', 
            '-in',infile,
            '-out',outfile]
    # print cmd
    # print " ".join(cmd)
    subprocess.Popen(cmd).wait()
    with open(outfile,"rb") as f:
        result = f.readline().rstrip()
    return result

def encrypt_with_public_key(data, infile, outfile):
    # Ancora da fare
    cmd = ['openssl', 'rsa']
    cmd += ['-pubout', 
            '-in',infile,
            '-out',outfile]
    # print cmd
    # print " ".join(cmd)
    subprocess.Popen(cmd).wait()
    #with open(outfile,"rb") as f:
    #    result = f.readline().rstrip()
    #return result

def password_generator(outfile):
    # openssl rand -base64 48 -out pippo.pwd 
    cmd = ['openssl', 'rand']
    cmd += ['-base64', 
            '48',
            '-out',outfile]            
    #print cmd
    #print " ".join(cmd)
    subprocess.Popen(cmd).wait()
    with open(outfile,"rb") as f:
        result = f.readline().rstrip()
    return result  

def simmetric_encrypt(infile,outfile,password):
    cmd = 'openssl aes-128-cbc -k %s -in "%s" -out "%s"' % ( password, infile, outfile )
    subprocess.Popen(cmd).wait()

def simmetric_decrypt(infile,outfile,password):
    cmd = 'openssl aes-128-cbc -d -k %s -in "%s" -out "%s"' % ( password, infile, outfile )
    subprocess.Popen(cmd).wait()

def simmetric_encrypt_data(infile):
    password = password_generator(infile+".pwd")
    #print(password)
    encinfile = infile+".aes128"
    simmetric_encrypt(infile,encinfile,password)
    if os.path.exists(encinfile):
        return encinfile
    else:
        return None

def getApiData( password ):
    printD('support.getApiData')
    rpcuser = 'multichainrpc'
    rpcpasswd = 'E1istHrjEXZqp396G9uWsX4yuMC2qTHtUg52CPU8E4zz'
    rpcpasswd = password
    rpchost = 'localhost'
    rpcport = '2900'
    chainname = 'GeneChainData'
    #print(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
    api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
    try:
        data = api.getinfo()
    except:
        data = None
        api = None
    #print("API",api)
    #print("data",data)
    return api

def getApiCoin( password ):
    printD('support.getApiData')
    rpcuser = 'multichainrpc'
    rpcpasswd = '8H75HgFBxzv3Hd32RVP6QSp3e4U57Y3JvHk1x8UoqNJw'
    #rpcpasswd = password
    rpchost = 'localhost'
    rpcport = '2896'
    chainname = 'GeneChainCoin'
    print(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
    api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
    try:
        data = api.getinfo()
    except:
        data = None
        api = None
    print("API",api)
    print("data",data)
    return api
    

