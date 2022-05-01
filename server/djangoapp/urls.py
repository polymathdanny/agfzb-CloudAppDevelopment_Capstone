from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('registration/', views.registrationPage, name="registration"),

    # path for logout
    path(route='', view=views.get_dealerships, name='index'),
    path('about/', views.aboutPage, name="about"),
    path('contact/', views.contactPage, name="contact"),
    # path for dealer reviews view
    path('dealerships/<str:pk>/<int:val>/', views.get_dealerships_by_id),
    path('dealerships/state/<str:val>/', views.get_dealerships_by_state),  
    # path for add a review view
    path('add_review', views.add_review, name="add_review")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
