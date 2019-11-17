import requests, json, base64
import picamera


camera = picamera.PiCamera()
camera.resolution = (1000, 1000)
camera.start_preview()
camera.capture('snapshot.jpg')
camera.stop_preview()

with open("snapshot.jpg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(my_string)

endPoint = "https://green-house-monitor.herokuapp.com/evaluate"

requestBody = { 'payload': mystring}

requestHeaders = {'Content-Type': 'application/json'}

result = requests.post(url = endPoint, json = requestBody, headers= requestHeaders)
print(result.text)
