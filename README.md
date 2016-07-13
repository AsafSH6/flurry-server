# Flurry
_Collecting drivers driving data for self and academic use_

---

Flurry project helps you to collect data from experimenters using Android application and OBD-II device <img src="http://cf3.souqcdn.com/item/2013/11/25/63/61/64/4/item_XL_6361644_3688334.jpg" width="100"> 


# Server

Django Rest Framework API- easy to understand and use.

You are welcome to use our server: https://flurry.herokuapp.com/api/v1/flurry/
or manage your own:

- Clone Flurry project
- Create PostgreSQL database
- Edit flurry.settings
- Set environment variables: SECRET_KEY, DEBUG, HERE_API_APP_ID and HERE_API_APP_CODE
- Run: python manage.py makemigrations and then python manage.py migrate

*HERE_API_APP* tokens are used in order to detect what is the maximum limitation of speed in a current location.
you can get them from https://developer.here.com/

#### Querying the server
If you're familiar with Django Rest Framework then it will be very easy for you to understand the api.

1. List of drivers:
```bash
$ curl https://flurry.herokuapp.com/api/v1/flurry/drivers/
>> [
    {
      "id": 1,
      "user": {"id": 24, "username": "test"},
      "name": "Test Driver",
      "creation_date": "2016-07-13", 
      "driving_data": "https://flurry.herokuapp.com/api/v1/flurry/data-drivers/3/"
    },
    ...
]
```
_"driving_data"_: url of the driver driving data.  
2. Specific driver: 
```bash
$ curl https://flurry.herokuapp.com/api/v1/flurry/drivers/{driver_id}/
>> {
      "id": {driver_id},
      "user": {"id": 24, "username": "test"},
      "name": "Test Driver",
      "creation_date": "2016-07-13", 
      "driving_data": "https://flurry.herokuapp.com/api/v1/flurry/data-drivers/3/"
    },
```   
3. Driver driving data: 
list of lists where each list is a ride data.
ride data is a list of jsons where each json is the driving data for specific time
given that "Test Driver" driving data id id 3:
```bash
$ curl https://flurry.herokuapp.com/api/v1/flurry/data-drivers/3/
>> {
    "id": 3,
    "data": [
        [  // begin ride number 1
            {
                "throttle": "25.490196",
                "rpm": "839",
                "maximum_limition_of_speed": 30.0,
                "time": "1463043516031",
                "speed": "0",
                "gps": {
                    "lat": "31.87628096",
                    "lon": "34.9199814"
                }
            },
            {
                "throttle": "25.490196",
                "rpm": "858",
                "maximum_limition_of_speed": 30.0,
                "time": "1463043517152",
                "speed": "9",
                "gps": {
                    "lat": "31.87628096",
                    "lon": "34.9199814"
                }
            },
            {
                "throttle": "20.392157",
                "rpm": "2566",
                "maximum_limition_of_speed": 50.0,
                "time": "1463043543250",
                "speed": "22",
                "gps": {
                    "lat": "31.87641365",
                    "lon": "34.92051463"
                }
            },
            {
                "throttle": "94.90196",
                "rpm": "1545",
                "maximum_limition_of_speed": 50.0,
                "time": "1463043549281",
                "speed": "16",
                "gps": {
                    "lat": "31.8763137",
                    "lon": "34.9208201"
                }
            },
        ], // end ride number 1
        [ // begin ride number 2
        ...
        ], // end ride number 2
        ....
    ]
}
```   
4. Specific ride:
get the specific ride of driver by passing the parameter "ride"
ride parameter starts from 0 (the first ride) and also supports negative index: ride=-1 => last ride
```bash
$ curl https://flurry.herokuapp.com/api/v1/flurry/data-drivers/3/?ride=2
>> [
     {
        "load": "56.47059",
        "throttle": "20.784313",
        "rpm": "1274",
        "maximum_limition_of_speed": 50.0,
        "time": 1468406223678,
        "speed": "10",
        "gps": {
            "lat": "31.89901517",
            "lon": "35.00820239"
        }
    },
    {
        "load": "54.901962",
        "throttle": "20.392157",
        "rpm": "919",
        "maximum_limition_of_speed": 50.0,
        "time": 1468406224989,
        "speed": "10",
        "gps": {
            "lat": "31.89901517",
            "lon": "35.00820239"
        }
    },
    {
        "load": "34.901962",
        "throttle": "17.647058",
        "rpm": "862",
        "maximum_limition_of_speed": 50.0,
        "time": 1468406226479,
        "speed": "6",
        "gps": {
            "lat": "31.89901517",
            "lon": "35.00820239"
        }
    },
    ...
]
```   
5. specific data unit of specific ride:
get the specific data unit by passing the parameter "data_unit". 
data_unit parameter starts from 0 (the first data unit of the given ride) and also supports negative index: ride=-1 => last data unit
```bash
$ curl https://flurry.herokuapp.com/api/v1/flurry/data-drivers/3/?ride=2&data_unit=-1
>> {
        "load": "26.666666",
        "throttle": "17.647058",
        "rpm": "854",
        "maximum_limition_of_speed": 50.0,
        "time": 1468407153683,
        "speed": "0",
        "gps": {
            "lat": "31.89163008",
            "lon": "34.92453954"
        }
}
```   
6. get details about specific driver driving data:
```bash
$ curl https://flurry.herokuapp.com/api/v1/flurry/data-drivers/3/len/
>> {
    "number of rides": 55,
    "number of data units": 50357
}
```
