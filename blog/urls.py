from django.urls import path
from blog import views

urlpatterns = [

    path('',views.PostsView.as_view(),name="home"),
    path('logout',views.LogoutView.as_view(),name="logout"),
    path('login',views.LoginView.as_view(),name="login"),
    path('register',views.RegisterView.as_view(),name="register"),
    path('post/new',views.PostCreationView.as_view(),name="create_post"),
    path('post/<slug>',views.PostDetailView.as_view(),name="detail_post"),
    path('comment/<slug>',views.CommentCreationView.as_view(),name="add_comment")
]