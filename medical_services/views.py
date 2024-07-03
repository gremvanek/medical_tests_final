# medical_services/views.py
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'main/index.html'


# def contact_form(request):
#     if request.method == 'POST':
#         name = request.POST.get('name', '')
#         email = request.POST.get('email', '')
#         subject = request.POST.get('subject', '')
#         message = request.POST.get('message', '')
#
#         # Отправка электронной почты
#         send_mail(
#             subject,
#             f'From: {name} <{email}>\n\n{message}',
#             email,  # Используем email отправителя
#             ['gremvanek@gmail.com'],  # Замените на адрес получателя
#             fail_silently=False,
#         )
#
#         # Возвращаем сообщение об успешной отправке в формате JSON
#         return JsonResponse({'message': 'Сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время!'})
#
#     # Если запрос не POST, возвращаем пустой ответ с кодом 400
#     return JsonResponse({'error': 'Bad Request'}, status=400)

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
            ['gremvanek@gmail.com'],  # Замените на адрес получателя
            fail_silently=False,
        )

        # Возвращаем сообщение об успешной отправке
        success_message = 'Сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время!'
        return HttpResponse(success_message)

    # Если запрос не POST, возвращаем пустой ответ с кодом 400
    return HttpResponse('Bad Request', status=400)
