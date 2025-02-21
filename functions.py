import os
import shutil
import tqdm
HEADER_SIZE = 10
FILE_HEADER = 20
BUF_SIZE = 2048

def calculate_next(**kwargs):
    param = kwargs.get("parameters").split("=")
    num = int(param[1])
    num += 1
    with open("file_result.txt", "w") as f:
        f.write(str(num))

    return "file_result.txt"

def sub_calculate_area(base=10, hight=10):
    return base*hight/2

def calculate_area(**kwargs):
    param = kwargs.get("parameters").split("&")
    num1 , num2 = int(param[0].split("=")[1]), int(param[1].split("=")[1])
    area = sub_calculate_area(num1,num2)

    with open("file_result.txt", "w") as f:
        f.write(str(area))

    return "file_result.txt"


def upload(**kwargs):
    try:
        client_socket = kwargs.get('socket')
        file_size = int(kwargs.get("size"))
        file_name = kwargs.get("parameters").split("=")[1]
        folder = "upload"
        if file_name == "" or not file_size:
            return None
        folder_path = os.path.join(os.getcwd(), folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder)

        file_name = os.path.join(folder_path, file_name)  # folder_path+'\\'+ file_name

        with open(file_name, 'wb') as file:
            data_recv = 0
            while data_recv < file_size:
                line = client_socket.recv(BUF_SIZE)
                file.write(line)
                data_recv += len(line)

        with open("file_result.txt", "w") as f:
            f.write(f"uploaded {str(file_size)}")

        return "file_result.txt"

    except Exception as e:
        print(e)
        return None

def image(**kwargs):
    file_name = kwargs.get("parameters").split("=")[1]
    if os.path.exists(file_name):
        return file_name
    with open("file_result.txt", "w") as f:
        f.write("no such file found")

    return "file_result.txt"