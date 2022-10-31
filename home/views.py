from modules import *
globals().update(import_modules('home.views', globals()))


# Create your views here.
@never_cache
@require_http_methods(['GET'])
def index(request):
    db_pre_process(request)
    return render(request, 'home/index.html', index_vars())


@csp_exempt
@never_cache
@require_http_methods(['GET'])
def notif_verify_email(request):
    db_pre_process(request)
    return render(request, 'home/notif_verify_email.html', notif_verify_email_vars())


@csp_exempt
@never_cache
@require_http_methods(['GET'])
def terms_of_service(request):
    db_pre_process(request)
    return render(request, 'home/terms_of_service.html', terms_of_service_vars())


@csp_exempt
@never_cache
@require_http_methods(['GET'])
def privacy_policy(request):
    db_pre_process(request)
    return render(request, 'home/privacy_policy.html', privacy_policy_vars())


@never_cache
@require_http_methods(['GET'])
def verified(request, url):
    db_pre_process(request)
    db_verify_email(url)
    return HttpResponseRedirect(reverse('home:login'))


@never_cache
@require_http_methods(['GET', 'POST'])
def OTPP(request):
    db_pre_process(request)
    OTPP_session_id = request.session.get('OTPP_session_id', '')
    if request.method == 'POST' and db_OTPP_session_id(OTPP_session_id):
        data = request.POST
        if 'OTPP' in data:
            OTPP = data['OTPP']
            if db_verify_OTPP(OTPP_session_id, OTPP):
                request.session['session_id'] = db_verify_OTPP(OTPP_session_id, OTPP, update = True)
                return HttpResponseRedirect(reverse('account:dashboard'))
            db_verify_OTPP(OTPP_session_id, OTPP, unverified = True)
            return HttpResponseRedirect(reverse('home:login'))
        return HttpResponseRedirect(reverse('home:login'))
    if db_OTPP_session_id(OTPP_session_id):
        return render(request, 'home/OTPP.html', OTPP_vars(OTPP_session_id))
    return HttpResponseRedirect(reverse('home:login'))


@never_cache
@require_http_methods(['GET', 'POST'])
def login(request):
    db_pre_process(request)
    TOSAPP = request.session.get('TOSAPP', False)
    if request.method == 'POST':
        data = request.POST
        if 'TOSAPP' in data:
            request.session['TOSAPP'] = True
            return HttpResponseRedirect(reverse('home:login'))
        if all (key in data for key in ('forgot_password', 'email')) and TOSAPP:
            if data['email']:
                email = data['email']
                db_forgot_pass(email)
            return HttpResponseRedirect(reverse('home:login'))
        if all (key in data for key in ('email', 'password')) and TOSAPP:
            if data['email'] and data['password']:
                email = data['email']
                password = data['password']
                if db_login(email, password):
                    request.session.cycle_key()
                    request.session['OTPP_session_id'] = db_send_OTPP(email)
                    return HttpResponseRedirect(reverse('home:OTPP'))
                if db_account(email):
                    return HttpResponseRedirect(reverse('home:login'))
                if db_signed_up(email) == False:
                    url = secret_url()
                    if validate_email(email, url) == True:
                        db_sign_up(email, password, url)
                return HttpResponseRedirect(reverse('home:notif_verify_email'))
            return HttpResponseRedirect(reverse('home:login'))
        return HttpResponseRedirect(reverse('home:login'))
    if TOSAPP:
        return render(request, 'home/login.html', login_vars())
    return render(request, 'home/TOSAPP.html', TOSAPP_vars())

