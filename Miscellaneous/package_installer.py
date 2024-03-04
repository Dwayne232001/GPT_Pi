import subprocess

def install_package(package_name):
    try:
        subprocess.check_call(['pip', 'install', package_name])
        print(f"Successfully installed {package_name}.")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package_name}. Please check the package name and try again.")


