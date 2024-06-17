import os
import subprocess
import zipfile
import shutil
import sys
import time

#okay so this is the installer for the modpack.
#the rough idea is this script will be an exe in the end and if executed it will check if all required programs are installed.
#if not it will install them. (I think: fabric, java, MultiMc, and minecraft)
#if everything is installed it will check if the modpack is installed and on the latest version.
#if not it will install the modpack or update it.
#this should be doable with the modpack being uploaded to a github repo and then pulling any changes from there. (I hope)
#and if everything is installed and up to date it will just launch the modpack and the launcher as normal should start

#settings
git_install = os.path.join(sys._MEIPASS, "programs/git_installer.exe") #bundeled git installer
java_install = os.path.join(sys._MEIPASS, "programs/java_installer.exe") #bundeled java installer
jdk_install = os.path.join(sys._MEIPASS, "programs/jdk_17_installer.exe") #bundeled jdk installer
mmc_zip = os.path.join(sys._MEIPASS, "programs/mmc.zip") #bundeled MultiMC zip

mmc_dir = os.path.join(os.getenv("LOCALAPPDATA"), "Programs\MultiMC") #install at C:\Users\[user]\AppData\Local\Programs\MultiMC

modpack_name = "Prominence_2_Fighter" #this is the name of the Instance in MultiMC and the Repo name on github
modpack_repo = "https://github.com/Fightingpa1n/Prominence_2_Fighter.git" #this is the github repo where the modpack is stored

#values
mmc_exe = os.path.join(mmc_dir, "MultiMC.exe")
modpack_dir = os.path.join(mmc_dir, f"instances\{modpack_name}")

def check_and_programs():
    print("Checking for required programs...")

    #check for java
    java = False
    while not java:
        try:
            subprocess.run(["java", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            java = True

        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Java not found. Installing...")
            if os.path.exists(java_install):
                subprocess.run([java_install, "/silent"], check=True)
                print("waitng for java to finish installing trying again in 10 seconds")
                time.sleep(10)
            else:
                print(f"Java installer not found: {java_install}")
                raise FileNotFoundError(f"Java installer not found: {java_install}")
    print("Java is installed.")

    #check for jdk
    jdk = False
    while not jdk:
        try:
            subprocess.run(["java", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            jdk = True

        except (subprocess.CalledProcessError, FileNotFoundError):
            print("JDK not found. Installing...")
            if os.path.exists(jdk_install):
                subprocess.run([jdk_install, "/silent"], check=True)
                print("waitng for jdk to finish installing trying again in 10 seconds")
                time.sleep(10)
            else:
                print(f"JDK installer not found: {jdk_install}")
                raise FileNotFoundError(f"JDK installer not found: {jdk_install}")
    print("JDK is installed.")

    #check for git
    git = False
    while not git:
        try:
            subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            git = True

        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Git not found. Installing...")
            if os.path.exists(git_install):
                subprocess.run([git_install, "/silent"], check=True)
                print("waitng for git to finish installing trying again in 10 seconds")
                time.sleep(10)
            else:
                print(f"Git installer not found: {git_install}")
                raise FileNotFoundError(f"Git installer not found: {git_install}")
    print("Git is installed.")


def check_and_install_mmc():
    #check if MultiMC is installed
    if not os.path.exists(mmc_exe):
        print("MultiMC not found. Installing...")
        if os.path.exists(mmc_zip):
            with zipfile.ZipFile(mmc_zip, 'r') as zip_ref:
                zip_ref.extractall(mmc_dir)
            print("MultiMC installation completed.")
            return True
        else:
            print(f"MultiMC zip file not found: {mmc_zip}")
            raise FileNotFoundError(f"MultiMC zip file not found: {mmc_zip}")
    else:
        print("MultiMC was Found")
        return False


def check_instance_dir():
    #check if the modpack instance is installed if not we need to install it (like first time setup)
    print("Checking for modpack instance...")

    if not os.path.exists(modpack_dir):
        print("Modpack not found. Installing...")
        subprocess.run(["git", "clone", modpack_repo, modpack_dir], check=True)
        print("Modpack installed.")
    else:
        print("Modpack was Found")


def update_modpack():
    #check if the modpack is up to date
    print("CUpdating modpack...")

    os.chdir(modpack_dir)
    subprocess.run(["git", "fetch", "origin", "main"], check=True)
    result = subprocess.run(["git", "status", "-uno"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if b"Your branch is up to date" in result.stdout:
        print("Modpack is up to date.")
    else:
        print("Never Version Found. Updating...")
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        print("Modpack updated.")
    


if __name__ == "__main__":
    try:
        print("Hello,\n this this file will start the Game or install it if it is not installed yet. (this is my first installer, sorry if something doesn't work properly)\n\nPlease be patient as this may take a while... (especially the first time)")

        check_and_programs()
        print("All required programs are installed")

        first_time = check_and_install_mmc()
        check_instance_dir()
        update_modpack()

        print("all done, Starting Pack...\n\n\n\n\n")
        
        if first_time:
            print("Ah before I forget since this is a fresh install of MultiMC it will prompt you to some stuff, just click through it and you should be good to go.")
            print("oh and if it asks you to choose a java version, choose the one with jdk in the path, and the version should be around 17")
            print("If you have any issues with MultiMC try, starting it on it's own and see if it wants an update or something.")
        
        subprocess.Popen([mmc_exe, "--launch", f"{modpack_name}"])

    except Exception as e:
        print(f"An error occured: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

#TODO: (maybe) I think mmc uses config files for settings. I could maybe make it so mmc doesn't prompt the user and instead I can make a custom dialog for the user to set the settings. (I think this is possible but it might go into the realm of overkill)