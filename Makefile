install:
	pip install -r requirements.txt

setup:
	geth --exec "loadScript('/run/media/shankar/Data/comDocuments/uni/spring-24/561/561-ctf/src/setup_account.js')" attach http://localhost:8545
	solc-select use 0.8.13

forge-setup:
	forge build
	forge test

run:
	export FLASK_APP=main
	export FLASK_ENV=development
	flask --app src/main run