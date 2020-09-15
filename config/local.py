def show_toolbar(request):
    if request.is_ajax():
        return False
    return True