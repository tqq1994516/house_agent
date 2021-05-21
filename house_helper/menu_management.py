from house_helper.models import Menus


def get_menu_list(fun_name):
    '''
    根据调用view方法名查询对应菜单信息
    :param fun_name: 调用此方法的方法名称
    :return: 菜单子点击及当前选中菜单id
    '''
    menu_list = Menus.objects.all()
    menu_dict = menu_list.values()
    get_menu_id = menu_list.filter(en_name=fun_name).values().first()
    # print(get_menu_id)
    model_num, menu_checked_id, child_menu_checked_id, least_menu_checked_id = get_checked_menu_id(get_menu_id, menu_list)
    menu_dict.model_num = model_num
    menu_dict.menu_checked_id = menu_checked_id
    menu_dict.child_menu_checked_id = child_menu_checked_id
    menu_dict.least_menu_checked_id = least_menu_checked_id
    return menu_dict


def get_checked_menu_id(menu_id, menu_list):
    '''
    根据加载菜单编号，设置菜单及父级选中状态
    :param menu_id: 加载菜单id
    :param menu_list: 菜单querySet
    :return: 需要设置选中状态的菜单id
    '''
    model_num, menu_checked_id, child_menu_checked_id, least_menu_checked_id = 0, 0, 0, 0
    if menu_id['hierarchy'] > 1:
        parent_menu_id = menu_list.filter(id=menu_id['parent_id']).values().first()
        if parent_menu_id['hierarchy'] > 1:
            parent_menu_superior_id = menu_list.filter(id=parent_menu_id['parent_id']).values().first()
            if parent_menu_superior_id['hierarchy'] > 1:
                parent_menu_best_id = menu_list.filter(id=parent_menu_superior_id['parent_id']).values().first()
                model_num = parent_menu_best_id['id']
                menu_checked_id = parent_menu_superior_id['id']
                child_menu_checked_id = parent_menu_id['id']
                least_menu_checked_id = menu_id['id']
            else:
                model_num = parent_menu_superior_id['id']
                menu_checked_id = parent_menu_id['id']
                child_menu_checked_id = menu_id['id']
        else:
            model_num = parent_menu_id['id']
            menu_checked_id = menu_id['id']
    else:
        model_num = menu_id['id']
    return model_num, menu_checked_id, child_menu_checked_id, least_menu_checked_id
