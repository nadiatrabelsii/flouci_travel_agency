from django.shortcuts import render, get_object_or_404, redirect
from travel_app.models import TravelPackage, UserActivity, TravelNews
from frontend.tasks import send_booking_email  
from .recommendations import calculate_recommendations, calculate_recommendations
from django.http import JsonResponse

def homepage(request):
    user_id = request.session.get('user_id')
    if not user_id:
        import uuid
        user_id = str(uuid.uuid4())
        request.session['user_id'] = user_id

    UserActivity.objects.create(
        user_id=user_id,
        action="opened_homepage",
        details="User visited homepage."
    )

    packages = TravelPackage.objects.all()
    recommendations = calculate_recommendations(user_id)

    return render(request, 'frontend/homepage.html', {
        'packages': packages,
        'recommendations': recommendations,
    })


def api_recommendations(request, user_id):
    recommendations = calculate_recommendations(user_id)
    return JsonResponse({
        'recommendations': [
            {
                'id': pkg.id,
                'name': pkg.name,
                'description': pkg.description,
                'price': float(pkg.price),
                'themes': pkg.get_themes(),
            }
            for pkg in recommendations
        ]
    })


def package_detail(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)
    user_id = request.session.get('user_id')

    UserActivity.objects.create(
        user_id=user_id,
        action="viewed_package",
        details=str(package_id)
    )

    recommendations = calculate_recommendations(user_id)

    return render(request, 'frontend/package_detail.html', {
        'package': package,
        'recommendations': recommendations,
    })

def book_package(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)

    if request.method == 'POST':
        email = request.POST.get('email')  

        if not email:  
            return render(request, 'frontend/book_package.html', {
                'package': package,
                'error': 'Please provide a valid email address.',
            })

        send_booking_email.delay(email, package.name, package.price)

        return render(request, 'frontend/booking_success.html', {
            'package': package,
            'email': email,
        })

    return render(request, 'frontend/book_package.html', {'package': package})

def submit_feedback(request, package_id):
    if request.method == 'POST':
        feedback = float(request.POST.get('feedback'))
        user_id = request.session.get('user_id')

        # Log feedback
        UserActivity.objects.create(
            user_id=user_id,
            action="viewed_package",
            details=str(package_id),
            feedback_score=feedback
        )

        recommendations = calculate_recommendations(user_id)

    return redirect('package_detail', package_id=package_id)

def booking_success(request):
    return render(request, 'frontend/booking_success.html')


def news_page(request):
    news = TravelNews.objects.order_by("-published_date")[:20]  
    return render(request, "frontend/news.html", {"news": news})
