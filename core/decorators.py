from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles_autorises):
    """Decorateur pour restreindre l'acces selon le role."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Admin a toujours acces
            if request.user.is_staff:
                return view_func(request, *args, **kwargs)
            
            # Verifier le role
            try:
                profil = request.user.profil
                if profil.role in roles_autorises:
                    return view_func(request, *args, **kwargs)
            except:
                pass
            
            messages.error(request, "Vous n'avez pas les droits pour acceder a cette page.")
            return redirect('accueil')
        
        return wrapper
    return decorator