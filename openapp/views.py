from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
# Create your views here.
from dotenv import load_dotenv
import os
import openai
from .assistant import QAAssistant
from .models import ChatGptBot
load_dotenv()
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt



openai.api_key = os.getenv("OPENAI_API_KEY")
qa_assistant = QAAssistant()

def index(request):
    #check if user is authenticated
    if request.user.is_authenticated:
        if request.method == 'POST':
            #get user input from the form
            user_input = request.POST.get('userInput')
            #clean input from any white spaces
            clean_user_input = str(user_input).strip()
            #send request with user's prompt
            response = openai.Completion.create(
                model="text-davinci-003",
                    prompt=clean_user_input,
                    temperature=0,
                    max_tokens=1000,
                    top_p=1,
                    frequency_penalty=0.5,
                    presence_penalty=0
                    )
            #get response
            bot_response = response['choices'][0]['text']
            
            obj, created = ChatGptBot.objects.get_or_create(
                user=request.user,
                messageInput=clean_user_input,
                bot_response=bot_response.strip(),
            )
            return redirect(request.META['HTTP_REFERER'])
        else:
            #retrieve all messages belong to logged in user
            get_history = ChatGptBot.objects.filter(user=request.user)
            context = {'get_history':get_history}
            return render(request, 'index.html', context)
    else:
        return redirect("login")


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "users/register.html"
    def form_valid(self, form):
        response = super().form_valid(form)
        # Get the user's username and password in order to automatically authenticate user after registration
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        # Authenticate the user and log him/her in
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response
    def get_success_url(self):
        return reverse("main")


@login_required
def DeleteHistory(request):
    chatGptobjs = ChatGptBot.objects.filter(user = request.user)
    chatGptobjs.delete()
    return redirect(request.META['HTTP_REFERER'])


def get_history(request):
    user = request.user
    if user.is_authenticated:
        history = ChatGptBot.objects.filter(user=user).values()
        context = {'get_history': list(history)}


        return JsonResponse(context)

def convert_messages(messages):
    messages_list = []

    for message in messages:
        messages_list.append({"role": "user", "content":message['messageInput']})
        messages_list.append({"role": "assistant", "content": message['bot_response']})

    return messages_list

def get_bot_response(user, message):
    history = ChatGptBot.objects.filter(user=user).values()
    messages = convert_messages(history)
    messages.append({"role": "user", "content": message})

    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
    )

    chat_message = response.choices[0].message.content
    print("Bot: ", chat_message)

    return chat_message

@csrf_exempt
def send_message(request):

    user = request.user

    if user.is_authenticated:
        if request.method == "POST":
            user_input = request.POST['user_input']

            #clean input from any white spaces
            clean_user_input = str(user_input).strip()
            #send request with user's prompt
            """response = openai.Completion.create(
                model="text-davinci-003",
                    prompt=clean_user_input,
                    temperature=0,
                    max_tokens=1000,
                    top_p=1,
                    frequency_penalty=0.5,
                    presence_penalty=0
                    )
            
            #get response
            bot_response = response['choices'][0]['text']
            """

            assistant_response = qa_assistant.run_assistant(clean_user_input)
            #bot_response = get_bot_response(user, clean_user_input)
            obj, created = ChatGptBot.objects.get_or_create(
                user=request.user,
                messageInput=clean_user_input,
                bot_response=assistant_response,
            )

            return JsonResponse({"bot_response": assistant_response})