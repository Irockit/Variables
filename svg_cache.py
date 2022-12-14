from inkex.elements import load_svg
import copy

def _load_svg(file_name) :
        with open(file_name, "rb") as f:
            document = load_svg(f)
            layer = document.getroot().get_current_layer()
            return layer[0]


class SvgCache:
    data:dict[str, any] = {}
    absolute: bool = True
    relative_function = None

    @classmethod
    def add(cls, path, debug): 
        if path not in cls.data:
            new_path = path if cls.absolute else cls.relative_function(path)
            debug(cls.relative_function(path))
            value = _load_svg(new_path)
            cls.data[path] = value
    
    @classmethod
    def get(cls, path:str): return cls.data[path]

    @classmethod
    def set_relative(cls): cls.absolute = False 
    @classmethod
    def set_relative_function(cls, function): cls.relative_function = function