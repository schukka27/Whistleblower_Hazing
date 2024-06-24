from django.urls import path
from . import views

app_name = 'orgreport'
urlpatterns = [
    # ex: /orgreport/login
    path("login/", views.login, name="login"),
    # ex: /orgreport/home
    path("home/", views.home, name="home"),
    path('find_resources/', views.find_resources, name='find_resources'),
    path('search_reports/', views.search_reports, name='search_reports'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('home/uploaded_files/', views.s3_folder_view, name='s3_folder_view'),
    path("logout/", views.logout_view, name="logout"),
    path("download_file/<path:file_key>/", views.download_file, name="download_file"),
    path("report/", views.report, name="report"),
    path("profile/", views.profile, name="profile"),
    path('user_report/<int:report_id>/', views.report_detail_user, name='report_detail_user'),
    path('delete_report/<int:report_id>/', views.delete_report, name='delete_report'),
]

