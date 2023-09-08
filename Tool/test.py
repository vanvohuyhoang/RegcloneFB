
import threading, subprocess, time, random, os, unidecode, requests, sys, cv2, numpy as np, requests, re
os.system('cls')

def process_device(data_run):
    devices = data_run['id_divice']
    file_screanshott = data_run['part_png']
    file_object_check = data_run['part_obj']
    key_mail = data_run['key_mail']

    # Hàm ghi lên cmd
    def cmd(input):
        command = input
        subprocess.run(command, shell=True)

    # Hàm gửi lệnh ADB
    def adb_command(command):
        subprocess.run(["adb", "-s", devices, "shell"] + command)

    # Hàm điều hướng điện thoại
    def system_cmd(keycode):
        adb_command(["input", "keyevent", keycode])

    # Click vào một tọa độ trên màn hình điện thoại
    def postclick(x, y):
        adb_command(["input", "tap", str(x), str(y)])

    # Ghi nội dung văn bản lên màn hình điện thoại 
    def type_text(text):
        adb_command(["input", "text", text.replace(" ", "%s")]) # # Thay thế khoảng trắng bằng %s

    # Gửi lệnh swipe / nhấn giữ trên màn hình điện thoại
    def swipe(start_x, start_y, end_x, end_y, duration):
        adb_command(["input", "swipe", str(start_x), str(start_y), str(end_x), str(end_y), str(duration)])

    # Ham kiem tra va tim toa do
    def check_object(img_name):
        for x in range(10):
            # Chup anh man hinh
            with open(os.devnull, 'w') as devnull:
                subprocess.run(["adb", "-s", devices, "shell", "screencap", "-p", "/sdcard/screenshot.png"], stdout=devnull, stderr=devnull)
                subprocess.run(["adb", "-s", devices, "pull", "/sdcard/screenshot.png", file_object_check], stdout=devnull, stderr=devnull)
            # # Đường dẫn đến ảnh / doi tuong
            screenshot_path = file_screanshott
            template_path = f"{file_object_check}{img_name}"
            # Đọc hình ảnh đối tượng / anh goc
            object_image = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            original_image = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)
            # Phát hiện đối tượng trong hình ảnh gốc
            result = cv2.matchTemplate(original_image, object_image, cv2.TM_CCOEFF_NORMED)
            # Thiết lập ngưỡng phát hiện
            threshold = 0.8
            # Lấy vị trí và độ chính xác của đối tượng
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            # Kiểm tra xem đối tượng có tồn tại trong hình ảnh gốc hay không
            if max_val >= threshold:
                # # Đọc ảnh chụp màn hình và mẫu
                screenshot = cv2.imread(screenshot_path)
                template = cv2.imread(template_path)
                # Chuyển đổi ảnh sang đen trắng để tăng cường sự khác biệt giữa mẫu và ảnh chụp màn hình
                screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                # # Thực hiện Template matching
                result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
                # Tìm tọa độ của đối tượng trong ảnh chụp màn hình
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + template_gray.shape[1], top_left[1] + template_gray.shape[0])
                # Vẽ đường viền xung quanh đối tượng trên ảnh chụp màn hình (chỉ để minh họa)
                cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
                # Lấy tọa độ trung tâm của đối tượng
                object_center = (top_left[0] + template_gray.shape[1] // 2, top_left[1] + template_gray.shape[0] // 2)
                x = top_left[0] + template_gray.shape[0]
                y = top_left[1] + template_gray.shape[0]
                return x, y
                break
            else:
                print('Dang cho hinh anh xuat hien', end = '')
                sys.stdout.flush()
                time.sleep(2)
                print('\r                                       \r', end = '')
        return 0

    def click(file_name, time_sleep, note):
        object_center = check_object(file_name)
        if object_center != 0:
            x, y = object_center
            print(note, end = '')
            sys.stdout.flush()
            postclick(x, y)
            time.sleep(time_sleep)
            print('\r                                       \r', end = '')
        else:
            clear_data_lite()

    def swipes(a, b, c, d, e, time_sleep, note):
        print(note, end = '')
        sys.stdout.flush()
        swipe(a, b, c, d, e)
        time.sleep(time_sleep)
        print('\r                                       \r', end = '')

    def putdata(text, time_sleep, note):
        print(note, end = '')
        sys.stdout.flush()
        type_text(text)
        time.sleep(time_sleep)
        print('\r                                       \r', end = '')

    # Lay email ao
    headers = {

    }

    def get_mail(x):
        if x == 1:
            get = requests.get(url = f'https://10minutemail.net/address.api.php?new=1&sessionid={key_mail}', headers = headers).json()
            mail = get['mail_get_mail']
            return mail
        else:
            for x in range(15):
                get = requests.get(url = f'https://10minutemail.net/address.api.php?sessionid={key_mail}', headers = headers).json()
                fist_mail = get['mail_list'][0]
                from_mail = fist_mail['from']
                if 'Facebook' in from_mail:
                    data_mail = fist_mail['subject']
                    code = re.findall(r'\d+', data_mail)[0]
                    return code
                    break
                else:
                    time.sleep(5)
                    if x == 10:
                        return 'no_email'

    def save_info(email, password):
        with open('D:\RegCloneFbDl\data_reg.txt', 'a', encoding='utf-8') as filee:
            filee.write(f'{email}|{password}\n')

    # Xoa du lieu lite
    def clear_data_lite():
        system_cmd('KEYCODE_HOME')
        time.sleep(1)
        click('syssetting.png', 1, 'Nhấn Vào Cài Đặt Hệ Thống')
        click('settingapp.png', 1, 'Nhấn Vào Cài Đặt App')
        click('litesetting.png', 1, 'Nhấn Vào Cài Đặt Lite')
        click('appstop.png', 1, 'Nhấn Buộc Dừng Lite')
        click('okstop.png', 1, 'Xác Nhận Buộc Dừng Lite')
        click('bonho.png', 1, 'nhan bo nho')
        click('cache.png', 1, 'nhan bo nho')
        click('data.png', 1, 'nhan bo nho')
        click('taikhoanvacaidat.png', 1, 'nhan bo nho')
        click('okthem.png', 1, 'nhan bo nho')
        click('xoadataapp.png', 1, 'nhan bo nho')
        system_cmd('KEYCODE_HOME')
        time.sleep(5)
        creat_acc()

    def very_code(email, password):
        for i in range(5):
            code = get_mail(2)
            if code != 'no_email':
                putdata("12345", 1, 'Nhập code xác minh')
                click('ok.png', 2, 'Bấm OK')
                click('boxcode.png', 1, 'Nhấn o nhap mail')
                putdata(code, 2, 'Nhập code xác minh')
                click('ok.png', 3, 'Bấm OK')
                break
            else:
                click('thaymail.png', 1, 'Bấm OK')
                click('mailmoi.png', 1, 'Nhấn o nhap mail')
                email = get_mail(1)
                putdata(email, 2, 'Nhập email mới')
                click('next.png', 2, 'Nhấn tiep')
                click('boxcode.png', 1, 'Nhấn o nhap mail')
                code = get_mail(2)
                if code != 'no_email':
                    putdata('12345', 2, 'Nhập code xác minh')
                    click('ok.png', 1, 'Bấm OK')
                    click('boxcode.png', 1, 'Nhấn o nhap mail')
                    putdata(code, 2, 'Nhập code xác minh')
                    click('ok.png', 3, 'Bấm OK')
                    break

    def creat_acc():
        # gioi tinh
        sex = random.randint(1, 2)
        # ho
        with open('D:/RegCloneFbDl/DataReg/infoacc/lastname.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            last_name = unidecode.unidecode(random.choice(lines)).strip()
        name = None
        # ten nu
        if sex == 1:
            with open('D:/RegCloneFbDl/DataReg/infoacc/firstname_female.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                fist_name = unidecode.unidecode(random.choice(lines)).strip()
        # ten nam
        else:
            with open('D:/RegCloneFbDl/DataReg/infoacc/firstname_male.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                fist_name = unidecode.unidecode(random.choice(lines)).strip()  
        # Generate Phone Ảo         
        fake_number = f'{9195}{random.randint(1111, 9999)}{random.randint(1111, 9999)}'
        # password
        password = f'{fist_name.replace(" ","")}{random.randint(1111, 9999)}'

        system_cmd('KEYCODE_HOME')
        time.sleep(1)       
        click('spvpn.png', 3, 'Đang mở app facebook lite')
        click('cancel.png', 3, 'Đang mở app facebook lite')
        click('nothank.png', 3, 'Đang mở app facebook lite')
        click('chonvpn.png', 3, 'Đang mở app facebook lite')
        click(random_vpn, 1, 'Click chọn avata')
        system_cmd('KEYCODE_HOME')
        time.sleep(1)
        click('logo.png', 3, 'Đang mở app facebook lite')
        click('deny.png', 3, 'từ chối')
        click('tienganh.png', 3, 'Chuyển đổi ngôn ngữ sang tiếng anh')
        click('creatacc.png', 2, 'Tạo mới tài khoản')
        click('next.png', 1, 'Nhấn tiếp')       
        putdata('x', 0, '')
        system_cmd('KEYCODE_DEL')
        putdata(last_name, 5, 'Nhập Họ')
        click('lastname.png', 1, 'Nhấn sang ô nhập tên')
        putdata(fist_name, 5, 'Nhập tên')
        click('next.png', 2, 'Nhấn tiếp')
        click('deny.png', 3, 'từ chối')
        click('deny.png', 3, 'từ chối')
        click('deny.png', 3, 'từ chối')
        click('phone.png', 1, 'Nhấn đăng ký bằng sdt')       
        putdata(fake_number, 5, 'sdt')
        click('next.png', 2, 'Nhấn tiep')
        click('number0.png', 0, '0')
        click('number2.png', 0, '2')
        click('number2.png', 0, '2')
        click('number1.png', 0, '1')
        click('number1.png', 0, '1')
        click('number9.png', 0, '9')
        click('number9.png', 0, '9')
        click('number7.png', 0, '7')
        click('next.png', 2, 'Nhấn tiep')
        if sex == 1:
            click('nu.png', 2, 'Chọn giới tính nữ')
        else:
            click('nam.png', 2, 'Chọn giới tính nam')
        putdata('p', 0, '')
        system_cmd('KEYCODE_DEL')
        putdata(password, 8, 'Nhập mật khẩu')
        click('next.png', 2, 'Nhấn next')
        click('dangky.png', 20, 'Xác nhận tạo tài khoản')       
        click('notnow1.png', 2, 'Nhan luc khac')
        click('deny.png', 3, 'từ chối')
        click('seencode1.png', 3, 'lấy otp')
        click('thememail.png', 3, 'xác minh bằng mail')
        click('boxmail1.png', 1, 'Nhấn ô nhập mail')
        email = get_mail(1)
        putdata(email, 1, 'Nhập email mới')
        click('next.png', 1, 'Nhấn tiếp')
        save_info(email, password)
        click('deny.png', 3, 'từ chối')
        click('boxcode.png', 1, 'Nhấn o nhap mail')
        very_code(email, password)
        upload_infoacc()

    def upload_infoacc():
        click('taianhlen.png', 1, 'Bấm upload avata')
        click('taianhlen2.png', 1, 'Chọn ảnh có sẵn trong thiết bị')
        click('taixuong.png', 1, 'Chọn ảnh từ thư viện')
        click('avata.png', 1, 'Click chọn avata')
        click('luu.png', 5, 'Xác nhận lưu avata')
        system_cmd('KEYCODE_HOME')
        time.sleep(1)
        click('syssetting.png', 1, 'Nhấn Vào Cài Đặt Hệ Thống')
        click('settingapp.png', 1, 'Nhấn Vào Cài Đặt App')
        click('litesetting.png', 1, 'Nhấn Vào Cài Đặt Lite')
        click('appstop.png', 1, 'Nhấn Buộc Dừng Lite')
        click('okstop.png', 1, 'Xác Nhận Buộc Dừng Lite')
        system_cmd('KEYCODE_HOME')
        time.sleep(1)
        click('logo.png', 15, 'Đang mở app facebook lite')
        clear_data_lite()


    creat_acc()

# Setup luồng chạy / luong chay day anh nhe / vd anh muon chay 2 luong
data_runs = [
      {'id_divice': 'emulator-5554', 'part_png': 'D:/RegCloneFbDl/DataReg/screen/screenshot.png', 'part_obj': 'D:/RegCloneFbDl/DataReg/screen/', 'key_mail': 'lg7fn50dojkecvibc5focg7lju'},
      {'id_divice': 'emulator-5556', 'part_png': 'D:/RegCloneFbDl/DataReg/screen2/screenshot.png', 'part_obj': 'D:/RegCloneFbDl/DataReg/screen2/', 'key_mail': 'lg7fn55dojkecvibc5focg7lju'},
      {'id_divice': 'emulator-5558', 'part_png': 'D:/RegCloneFbDl/DataReg/screen3/screenshot.png', 'part_obj': 'D:/RegCloneFbDl/DataReg/screen3/', 'key_mail': 'lg7fn60dojkecvibc5focg7lju'},
      {'id_divice': 'emulator-5560', 'part_png': 'D:/RegCloneFbDl/DataReg/screen4/screenshot.png', 'part_obj': 'D:/RegCloneFbDl/DataReg/screen4/', 'key_mail': 'lg7fn65dojkecvibc5focg7lju'},
      {'id_divice': 'emulator-5562', 'part_png': 'D:/RegCloneFbDl/DataReg/screen5/screenshot.png', 'part_obj': 'D:/RegCloneFbDl/DataReg/screen5/', 'key_mail': 'lg7fn70dojkecvibc5focg7lju'},
#      {'id_divice': 'emulator-5564', 'part_png': 'D:/RegCloneFbDl/DataReg/screen2/screenshot.png', 'part_obj': 'D:/RegCloneFbDl/DataReg/screen2/', 'key_mail': 'lg7fn79dojkecvibc5focg7lju'}'
#      {'id_divice': 'emulator-5566', 'part_png': 'D:/RegCloneFbDl/DataReg/screen2/screenshot.png', 'part_obj': 'D:/RegCloneFbDl/DataReg/screen2/', 'key_mail': 'lg7fn80dojkecvibc5focg7lju'}'
#      {'id_divice': 'emulator-5568', 'part_png': 'D:/RegCloneFbDl/DataReg/screen2/screenshot.png', 'part_obj': 'D:/RegCloneFbDl/DataReg/screen2/', 'key_mail': 'lg7fn59dojkecvibc5focg7lju'}'
]

threads = []


for data_runs in data_runs:
    thread = threading.Thread(target=process_device, args=(data_runs,))
    thread.start()
    threads.append(thread)

# Chờ cho tất cả các luồng hoàn thành
for thread in threads:
    thread.join()
