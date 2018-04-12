@echo off
TITLE Easy Walton Miner GPU Lite V1.0

echo The lite version is written in shell script to minimize impact on performance. If you have a good computer, 
echo consider upgrading to the full version coming soon for more features.
echo.

REM ## WTC wallet installation path ##
set walletInstallPath="C:\Program Files\WTC\walton.exe"

REM ## Other variables ##
set publicAddressFile=pubaddr.txt
set delay=60

setlocal enabledelayedexpansion

if exist %publicAddressFile% (
echo Waiting for miner to launch.
) else (
set /p id="Enter Etherbase Address: "
echo !id! > %publicAddressFile%
)

REM ## Print hashrate every X seconds indefinitely ##
TITLE Walton Hashrate Monitor (Can be closed)
start start_automated_GPU.bat
timeout 10 /NOBREAK > NUL

REM ## The following will loop indefinitely
:loop
cls
mode con: cols=60 lines=7
echo Mining to address {specified in %publicAddressFile%}
type %publicAddressFile%
echo.
echo This window will print your GPU hash rate every %delay% seconds.
echo.


REM ## Use buffer in order to be able to log & echo to console at the same time
type 0202001.txt >> hashlogGPU.csv
type 0202001.txt

timeout %delay% /NOBREAK > NUL

goto loop
