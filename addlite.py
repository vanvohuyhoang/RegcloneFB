import subprocess

def install_apk(device_id, apk_path):
    try:
        subprocess.run(["adb", "-s", device_id, "install", apk_path], check=True)
        print("APK đã được cài đặt thành công.")
    except subprocess.CalledProcessError as e:
        print("Lỗi khi cài đặt APK:", e)

device_id = input('Nhập id thiết bị muốn cài đặt : ')
apk_path = 'D:/RegCloneFbDl/DataReg/appsp/Fb_lite.apk'

install_apk(device_id, apk_path)