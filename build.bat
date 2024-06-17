:: pyinstaller --onefile --add-data "programs/git_installer.exe;." --add-data "programs/java_installer.exe;." --add-data "programs/jdk_17_installer.exe;." --add-data "programs/mmc.zip;." installer.py --icon=icon.ico
pyinstaller installer.spec
