@echo off
TITLE Easy Walton Miner

REM ## WTC wallet installation path ##
set walletInstallPath="C:\Program Files\WTC\walton.exe"

REM ## Other variables ##
set publicAddressFile=pubaddr.txt
set delay=30

setlocal enabledelayedexpansion

if exist %publicAddressFile% (
echo Mining to address {specified in %publicAddressFile%}
type %publicAddressFile%
) else (
set /p id="Enter Etherbase Address: "
echo !id! > %publicAddressFile%
)

REM ## Print hashrate every 30 seconds indefinitely ##
TITLE Walton Hashrate Monitor (Can be closed)
start start_automated.bat
timeout 5 /NOBREAK > NUL

:loop
cls
echo Mining to address {specified in %publicAddressFile%}
type %publicAddressFile%
echo.
echo This window will print your hash rate every %delay% seconds.
echo.
%walletInstallPath% attach http://127.0.0.1:8545 --exec miner.getHashrate()
timeout %delay% /NOBREAK > NUL
goto loop
