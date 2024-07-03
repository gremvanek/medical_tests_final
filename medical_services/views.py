# medical_services/views.py
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST

from config import settings


class HomePageView(TemplateView):
    template_name = 'main/index.html'


@require_POST
def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        # Отправка электронной почты
        send_mail(
            subject,
            f'From: {name} <{email}>\n\n{message}',
            email,  # Используем email отправителя
            [settings.EMAIL_HOST_USER],  # Замените на адрес получателя
            fail_silently=False,
        )

    #     # Возвращаем JSON ответ
    #     return JsonResponse({'message': 'Сообщение успешно отправлено!'})
    # else:
    #     return JsonResponse({'error': 'Метод не поддерживается'}, status=405)
