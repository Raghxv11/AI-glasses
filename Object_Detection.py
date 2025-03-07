def object_detect():    
    import cv2
    import numpy as np
    from datetime import datetime
    import gtts
    import playsound
    import os

    net = cv2.dnn.readNet('yolov3.weights','yolov3.cfg')
    classes=[]
    with open('coco.names','r') as f:
        classes = f.read().splitlines()
    
    nameList = []
    def logs(name):
        
        if name not in nameList:
            nameList.append(name)
            audio = name + "ahead"
            print(name)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            audio_folder = "audios"  # Specify the folder name
            audio_file_name = f"{name}_{timestamp}.mp3"
            audio_file_path = os.path.join(audio_folder, audio_file_name)
            sound = gtts.gTTS(audio, lang="en")
            sound.save(audio_file_path)
            playsound.playsound(audio_file_path)

    cap = cv2.VideoCapture(0)
    
    while True:
        _,img = cap.read()
        height,width,_ = img.shape

        blob = cv2.dnn.blobFromImage(img,1/255,(416,416),(0,0,0),swapRB=True,crop=False)
        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        layerOutputs = net.forward(output_layers_names)

        boxes=[]
        confidences=[]
        class_ids=[]

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0]*width)
                    center_y = int(detection[1]*height)
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)
                    x= int(center_x-w/2)
                    y = int(center_y-h/2)
                    boxes.append([x,y,w,h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)
                
        indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.5,0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0,255,size = (len(boxes),3))
        for i in indexes.flatten():
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            color = colors[i]
            cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
            cv2.putText(img,label+ " "+confidence,(x,y+20),font,2,(255,255,255),2)
            logs(label)
        cv2.imshow('Image',img)
        # cv2.waitKey(0)
        key = cv2.waitKey(1)
        if key==27:
            break


    cap.release()
    cv2.destroyAllWindows()    


