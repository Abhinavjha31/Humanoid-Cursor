import cv2
import mediapipe as mp
import pyautogui
import pyaudio
import speech_recognition as sr
import time

print("enter your choice")
print("1 for eye ")
print("2 for hand")
print("3 for speech")
print("0 to exit")
a=int(input())

if(a==1):
    cam= cv2.VideoCapture(0)
    face_mesh=mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h =pyautogui.size()
    while True:
        _, frame= cam.read()
        frame =cv2.flip(frame, 1)
        rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output=face_mesh.process(rgb_frame)
        landmark_points=output.multi_face_landmarks
        frame_h, frame_w ,_=frame.shape
        if landmark_points:
            landmarks=landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x=int(landmark.x * frame_w)
                y=int(landmark.y * frame_h)
                cv2.circle(frame, (x,y), 3 ,(0,0,255))
                if id==1:
                    screen_x=screen_w/frame_w*x
                    screen_y=screen_h/frame_h*y
                    pyautogui.moveTo(screen_x,screen_y)
            left=[landmarks[145],landmarks[159]]
            for landmark in left:
                x=int(landmark.x * frame_w)
                y=int(landmark.y * frame_h)
                cv2.circle(frame, (x,y), 3 ,(0,255,0))
            if (left[0].y-left[1].y) < 0.004:
                pyautogui.click()
                pyautogui.sleep(0.5)
        cv2.imshow("eye",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

elif(a==2):
    cap = cv2.VideoCapture(0)
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()
    index_y = 0
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x*frame_width)
                    y = int(landmark.y*frame_height)
                    if id == 8:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                        index_x = screen_width/frame_width*x
                        index_y = screen_height/frame_height*y

                    if id == 4:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                        thumb_x = screen_width/frame_width*x
                        thumb_y = screen_height/frame_height*y
                        print('outside', abs(index_y - thumb_y))
                        if abs(index_y - thumb_y) < 20:
                            pyautogui.click()
                            pyautogui.sleep(0.5)
                        elif abs(index_y - thumb_y) < 100:
                            pyautogui.moveTo(index_x, index_y)
        cv2.imshow('Virtual Mouse', frame)
        cv2.waitKey(1)

elif(a==3):
    r = sr.Recognizer()

# set up the audio stream
chunk_size = 1024  # number of audio samples per chunk
sample_rate = 44100  # number of audio samples per second
audio_format = pyaudio.paInt16  # audio format (16-bit integer)
num_channels = 1  # number of audio channels (mono)
stream = pyaudio.PyAudio().open(format=audio_format,
                                channels=num_channels,
                                rate=sample_rate,
                                input=True,
                                frames_per_buffer=chunk_size)

# listen for speech and convert to text
print("Speak now!")
audio_buffer = []
while True:
    # read a chunk of audio data from the stream
    data = stream.read(chunk_size, exception_on_overflow=False)
    audio_buffer.append(data)
    
    # check if speech has stopped (silence for at least 1 second)
    if len(audio_buffer) > sample_rate / chunk_size:
        audio_buffer.pop(0)  # remove oldest audio chunk
        audio_signal = b''.join(audio_buffer)
        try:
            audio_data = sr.AudioData(audio_signal, sample_rate=sample_rate, sample_width=2)
            text = r.recognize_google(audio_data)
            print("You said: " + text)
            break
        except sr.UnknownValueError:
            print("Speech was unintelligible.")
        except sr.RequestError as e:
            print("Error: {0}".format(e))
            print("Retrying in 5 seconds...")
            time.sleep(5)
            continue
        audio_buffer = []  # reset audio buffer

    elif(a==0):
        exit()
    else:
        print("Wrong Choice")
        exit()