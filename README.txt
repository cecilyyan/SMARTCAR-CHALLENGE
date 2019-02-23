Smartcar Backend Challenge
***************************************************************************** 
Introduction:
The Generic Motors (GM) car company has a terrible API. It returns badly structured JSON which isn't always consistent. Smartcar needs to adapt the API into a cleaner format.
*****************************************************************************
Requirement:
In order to run this project, python 2 is required. Also, you need to install the JSON and  Flask.
*****************************************************************************
Design:
In my backend, first I use POST to send request to GM API and get the response, then convert the response into json type. I also use a checker which includes a check function to make sure the input is valid and legal.
Then I work with json parse, in order to adapt the GM API into a cleaner format.
1. Programming Language:
    -Python
2. Framework:
    -Flask
    -Implement blueprint in flask to handle URL routing.
3. Test:
    -Unittest
*****************************************************************************
Usage£º

Run the jsonParse.py first, by typing python jsonParse.py. Then Run the unit test by typing python test.py. Also you can manually test the server using cUrl command. Instructions are followed below.  

1. To test the basic vehicle information
eg. curl http://127.0.0.1:5000/vehicles/1234
This will return basic vehicle info in JSON format. 
for example:
{"color":"Metallic Silver","doorCount":4,"driveTrain":"v8","vin":"123123412412"}

2. To test the fuel level
eg. curl http://127.0.0.1:5000/vehicles/1234/fuel 
This will return fuel level in JSON format. Results should be the float number between 0 and 100.
for example:
{"percent":23.92}

3. To test the battery level
eg. curl http://127.0.0.1:5000/vehicles/1234/battery 
This will return battery level in JSON format. Results should be the float number between 0 and 100.
for example:
{"percent":0.0}


4. To test the lock condition of each door
eg. curl http://127.0.0.1:5000/vehicles/1234/doors
This will return battery level in JSON format. Results should be in boolean format.
for example:
[{"location":"frontLeft","locked":true},{"location":"backLeft","locked":true},{"location":"backRight","locked":true},{"location":"frontRight","locked":true}]


5. To test the engine command
curl --request POST --data '{"action": "STOP"}' -H "Content-Type: application/json" 
http://127.0.0.1:5000/vehicles/1234/engine 
We can send the stop or start command by change the action field to STOP or START. Results should be success or failure.
for example:
{"status":"success"}
