import ctypes
import os.path
import time
import datetime
import sys
import subprocess
import argparse

## Global variables
versionStr = "v1.5.0"

''' Class to contain all configuration options. '''
class Config(object):
    def __init__(self):
        self.__args = parseArgs()
        self.__mode = self.__args['mode']
        self.__walletInstallPath = self.__args['walletpath']
        self.__logging = not self.__args['nolog']
        self.__threadCount = self.__args['threads']
        self.__publicAddressFile = self.__args['publickeypath']
        self.__publicKey = ""
        self.__status = "Status messages will appear here."
        
    def setWalletPath(self, path):
        self.__walletInstallPath = path
    def getWalletPath(self):
        return self.__walletInstallPath
    def setMode(self, mode):
        self.__mode = mode
    def getMode(self):
        return self.__mode
    def setLogging(self, logging):
        self.__logging = logging
    def getLogging(self):
        return self.__logging
    def setThreads(self, threads):
        self.__threadCount = threads
    def getThreads(self):
        return self.__threadCount
    def setPAF(self, file):
        self.__publicAddressFile = file
    def getPAF(self):
        return self.__publicAddressFile
    def setKey(self, key):
        self.__publicKey = key
    def getKey(self):
        return self.__publicKey
    def setStatus(self, status):
        self.__status = status
    def getStatus(self):
        return self.__status

''' Sets the Etherbase address, based on whether the address file already
exists or not. If it does, load it from the file. If not, prompt user for it
and create said file. Returns the key in either case.'''
def setEtherAddr(config):
    if os.path.exists(config.getPAF()):
        adrFile = open(config.getPAF(), "r")
        config.setKey(adrFile.readline().strip())
        adrFile.close()
    else:
        config.setKey(input("Enter Etherbase Address: "))
        adrFile = open(config.getPAF(), "w")
        adrFile.write(config.getKey())
    return config

''' Starts walton.exe in mining mode, with any other flags specified by the
user including walletInstallPath, publicKey, and thread count.'''
def startMining(config):
    os.chdir(config.getWalletPath())
    if not os.path.isdir(config.getWalletPath()+"node1/"):
        os.system("walton.exe --datadir node1 init genesis.json")
    os.system("walton.exe --identity \"development\" --rpc --rpcaddr 127.0.0.1 "+
              "--rpccorsdomain \"*\"  --cache 2048 --datadir \"node1\" --port \"30303\" "+
              "--rpcapi \"admin,personal,db,eth,net,web3,miner\" --mine --etherbase "+config.getKey()+
              " --networkid 999 --rpcport 8545 console")
    return config

''' Attatches to mining process using walton.exe's attach mode, then checks
the current hashrate. Pipes and returns the output as a string.'''
def getHash(config):
    p = subprocess.Popen("\""+config.getWalletPath()+"walton.exe\" attach http://127.0.0.1:8545 --exec miner.getHashrate()", shell=True, stdout=subprocess.PIPE)
    p.wait()
    stdout = p.communicate()[0]
    return stdout.decode("utf-8").strip()

''' Writes the curernt time and hashrate to the specified log file (in csv format.) '''
def logHash(logfile, currHash):
    hashlog = open(logfile, "a")
    ts = time.time()
    sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    hashlog.write(sttime+","+currHash+"\n")
    hashlog.close()

''' Defines and parses possible arguments for the application. Returns a
dictionary of arguments with their associated values. '''
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-wp','--walletpath', required=False, default="C:/Program Files/WTC/")
    parser.add_argument('-pkp','--publickeypath', required=False, default="pubaddr.txt")
    parser.add_argument('-m','--mode', required=False, default="address")
    parser.add_argument('-nl','--nolog', action='store_true', required=False, default=False)
    parser.add_argument('-t', '--threads', required=False, type=int, default=0)
    return vars(parser.parse_args())

''' Sets the current window title to the string specified. '''
def setTitle(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

## CONFIG MENU FUNCTIONS

''' Config menu function to set the wallet path. '''
def menu_walletPath(config):
    path = input("\nEnter new wallet path: ")
    config.setWalletPath(path)
    config.setStatus("Updated wallet path.")
    return config, False

''' Config menu function to enable hashrate logging. '''
def menu_enableLog(config):
    config.setLogging(True)
    config.setStatus("Logging enabled.")
    return config, False

''' Config menu function to disable hashrate logging. '''
def menu_disableLog(config):
    config.setLogging(False)
    config.setStatus("Logging disabled.")
    return config, False

''' Config menu function to set thread count. '''
def menu_threads(config):
    threads = 0
    while threads < 1:
        try:
            threads = int(input("Enter new thread count: "))
        except:
            print("Please enter a valid number.")
    config.setThreads(threads)
    config.setStatus("Updated thread count.")
    return config, False

''' Config menu option to tell the menu loop to break. '''
def menu_exit(config):
    return config, True

def main(argv):
    ## General variables
    delay = 5
    avgHash = 0
    loops = 0

    ## Configuration object
    config = Config()

    ## Beta config menu. Working, but not very useful as config is currently not saved between launches.
    if (config.getMode() == "config"):
        exitMenu = False

        ## Dictionary to store menu options along with associated function for each option
        menu = {     "1. Set Wallet Path": menu_walletPath,
                     "2. Enable Logging": menu_enableLog,
                     "3. Disable Logging": menu_disableLog,
                     "4. Set Thread Count": menu_threads,
                     "5. Exit and Start Mining": menu_exit,
                     }
        while not exitMenu:
            os.system("cls")
            print("\033[92m"+config.getStatus()+"\033[0m\n")
            
            for i,entry in enumerate(menu):
                print(entry)
            choice = input("\nSelect an option: ")
            for i,entry in enumerate(menu):
                if choice == str(i+1):
                    ## Call the relevant menu function
                    config, exitMenu = menu[entry](config)
        config.setMode("address")
    ## Mining mode, usually only when launched from self
    if (config.getMode() == "mine"):
        setTitle("DO NOT CLOSE - Walton Miner/Info")
        ## minimize mining window
        ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )
        config = setEtherAddr(config)
        config = startMining(config)
        return
    ## Address/hashrate mode, the default operating mode on launch
    elif (config.getMode() == "address"):
        setTitle("Easy Walton Miner "+versionStr)
        config = setEtherAddr(config)
        
        ## Launch self in mining mode in a new window. Checks to see if compiled to exe or not.
        if config.getThreads() == 0:
            argStr = " -m mine"
        else:
            argStr = " -m mine -t %d" % config.getThreads()
    
        if os.path.exists("easyWaltonMiner.exe"):
            os.system("start easyWaltonMiner.exe"+argStr)
        elif os.path.exists("easyWaltonMiner.py"):
            os.system("start python easyWaltonMiner.py"+argStr)
        else:
            print("Error launching miner! Did you change the filename of easyWaltonMiner?")
            return
        
        setTitle("Hashrate Monitor (can be closed)")
        os.system('mode con: cols=60 lines=8')
        os.system("cls")
        print("\033[92mINFO: Miner has been started and minimized to the task bar.\n\033[0m")
        print("Mining to address (specified in public address file):\033[93m")
        print(config.getKey())
        print("\n\033[0mThis window will print your hash rate.")
        time.sleep(delay)
        while True:
            currHash = getHash(config)
            if config.getLogging():
                logHash("hashlog.csv", currHash)
            sys.stdout.write("\rAverage hash: \033[91m%d\033[0m | Current hash: \033[91m"%avgHash + currHash+"\033[0m")
            sys.stdout.flush()
            time.sleep(delay)
            loops += 1
            avgHash = ((avgHash*(loops-1))+int(currHash))/loops
                    
    else:
        print("Invalid mode specified. Valid modes are \"mine\" and \"address\"")
    return
            
if __name__ == '__main__':
    sys.exit(main(sys.argv))
