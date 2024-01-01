import shutil

import cv2
import os

image_base_path = "./images/"


# 已经提取好了图片, x-xxx.png, 每隔split_num张取一张,重新排序放到S3文件夹中
def get_images_from_dir(dir_path, split_num):
    frame_times = -1
    file_num = -1
    image_out_path = dir_path + "_S" + str(split_num)
    if not os.path.exists(image_out_path):
        os.makedirs(image_out_path)
    # 不能直接遍历目录文件,会乱序
    while frame_times < len(os.listdir(dir_path)):
        frame_times = frame_times + 1
        if frame_times % split_num == 0:
            file_num = file_num + 1
            shutil.copyfile(dir_path + "/" + str(frame_times) + ".png", image_out_path + "/frame_" + str(file_num) + ".png")


# 从视频中提取图片
def get_images(video_path):
    frame_times = -1
    fileName = video_path.split("/")[-1:][0].split('.')[0]
    image_out_path = image_base_path + fileName
    if not os.path.exists(image_out_path):
        os.makedirs(image_out_path)
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        frame_times = frame_times + 1
        success, frame = cap.read()
        if not success:
            break
        cv2.imencode('.png', frame)[1].tofile(image_out_path + "/frame_" + str(frame_times) + ".png")


if __name__ == '__main__':
    get_images('你的视频目录/dance_out_v2.mp4')  # 提取视频中的图片
    get_images_from_dir(image_base_path + 'dance_out_v2', 4)  # 提取图片文件夹中的图片
    