from django.shortcuts import render
from django.http import HttpResponse
from groq import Groq

# this should be an env variable but whatever
GROQ_KEY = "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"
client = Groq(
    api_key=GROQ_KEY,
)

def home(request):
    return render(request, 'FoodReview2340/homepage.html')
def map(request):
    return render(request, 'FoodReview2340/mapTest.html')
def generateDescription(request):
    if request.method == 'GET' and request.GET.get('restaurantName') and request.GET.get('restaurantType'):

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Create a one line very brief description for the restaurant " + request.GET.get('restaurantName') + ", a " + request.GET.get('restaurantType') + " in Atlanta, Georgia. Examples include 'Mellow sandwich shop for toasted subs', 'Spicy chicken & comfort sides joint' and 'Counter-serve eatery with Creole fare'. Do not prefix with anything, only output the response."
                }
            ],
            model="llama3-8b-8192",
        )
    return HttpResponse(chat_completion.choices[0].message.content)