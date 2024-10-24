from django.shortcuts import render
from django.http import HttpResponse
from groq import Groq

# this should be an env variable but whatever
GROQ_KEY = "keyhere"
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
    else:
        return HttpResponse("")
def summarizeComments(request):
    if request.method == 'GET' and request.GET.get('review1') and request.GET.get('reviewRandom'):

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Briefly summarize what people think about the restaurant based on the following reviews. One says: " + request.GET.get('review1') + ". Another review said: " + request.GET.get('reviewRandom') + ". Write as if you were providing unbiased advice to someone considering the restaurant. Output should be 1-2 very short incomplete but highly informational sentences without adjectives or listing anything (avoid commas). Do not prefix with anything, only output the response."
                }
            ],
            model="llama3-8b-8192",
        )
        return HttpResponse(chat_completion.choices[0].message.content)
    else: return HttpResponse("")
def generateCuisineType(request):
    if request.method == 'GET' and request.GET.get('restaurantName') and request.GET.get('restaurantType'):

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Give a one to two word cuisine type for the restaurant " + request.GET.get('restaurantName') + ", a " + request.GET.get('restaurantType') + " in Atlanta, Georgia. The possible cuisine types include 'Fast Food', 'American', 'Chinese', 'Italian', 'Vietnamese', 'Mexican', 'Indian', 'Japanese', 'Korean', 'Thai', 'Mediterranean',and 'Snacks'. Do not prefix with anything, only output the response."
                }
            ],
            model="llama3-8b-8192",
        )
        return HttpResponse(chat_completion.choices[0].message.content)
    else:
        return HttpResponse("")