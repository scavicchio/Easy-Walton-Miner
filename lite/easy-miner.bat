@echo off
TITLE Easy Walton Miner Lite v1.3.0

echo The lite version is written in shell script to minimize impact on performance. If you have a good computer, 
echo consider upgrading to the full version for more features.
echo.

REM ## WTC wallet installation path ##
set walletInstallPath="C:\Program Files\WTC\walton.exe"

REM ## Other variables ##
set publicAddressFile=pubaddr.txt
set delay=10

setlocal enabledelayedexpansion

if exist %publicAddressFile% (
echo Waiting for miner to launch.
) else (
set /p id="Enter Etherbase Address: "
echo !id! > %publicAddressFile%
)

REM ## Print hashrate every X seconds indefinitely ##
TITLE Walton Hashrate Monitor (Can be closed)
start start_automated.bat
timeout 10 /NOBREAK > NUL

REM ## The following will loop indefinitely
:loop
cls
mode con: cols=60 lines=7
echo Mining to address {specified in %publicAddressFile%}
type %publicAddressFile%
echo.
echo This window will print your hash rate every %delay% seconds.
echo.

REM ## Print hash rate to csv for logging purposes as well as output to console ##
<nul set /p =%DATE% %TIME% >> hashlog.csv
<nul set /p =, >> hashlog.csv
%walletInstallPath% attach http://127.0.0.1:8545 --exec miner.getHashrate() > lastHash.txt

REM ## Use buffer in order to be able to log & echo to console at the same time
type lastHash.txt >> hashlog.csv
type lastHash.txt

timeout %delay% /NOBREAK > NUL

goto loop