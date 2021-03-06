#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# based on fuckshell from @jofpin
# 

import os
import sys
import datetime
import argparse
import textwrap

###
try:
    import urllib2
except:
    import urllib.request as urllib2
import re

if "linux" in sys.platform:
    os.system("clear")
elif "win" in sys.platform:
    os.system("cls")
else:
    pass

#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.socketip, args.socketport)
#socket.socket = socks.socksocket

    #Todo
    # sockes from cmd or from list

VERSION = '1.0'

# Colors
color = {"blue": "\033[34m", "red": "\033[31m", "green": "\033[32m", "white": "\033[97m", "yellow": "\033[33m"}


#banner
def banner():
            print("")
            print("\t\t-------------" + color['blue'] + " Shell Finder " + color['white'] + "------------")
            print("\t\tx      Developed by: zer0.de        x")
            print("\t\tx             OWC RulZ              x")
            print("\t\t  ----------------------------------\n\n")
            print("")
            
# Global scan        

def write_to_file(file,text):
    if not os.path.exists(file):
        try:
            d = open(file,"w")
            d.write(text)
            d.close
        except:
            print("[!] Error file \'%s\' not found or writeable" % file)
            sys.exit(1)
    else:        
         d = open(file,"a")
         d.write(text)
         d.close 

def gscan(filelist,hostfile,logfile):
    #show banner
    banner()
    
    #start logging
    now = datetime.datetime.now()
    write_to_file(logfile, "[##] Shell finder by zer0.de starting at " + now.strftime("%d-%m-%Y %H:%M:%S") + "\n")
     
    # check files available
    try:
        lines = open(filelist).read().splitlines()
    except:
        sys.exit(color['white'] + "Error: " + color['red'] + filelist + " not found\n" + color['white'])
                   
    try:
        hosts = open(hostfile).read().splitlines()
    except:
        sys.exit(color['white'] + "Error: " + color['red'] + hostfile  + " not found\n" + color['white'])
    
    
    rela = []  # relationship
    avai = []  # available
    redi = []  # redirect
    
    
    for url in hosts:
        print('\n' + color['green'] + "[+]" + color['blue'] + "Scanning..." + url + "\n" + color['white'])
        for line in lines:
            try:
                coneccion_url = 'http://' + url + '/' + line
                r = urllib2.Request(coneccion_url)
                r.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6')  # UserAgent
                r.add_unredirected_header('Referer', 'http://www.google.com/')
                req = urllib2.urlopen(r)
                resp = req.read()
                if req.getcode() == 200:
                        print(color['yellow'] + 'Found ' + line + color['white'])  # Found
                        rela.append(coneccion_url)
                else:
                        print(color['green'] + '/' + coneccion_url)  # Redirection
                        redi.append(coneccion_url) 
            except urllib2.HTTPError as e:
                    if e.code == 401:
                            print(color['red'] + '|' + coneccion_url())  # Possible suspicion
                            avai.append(coneccion_url)
                    elif e.code == 404:
                            # print(color['red'] + '-' + color['white']) #Not Found
                            pass
                    elif e.code == 503:
                            print(color['red'] + 'x' + coneccion_url)  # Not Found
                    else:
                            print(color['blue'] + '/' + coneccion_url)  # Redirection
                            redi.append(coneccion_url)                                   
    print('\n')
    print(color['blue'] + "[!]" + " " + color['green'] + "Result:" + color['white'])

       
    if len(rela) == 0:
        print(color['green'] + "\t Nothing Found" + color['white'])  # founds
        print(color['green'] + '================================================================' + color['white'])
        write_to_file(logfile, "[!] Nothing Found for " + url + "\n")
    else:
         print(color['blue'] + "[>]" + " " + color['yellow'] + "Possible malicious files\n" + color['white'])
         for relas in rela:
             print(color['red'] + "\t Shell: " + relas + color['white'])  # founds
             write_to_file(logfile, "[!!] Possible malicious files " + relas + "\n")
         print(color['red'] + '================================================================' + color['white'])
        
    if not avai:
        pass
    else:
        print(color['blue'] + "[+]" + " " + color['yellow'] + "Possible detected WebShell\n" + color['white'])
        for avais in avai:
            print(color['red'] + "\t WebShell: " + color['white'] + avais)
            write_to_file(logfile, "[!!] WebShell " + avais + "\n")
        print(color['yellow'] + '==================================================================' + color['white'])
        
    if not redi:
        pass
    else:
        print("Statements of other income")
        for redis in redi:
            print(color['red'] + "\t" + color['white'] + redis)
            write_to_file(logfile, "[!!] Statements of other income " + redi +"\n")
        print(color['blue'] + '===================================================================' + color['white'])
        
            
    #at last
    now = datetime.datetime.now()
    write_to_file(logfile, "[##] Shell finder by zer0.de completet at " + now.strftime("%d-%m-%Y %H:%M:%S") + "\n\n")
    
    
    
                
if __name__ == "__main__":
        try:
            parser = argparse.ArgumentParser(prog='OWC_Shell_finder', formatter_class=argparse.RawDescriptionHelpFormatter, 
                                                            description=textwrap.dedent('''
                                                                    ------------" Shell finder "-----------
                                                                    x      Developed by: zer0.de          x
                                                                    x             OWC RulZ                x
                                                                      -----------------------------------'''),
                                                                    epilog="")
            
            parser = argparse.ArgumentParser()
            parser.add_argument("-i", "--hosts", required=True,  help="Target IPs")
            parser.add_argument("-d", "--dict", required=True, help="list with shell names")
            parser.add_argument("-o", "--logfile" ,help="Logfile")
            
            args = parser.parse_args()
            
            if not args.logfile:
                logfile = "log.txt"
            else:
                logfile = args.logfile
            
            gscan(args.dict, args.hosts, logfile)
            
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(color['red'] + "Error: " + color['white'] + "%s" % e)
