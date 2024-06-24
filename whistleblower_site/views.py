from django.contrib.auth import logout
import boto3
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
import mimetypes
from django.core.exceptions import ValidationError
import os

from django.urls import reverse
from .models import Report, User, ReportFile
from .forms import ReportForm

from django.http import HttpResponse

def logout_view(request):
    logout(request)
    return render(request, "whistleblower_site/login.html")

def login(request):
    # Log out any user who is currently logged in
    if request.user.is_authenticated:
        logout(request)
    return render(request, "whistleblower_site/login.html")

def home(request):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    #If the user logged in
    if user.is_authenticated:
        users = User.objects.all()
        #Search for the user in the database
        for ind_user in users:
            #If the user is in the database, return the home page with the user's information
            if ind_user.email == user.email:
                return render(request, "whistleblower_site/home.html", {'user': user, 'user_groups': user_groups})
        #If the user is not in the database, add them with their first name, last name, and email
        new_user = User(first_name=user.first_name, last_name=user.last_name, email=user.email)
        new_user.save()

    return render(request, "whistleblower_site/home.html", {'user': user, 'user_groups': user_groups})

def download_file(request, file_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    bucket_name = 'org-report-storage-bucket'
    file_path = 'org-report-uploaded-files/' + file_key

    try:
        # Retrieve the file object from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_path)
        file_content = response['Body'].read()

        # Determine the file's MIME type based on its extension
        content_type, _ = mimetypes.guess_type(file_key)
        if not content_type:
            content_type = 'application/octet-stream'

        # Serve the file content as the HTTP response with appropriate content type
        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{file_key}"'
        return response
    except Exception as e:
        # Return a 404 error if the file does not exist or there's an error retrieving it
        return HttpResponse(status=404)

def s3_folder_view(request):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    organization_query = request.GET.get('org')
    after_query = request.GET.get('after')
    before_query = request.GET.get('before')
    reset_query = request.GET.get('reset')
    status_query = request.GET.get('status')
    reports = Report.objects.all()

    if reset_query:
        organization_query=None
        after_query=None
        before_query=None
        status_query=None
        reports = Report.objects.all()
    else:
        if organization_query:
            reports = reports.filter(organization__icontains=organization_query)
        if after_query:
            reports = reports.filter(date__gte=after_query)
        if before_query:
            reports = reports.filter(date__lte=before_query)
        if status_query:
            if status_query == 'In Progress':
                status_query = 'in_progress'
            elif status_query == 'All':
                status_query = ''
            reports = reports.filter(status__icontains=status_query)

    report_data = [{
    'report': report,
    'status': report.status,
    'admin_notes': report.admin_notes,
    } for report in reports]

    return render(request, 'whistleblower_site/s3_folder_view.html', {
        'report_data': report_data, 
        'user': user, 
        'user_groups': user_groups,
        'organization_query':organization_query, 
        'after_query':after_query, 
        'before_query':before_query, 
        'status_query':status_query,
        'reset_query':reset_query
    })



def report(request):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    if request.method == 'POST':
        return upload_file(request)
    return render(request, "whistleblower_site/report.html", {'user': user, 'user_groups': user_groups})

ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.jpg']

def validate_file_extension(file):
    # Extract the file extension
    _, extension = os.path.splitext(file.name)
    if extension.lower() not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'Unsupported file type. Only {", ".join(ALLOWED_EXTENSIONS)} files are allowed.')

def upload_file(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    form = ReportForm(request.POST, request.FILES)
    if form.is_valid():
        report = form.save(commit=False)
        if request.user.is_authenticated:
            try:
                user = User.objects.get(email=request.user.email, first_name=request.user.first_name, last_name=request.user.last_name)
                report.user = user
                report.anonymous_account = False
            except User.DoesNotExist:
                pass
        else:
            report.anonymous_account = True
        report.save()
    else: 
        return render(request, 'whistleblower_site/report.html', {'user': request.user, 'user_groups': user_groups})
    
    if 'file' in request.FILES:
        files = request.FILES.getlist('file')
        for file in files:
            try:
                validate_file_extension(file)
                ReportFile.objects.create(report=report, file=file)
            except ValidationError as e:
                return render(request, 'whistleblower_site/report.html', {'user': request.user, 'user_groups': user_groups, 'error': e.message}) 
        return render(request, 'whistleblower_site/report.html', {'user': request.user, 'user_groups': user_groups, 'submitted': True})
    else:
        return render(request, 'whistleblower_site/report.html', {'user': request.user, 'user_groups': user_groups, 'submitted': True})

def find_resources(request):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    return render(request, "whistleblower_site/resources.html", {'user': user, 'user_groups': user_groups})

def search_reports(request):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    organization_query = request.GET.get('org')
    after_query = request.GET.get('after')
    before_query = request.GET.get('before')
    reset_query = request.GET.get('reset')

    reports = Report.objects.filter(publish=True)
    if reset_query:
        organization_query=None
        after_query=None
        before_query=None
        reports = Report.objects.filter(publish=True)
    else:
        if organization_query:
            reports = reports.filter(organization__icontains=organization_query)
        if after_query:
            reports = reports.filter(date__gte=after_query)
        if before_query:
            reports = reports.filter(date__lte=before_query)
    return render(request, "whistleblower_site/search_reports.html", {'reports': reports, 'user': user, 'user_groups': user_groups, 'organization_query':organization_query, 'after_query':after_query, 'before_query':before_query, 'reset_query':reset_query})


def report_detail(request, report_id):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    report = get_object_or_404(Report, pk=report_id)
    if 'admin' in request.user.groups.values_list('name', flat=True) and report.status == 'new':
        report.status = 'in_progress'
        report.save()

    context = {
        'report': report,
        'user': user,
        'user_groups': user_groups
    }

    if request.method == 'POST':
        new_status = request.POST.get('status', report.status)
        valid_statuses = ['in_progress', 'resolved']
        if new_status in valid_statuses:
            report.status = new_status
        report.admin_notes = request.POST.get('admin_notes', report.admin_notes)
        report.save()
        context['report'] = report
        return render(request, 'whistleblower_site/report_detail.html', context)

    return render(request, 'whistleblower_site/report_detail.html', context)


def profile(request):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    reports = Report.objects.filter(user__email=user.email)

    report_data = [{
        'report': report,
        'status': report.status,
        'admin_notes': report.admin_notes,
    } for report in reports]

    return render(request, 'whistleblower_site/profile.html', {
        'report_data': report_data,
        'user': user,
        'user_groups': user_groups
    })


def report_detail_user(request, report_id):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    report = get_object_or_404(Report, pk=report_id)

    if 'admin' in request.user.groups.values_list('name', flat=True) and report.status == 'new':
        report.status = 'in_progress'
        report.save()

    context = {
        'report': report,
        'user': user,
        'user_groups': user_groups
    }

    if request.method == 'POST':
        new_status = request.POST.get('status', report.status)
        valid_statuses = ['in_progress', 'resolved']
        if new_status in valid_statuses:
            report.status = new_status
        report.admin_notes = request.POST.get('admin_notes', report.admin_notes)
        report.save()
        context['report'] = report
        return render(request, 'whistleblower_site/report_detail_user.html', context)

    return render(request, 'whistleblower_site/report_detail_user.html', context)

def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.delete()
    return redirect('orgreport:profile')