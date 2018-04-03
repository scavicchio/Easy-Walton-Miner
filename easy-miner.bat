@echo off
TITLE Easy Walton Miner
setlocal enabledelayedexpansion
set /p "specify=Specify Etherbase address? (y/n, must do on first launch): "
IF "%specify%"=="y" (
	set /p id="Enter Etherbase Address: "
	echo !id! > pubaddr.txt
)
TITLE Walton Hashrate Monitor (Can be closed)
start start_automated.bat
"C:\Program Files\WTC\walton.exe" attach http://127.0.0.1:8545

