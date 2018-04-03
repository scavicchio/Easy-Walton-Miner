TITLE Walton Miner (DO NOT CLOSE)
set /p texte=<pubaddr.txt
echo %texte%
cd "C:/Program Files/WTC"
if exist node1\ (
	echo "exist"
	) else (
	echo "not exist"
	.\walton.exe --datadir node1 init genesis.json
	)
walton --identity "development" --rpc --rpcaddr 127.0.0.1 --rpccorsdomain "*"  --datadir "node1" --port "30303" --rpcapi "admin,personal,db,eth,net,web3,miner" --mine --etherbase %texte% --networkid 999 --rpcport 8545 console