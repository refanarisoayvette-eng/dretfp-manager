from .models import DemandeReinitialisation


def notifications(request):
    """Context processor pour les notifications."""
    if request.user.is_authenticated and request.user.is_staff:
        nb_demandes = DemandeReinitialisation.objects.filter(statut='En attente').count()
        return {
            'nb_notifications': nb_demandes,
        }
    return {
        'nb_notifications': 0,
    }