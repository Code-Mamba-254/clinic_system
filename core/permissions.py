from django.http import HttpResponseForbidden


def is_doctor(user):
    return user.groups.filter(name="Doctor").exists()


def is_receptionist(user):
    return user.groups.filter(name="Receptionist").exists()


def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Admin").exists()


# -----------------------------
# DECORATORS (REAL PROTECTION)
# -----------------------------

def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if is_doctor(request.user):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Doctors only.")
    return wrapper


def receptionist_required(view_func):
    def wrapper(request, *args, **kwargs):
        if is_receptionist(request.user):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Reception only.")
    return wrapper


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if is_admin(request.user):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Admins only.")
    return wrapper