from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import (
    UserProfileViewSet,
    UserInterestViewSet,
    UserCompanyViewSet,
    UserIndustryViewSet
)

router = DefaultRouter()
router.register('profiles', UserProfileViewSet, basename='profile')
router.register('interests', UserInterestViewSet, basename='interest')
router.register('companies', UserCompanyViewSet, basename='company')
router.register('industries', UserIndustryViewSet, basename='industry')

urlpatterns = [
    path('', include(router.urls)),
]
