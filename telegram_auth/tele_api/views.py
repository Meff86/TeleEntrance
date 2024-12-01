from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import jwt
from .models import TelegramUser
import requests

def telegram_auth(request):

    if request.user.is_authenticated:

        return redirect('telegram_callback')
    return render(request, 'telegram_auth.html')

@csrf_exempt
def telegram_callback(request):
    if request.method == 'POST':
        try:
            data = request.POST
            telegram_id = data.get('id')
            telegram_username = data.get('username')

            if not telegram_id:
                return HttpResponse('Telegram ID is required', status=400)

            with transaction.atomic():
                try:
                    telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
                    user = telegram_user.user
                except TelegramUser.DoesNotExist:
                    if telegram_username:
                        username = telegram_username
                    else:
                        username = f"telegram_user_{telegram_id}"

                    user = User.objects.create_user(username=username)
                    telegram_user = TelegramUser.objects.create(
                        user=user,
                        telegram_id=telegram_id,
                        telegram_username=telegram_username
                    )

                login(request, user)
                token = jwt.encode({'telegram_id': telegram_id}, 'your-secret-key', algorithm='HS256')
                redirect_url = f'/auth/complete/telegram/?token={token}'
                return JsonResponse({'redirect_url': redirect_url})

        except Exception as e:
            return HttpResponse(f'Error: {str(e)}', status=500)

    else:
        token = request.GET.get('token')
        if token:
            try:
                data = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
                telegram_id = data.get('telegram_id')
                telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
                login(request, telegram_user.user)
                return render(request, 'telegram_callback.html')
            except jwt.ExpiredSignatureError:
                return HttpResponse('Token has expired', status=400)
            except jwt.InvalidTokenError:
                return HttpResponse('Invalid token', status=400)
            except TelegramUser.DoesNotExist:
                return HttpResponse('User not found', status=400)

    return render(request, 'telegram_callback.html')
