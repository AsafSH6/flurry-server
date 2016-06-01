# import django
# django.setup()
#
# from flurryapp.models import *
# print len(Driver.objects.get(id=7).driving_data.data[0]['speed'])
# print len(Driver.objects.get(id=7).driving_data.data[0]['rpm'])
# print len(Driver.objects.get(id=7).driving_data.data[0]['throttle_pos'])
# print len(Driver.objects.get(id=7).driving_data.data[0]['engine_load'])
# print Driver.objects.all()
# Profile.objects.create_new_profile_for_driver(driver_obj=Driver.objects.get(id=7))
# print [1, 2] > 5
# data_driver = DataDriver(data={
#     'name': 'Mor',
# }).save()
#
# print data_driver.data
#
# driver = Driver(name='Mor', driving_data=+data_driver).save()
#
# print driver
#
# car1 = Car(manufacturer='bla1', production_year=1995, model='blabka1', owner=driver).save()
# car2 = Car(manufacturer='bla2', production_year=1995, model='blabka2', owner=driver).save()
#
# print car1
# print car2
#
# profile = Profile(driver=driver).save()
#
# print profile
#
# print '\n\n~~~~~~~~~~~~~~~~~~\n\n'
#
# print driver.cars.all()
#
# print driver.profiles.all()


# import numpy as np
#
# arr = np.array([])
# print arr.add(1)


print [1, 2, 3] + [5, 6]