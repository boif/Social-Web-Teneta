from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from Profile import views, forms
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/',
         LoginView.as_view
             (
             template_name='registration/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/subscribers/', views.subscribersPage, name='subscribers'),
    path('profile/<str:username>/subscribes/', views.subscribesPage, name='subscribes'),
    path('subscribe/<str:username>/', views.subscribe, name='subscribe'),
    path('unsubscribe/<str:username>/', views.unsubscribe, name='unsubscribe'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)