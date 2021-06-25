from users.models import ManagerUser


def get_manager_lackeys(manager):
    return [lackey.lackey for lackey in ManagerUser.objects.filter(manager=manager)]


def get_hitman_choices(user):
    hitman_list = [(str(hitman.pk), hitman) for hitman in get_manager_lackeys(user) if hitman.is_active]
    # Insert default option at initial position
    hitman_list.insert(0, ('', '----------'))
    return sorted(hitman_list)
