import numpy as np
from scipy.spatial.distance import cosine
from travel_app.models import TravelPackage, UserActivity
from decimal import Decimal
from django.db.models import Q

def calculate_similarity(vector1, vector2):
    if not any(vector1) or not any(vector2):  
        return 0.0
    return 1 - cosine(vector1, vector2)

def recommend_by_similarity(user_id, exclude_package=None):
    user_preferences = np.zeros(5)  
    # Fetch user activity
    activities = UserActivity.objects.filter(user_id=user_id, action="viewed_package")
    viewed_package_ids = [int(activity.details) for activity in activities if activity.details.isdigit()]

    # Get viewed packages and create preference vector
    viewed_packages = TravelPackage.objects.filter(id__in=viewed_package_ids)
    for package in viewed_packages:
        user_preferences += np.array(package.get_themes_vector()) 

    user_preferences /= np.linalg.norm(user_preferences) if np.linalg.norm(user_preferences) > 0 else 1

    # Calculate similarity for all packages
    all_packages = TravelPackage.objects.exclude(id__in=viewed_package_ids)
    recommendations = []
    for package in all_packages:
        similarity = calculate_similarity(user_preferences, np.array(package.get_themes_vector()))
        recommendations.append((package, similarity))

    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

    if exclude_package:
        recommendations = [rec for rec in recommendations if rec[0].id != exclude_package.id]

    return [rec[0] for rec in recommendations[:5]]
