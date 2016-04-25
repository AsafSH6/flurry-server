import requests as req
r = req.get('https://roads.googleapis.com/v1/speedLimits?path=60.170880,24.942795&key=AIzaSyBxpwRBSBUDhnVM66L8xgChJSHUZ6Ni6sc')
print r
print r.json()