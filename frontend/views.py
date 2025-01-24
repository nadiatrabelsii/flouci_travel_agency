from django.shortcuts import render, get_object_or_404, redirect
from travel_app.models import TravelPackage, UserActivity, TravelNews
from frontend.tasks import send_booking_email 
from travel_app.utils import recommend_by_similarity
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from travel_app.tasks import OpenAIChatbot 

def homepage(request):
    user_id = request.session.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        request.session['user_id'] = user_id

    UserActivity.objects.create(user_id=user_id, action="opened_homepage", details="User visited homepage.")

    packages = TravelPackage.objects.all()
    recommendations = recommend_by_similarity(user_id)

    return render(request, 'frontend/homepage.html', {
        'packages': packages,
        'recommendations': recommendations,
    })

def booking_success(request):
    user_id = request.session.get('user_id')
    package_id = request.GET.get('package_id')  
    package = get_object_or_404(TravelPackage, id=package_id)
    recommendations = recommend_by_similarity(user_id, exclude_package=package)

    return render(request, 'frontend/booking_success.html', {
        'package': package,
        'recommendations': recommendations,
    })


def package_detail(request, package_id):

    # Get the travel package by ID or return 404
    package = get_object_or_404(TravelPackage, id=package_id)
    return render(request, 'frontend/package_detail.html', {'package': package})

def submit_feedback(request, package_id):
    if request.method == 'POST':
        feedback = float(request.POST.get('feedback'))
        user_id = request.session.get('user_id')

        # Log feedback in UserActivity
        UserActivity.objects.create(
            user_id=user_id,
            action="viewed_package",
            details=str(package_id),
            feedback_score=feedback
        )

    return redirect('package_detail', package_id=package_id)


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

def news_page(request):
    news_list = TravelNews.objects.order_by('-created_at')
    return render(request, 'frontend/news.html', {'news_list': news_list})

chatbot_instance = OpenAIChatbot()

def chatbot_page(request):
    return render(request, 'frontend/chatbot.html')

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message', '')

            # Use the chatbot instance to get a response
            reply = chatbot_instance.get_response(user_input)
            return JsonResponse({'reply': reply})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
