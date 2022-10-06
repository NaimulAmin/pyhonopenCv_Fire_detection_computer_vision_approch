import threading
import smtplib
import cv2
import numpy as np
import playsound
Fire_Reported = 0
Alarm_Status = False
Email_Status = False


def play_alarm_sound_function():
	while True:
		playsound.playsound('alarm-sound.mp3',True)



# def send_mail_function():
#
#     recipientEmail = "Enter_Recipient_Email"
#     recipientEmail = recipientEmail.lower()
#
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.ehlo()
#         server.starttls()
#         server.login("Enter_Your_Email (System Email)", 'Enter_Your_Email_Password (System Email')
#         server.sendmail('Enter_Your_Email (System Email)', recipientEmail, "Warning A Fire Accident has been reported on ABC Company")
#         print("sent to {}".format(recipientEmail))
#         server.close()
#     except Exception as e:
#     	print(e)



video = cv2.VideoCapture('video.wmv')
#video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    frame = cv2.resize(frame, (1000,600))
    blur = cv2.GaussianBlur(frame, (15, 15), 0)

    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    no_red = cv2.countNonZero(mask)

    if int(no_red) > 8000:
        # this fire will be detected while no read in 10000
        print('fire detected')
        Fire_Reported = Fire_Reported + 1

        if Fire_Reported >= 1:

            if Alarm_Status == False:
                #play_alarm_sound_function()
                threading.Thread(target=play_alarm_sound_function).start()
                Alarm_Status = True

            # if Email_Status == False:
            #     threading.Thread(target=send_mail_function).start()
            #     Email_Status = True



    if ret == False:
        break

    cv2.imshow('output',output  )
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllwinddows()
video.release()
