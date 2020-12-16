from foxilang.models import *


def update_user_level(user_id, level, current_experience, border_experience):
    User_Level.objects.filter(user=user_id).update(level=level,
                                                   current_experience=current_experience,
                                                   border_experience=border_experience)
