def get_modifier_of_type(obj, mod_type : str):
    for mod in obj.modifiers:
        if mod.type == mod_type:
            return mod
    return None

def remove_modifier_of_type(obj, mod_type : str):
    for mod in obj.modifiers:
        if mod.type == mod_type:
            obj.modifiers.remove(mod)

def get_or_create_modifier(obj, mod_name, mod_type : str):

    mod = get_modifier_of_type(obj, mod_type)

    if not mod:
        mod = obj.modifiers.new(type=mod_type, name=mod_name)
    
    return mod
    
    