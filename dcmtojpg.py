
import SimpleITK
import cv2
import os

dcm_path='./20200827034939394'
jpg_path="./20200827034939394_jpg"

def Dcm2jpg(dicom_dir): #用simpleITK读取dcm文件

    reader = SimpleITK.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dicom_dir)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    img_array = SimpleITK.GetArrayFromImage(image)
    img_array[img_array == -2000] = 0

    print('all is changed',img_array.shape)
    return img_array
def normalize_hu(image):
    '''
           将输入图像的像素值(-4000 ~ 4000)归一化到0~1之间
       :param image 输入的图像数组
       :return: 归一化处理后的图像数组
    '''
    MIN_BOUND = -1000.0
    MAX_BOUND = 400.0
    image = (image - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
    image[image > 1.] = 1.
    image[image < 0.] = 0.
    return image

names = os.listdir(dcm_path)
image=Dcm2jpg(dcm_path)

for i in range(image.shape[0]):
    new_name=names[i].replace(".dcm","")
    img_path = jpg_path +'/'+ new_name + ".jpg"
    org_img = normalize_hu(image[i])
    cv2.imwrite(img_path, org_img * 255)
