@echo off
TITLE Easy Walton Miner

REM ## WTC wallet installation path ##
set walletInstallPath="C:\Program Files\WTC\walton.exe"

REM ## Other variables ##
set publicAddressFile=pubaddr.txt
set delay=5

setlocal enabledelayedexpansion

if exist %publicAddressFile% (
echo Mining to address {specified in %publicAddressFile%}
type %publicAddressFile%
) else (
set /p id="Enter Etherbase Address: "
echo !id! > %publicAddressFile%
)

TITLE Walton Hashrate Monitor (Can be closed)
start start_automated.bat
timeout %delay%
%walletInstallPath% attach http://127.0.0.1:8545
