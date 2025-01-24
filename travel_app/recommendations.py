import numpy as np
from travel_app.models import TravelPackage, UserActivity

def calculate_recommendations(user_id):
    # Récupérer les activités utilisateur
    activities = UserActivity.objects.filter(user_id=user_id)

    # Identifier les packages vus et leurs scores de feedback
    viewed_packages = {
        int(activity.package.id): activity.feedback_score or 0
        for activity in activities.filter(action="viewed_package")
    }

    if not viewed_packages:
        return [] 

    # Obtenir les objets des packages vus
    viewed_package_ids = list(viewed_packages.keys())
    viewed_package_objs = TravelPackage.objects.filter(id__in=viewed_package_ids)

    # Préférences utilisateur par thème
    theme_preferences = {}
    for package in viewed_package_objs:
        for theme in package.get_themes():
            theme_preferences.setdefault(theme, []).append(viewed_packages[package.id])

    # Calculer les scores moyens par thème
    average_theme_scores = {
        theme: np.mean(scores) for theme, scores in theme_preferences.items()
    }

    # Recommander des packages avec des thèmes similaires
    recommended_packages = TravelPackage.objects.filter(
        themes__overlap=list(average_theme_scores.keys())
    ).exclude(id__in=viewed_package_ids)

    # Trier les packages par pertinence et prix
    recommended_packages = sorted(
        recommended_packages,
        key=lambda p: (
            -sum(average_theme_scores.get(theme, 0) for theme in p.get_themes()),
            p.price
        )
    )[:5] 

    return recommended_packages
