def get_modifier_of_type(obj, mod_type : str):
    if obj:
        for mod in obj.modifiers:
            if mod.type == mod_type:
                return mod
    return None

def has_modifiers(obj, modifier_types : list) -> bool:
    if not obj:
        return False

    for mod_type in modifier_types:
        if not get_modifier_of_type(obj, mod_type):
            return False

    return True   


def remove_modifier_of_type(obj, mod_type : str):
    if obj:
        for mod in obj.modifiers:
            if mod.type == mod_type:
                obj.modifiers.remove(mod)

def get_or_create_modifier(obj, mod_name, mod_type : str):

    mod = get_modifier_of_type(obj, mod_type)

    if not mod:
        mod = obj.modifiers.new(type=mod_type, name=mod_name)
    
    return mod
    
    