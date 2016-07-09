from django.conf.urls import url
from rest_framework_extensions.routers import ExtendedDefaultRouter
from flurryapp import viewsets


router = ExtendedDefaultRouter()

router.register(r'data-drivers', viewsets.DataDriverViewSet, base_name='datadriver')\
    .register(r'drivers', viewsets.DriverViewSet,  base_name='data-drivers-driver', parents_query_lookups=['data_driver'])

router.register(r'users', viewsets.UserViewSet, base_name='users')\
    .register(r'drivers', viewsets.DriverViewSet, base_name='user-drivers', parents_query_lookups=['user'])

drivers_router = router.register(r'drivers', viewsets.DriverViewSet, base_name='drivers')

urlpatterns = router.urls

urlpatterns += [url(r'user-log-in/', viewsets.UserLogInAPIViewSet.as_view(), name='user_log_in')]
