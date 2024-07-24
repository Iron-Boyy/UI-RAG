import subprocess
def get_current_app_package():
    adb_command = "adb shell dumpsys window windows | findstr mCurrentFocus"
    result = subprocess.run(adb_command, capture_output=True, text=True, shell=True)
    print(result)
    current_app = result.stdout.split()[-1].split('/')[0]
    return current_app

current_app = get_current_app_package()
print(current_app)