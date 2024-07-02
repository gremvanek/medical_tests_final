# user.models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

# Словарь для указания полей, допускающих null значения
NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    """
    Пользовательская модель пользователя, расширяющая AbstractUser Django.

    Поля:
    - email: EmailField (уникальный)
    - username: CharField (макс. длина 150, уникальный)
    - phone: CharField (макс. длина 35, допускает null)
    - avatar: ImageField (загружается в 'users/', допускает null)
    - country: CharField (макс. длина 35, допускает null)
    - is_verified: BooleanField (по умолчанию False)
    - token: CharField (макс. длина 100, допускает null)
    - have_permissions: BooleanField (по умолчанию False)
    - is_blocked: BooleanField (по умолчанию False)

    Настройки:
    - USERNAME_FIELD: Использует 'email' в качестве уникального идентификатора вместо 'username'.
    - REQUIRED_FIELDS: Для создания пользователя требуется только email и пароль.

    Методы:
    - has_group(group_name): Проверяет, принадлежит ли пользователь к определенной группе по названию.
    """

    class Meta:
        verbose_name = "Пользователь"  # Отображаемое имя в единственном числе
        verbose_name_plural = "Пользователи"  # Отображаемое имя во множественном числе
        permissions = [
            (
                "set_is_active",
                "Активация пользователя",
            ),  # Разрешение на активацию пользователей
            (
                "block_user",
                "Может блокировать пользователей",
            ),  # Разрешение на блокировку пользователей
        ]

    email = models.EmailField(unique=True, verbose_name="Почта")
    username = models.CharField(
        max_length=150, unique=True, verbose_name="Имя пользователя"
    )

    phone = models.CharField(max_length=35, verbose_name="Номер телефона", **NULLABLE)
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", **NULLABLE)
    country = models.CharField(max_length=35, verbose_name="Страна", **NULLABLE)

    is_verified = models.BooleanField(default=False, verbose_name="Верификация")
    token = models.CharField(max_length=100, verbose_name="Токен", **NULLABLE)

    have_permissions = models.BooleanField(default=False, verbose_name="Права доступа")
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def has_group(self, group_name):
        """
        Проверяет, принадлежит ли пользователь к определенной группе.

        Аргументы:
        - group_name (str): Название группы для проверки.

        Возвращает:
        - bool: True, если пользователь принадлежит к группе, False в противном случае.
        """
        return self.groups.filter(name=group_name).exists()
