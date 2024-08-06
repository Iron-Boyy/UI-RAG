
import subprocess
adb_command = "adb shell dumpsys window windows"
result = subprocess.run(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# print(result)
result = result.stdout.split('    ')
for i in range(len(result)):
    if len(result[i])>len("mActivityRecord") and result[i][:len("mActivityRecord")] == "mActivityRecord":
        print(result[i])
# print(result.stdout.split(' ')[])