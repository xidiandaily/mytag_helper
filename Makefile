all:
	python ./mytag_helper.py -h

run:
	python ./mytag_helper.py -t ./data/vim.after.tags -r

check:
	python ./mytag_helper.py -t ./data/vim.tags -c

after:
	python ./mytag_helper.py -t ./data/vim.after.tags -c

upgrade:
	python ./upgrade.py

rel:
	python ./release.py

exe:
	pyinstaller --onefile --icon=icon.ico  ./mytag_helper.py  2>&1 |tee pack.log

