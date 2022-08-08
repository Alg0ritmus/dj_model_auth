from django.http import HttpResponse
from django.contrib.auth.models import Group

def are_valid_group(parsed_groups):
    available_groups=[group.name for group in Group.objects.all()]
    for group in parsed_groups:
        if group not in available_groups:
            return False
    return True

def is_user_allowed(request,list_of_groups):
    user_groups= request.user.groups.all()
    # check if user has at least group
    if not user_groups:
        print("1 FLS")
        return False

    user_groups_list = [x for x in user_groups]
    # check if user group has permission
    for group in user_groups_list:
        if group.name not in list_of_groups:
            return False
    return True


def allowedFor(groups):
    def wrapper_func(view_func):
        def func_to_return(request, *args, **kwargs):
            print(request.user.groups.all())
            
            # check if parsed groups are valid
            assert(are_valid_group(groups),"Parsed groups are not valid - alloedFor decorator")

            #check if user is allowed
            if is_user_allowed(request,groups):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("not allowed to view page (dec)!")
        return func_to_return
    return wrapper_func