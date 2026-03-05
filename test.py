import platform
import psutil
import os

# 输出 Python 版本
# print(f"Python 版本: {platform.python_version()}")

# # 输出 CPU 信息
# print(f"CPU 信息: {psutil.cpu_count(logical=False)}")

# # 输出 内存 信息
# print(f"内存 信息: {psutil.virtual_memory()}")

# # 输出 网卡 信息
# print(f"网络 信息: {psutil.net_io_counters()}")

# # 输出 显卡 信息
# try:
#     from GPUtil import getGPUs
#     print(f"显卡 信息: {[gpu.name for gpu in getGPUs()]}")
# except ImportError:
#     print("显卡 信息: 未安装 GPUtil")


# # 输出 磁盘 信息
# print(f"磁盘 信息: {[disk.mountpoint for disk in psutil.disk_partitions()]}")

# # 输出 进程 信息
# # print(f"进程 信息: {[process.name() for process in psutil.process_iter()]}")

# # 输出 用户 信息
# print(f"用户 信息: {[user.name for user in psutil.users()]}")


