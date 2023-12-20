from datetime import datetime


def post_media_directory_path(instance, filename) -> str:
    """
     Приложение perevalinfo, Модель PerevalImages. Формирование пути для атрибута upload_to=
    """
    date = datetime.now()
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"perevalinfo/{instance.pk}/{date.year}/{date.month}/{date.day}/{filename}"

