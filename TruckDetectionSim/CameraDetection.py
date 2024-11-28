import os
from ultralytics import YOLO
import cv2 as cv
import time
import oci

#Función para verificar si existe un bucket en el Object Storage
def create_bucket(object_storage, namespace, bucket_name):
    try:
        object_storage.get_bucket(namespace, bucket_name)
        print(f"Bucket {bucket_name} already exists")
    except oci.exceptions.ServiceError as e:
        if e.status == 404:
            print(f"Creating bucket {bucket_name}")
            object_storage.create_bucket(namespace, oci.object_storage.models.CreateBucketDetails(name=bucket_name))
        else:
            raise

#Función para subir un archivo al Object Storage
def upload_file(object_storage, namespace, bucket_name, file_path):
    upload_manager = oci.object_storage.UploadManager(object_storage, max_parallel_uploads=3)
    if os.path.isfile(file_path):
        file_name = os.path.basename(file_path)  
        print(f"Uploading {file_path}")
        upload_manager.upload_file(namespace, bucket_name, file_name, file_path)
    else:
        print(f"The path {file_path} is not a valid file.")

#Función para detectar camiones en un video y subir una imagen al Object Storage
def truck_detection():
    MODEL_PATH_VIDEO = 'last.pt' #Modelo entrenado con YOLOv8
    VIDEO_PATH = 'Videos/Truck_Zona_3_BLM11077.mp4'

    model = YOLO(MODEL_PATH_VIDEO)
    output_folder='detected_frames'

    #Para mandar la imagen al Object Storage debe tener un archivo 'config' en la carpeta .oci
    config = oci.config.from_file(r".oci\config", "DEFAULT") #Cambiar por la ruta de su archivo config de ser necesario
    object_storage = oci.object_storage.ObjectStorageClient(config)
    namespace = object_storage.get_namespace().data

    bucket_name = "nombre_del_bucket" #Cambiar por el nombre de su bucket de Object Storage

    frame_count = 0
    times = 0

    video_predict = model.predict(VIDEO_PATH, stream=True, show=True, conf=0.8)

    for results in video_predict:
        frame_count += 1
        
        frame = results.orig_img
        markedTime = cv.putText(frame, "Zona 3", (180, 140), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        frame = cv.resize(markedTime, (1366, 768))

        for box in results.boxes:
            class_id = box.cls.item()
            class_name = model.names[class_id]
            confidence = box.conf.item() 

            if confidence >= 0.80 and confidence < 0.90:
                times += 1
                print(times)

            if class_name == 'truck' and times == 10:
                    
                frame_time = time.strftime("%Y%m%d-%H%M%S")
                frame_filename = os.path.join(output_folder, f"frame{frame_time}.jpg")
                cv.imwrite(frame_filename, frame)                
                    
                create_bucket(object_storage, namespace, bucket_name)
                upload_file(object_storage, namespace, bucket_name, frame_filename)
                    
                print(f"Saved: {frame_filename}")
                return    
                

def main():
    truck_detection()    
    
if __name__ == '__main__':
    main()