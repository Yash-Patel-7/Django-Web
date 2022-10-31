from modules import *
globals().update(import_modules('account.views', globals()))


# Create your views here.
@never_cache
@require_http_methods(['GET', 'POST'])
def dashboard(request):
    db_pre_process(request)
    session_id = request.session.get('session_id', '')
    if request.method == 'POST' and db_session_id(session_id):
        data = request.POST
        if 'log_out' in data:
            db_log_out(session_id)
            return HttpResponseRedirect(reverse('home:login'))
        return HttpResponseRedirect(reverse('home:login'))
    if db_session_id(session_id):
        return render(request, 'account/dashboard.html', dashboard_vars(session_id))
    return HttpResponseRedirect(reverse('home:login'))


@never_cache
@require_http_methods(['GET', 'POST'])
def reset_password(request, url):
    db_pre_process(request)
    if request.method == 'POST' and allowed_reset_pass_url(url):
        data = request.POST
        if 'password' in data:
            password = data['password']
            update_password(url, password)
            return HttpResponseRedirect(reverse('home:login'))
        return HttpResponseRedirect(reverse('home:login'))
    if allowed_reset_pass_url(url):
        return render(request, 'account/reset_password.html', reset_password_vars(url))
    return HttpResponseRedirect(reverse('home:login'))


@never_cache
@require_http_methods(['GET', 'POST'])
def admin(request):
    db_pre_process(request)
    session_id = request.session.get('session_id', '')
    if request.method == 'POST' and db_session_id(session_id):
        permissions = db_permissions(session_id)
        if permissions.get('admin') == 'True':
            data = request.POST
            if 'example' in data:
                pass
                return HttpResponseRedirect(reverse('account:admin'))
        return HttpResponseRedirect(reverse('home:login'))
    if db_session_id(session_id):
        permissions = db_permissions(session_id)
        if permissions.get('admin') == 'True':
            return render(request, 'account/admin.html', admin_vars())
    return HttpResponseRedirect(reverse('home:login'))

