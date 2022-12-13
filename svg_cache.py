from inkex.elements import load_svg
import copy

def _load_svg(file_name) :
        with open(file_name, "rb") as f:
            document = load_svg(f)
            layer = document.getroot().get_current_layer()
            return layer[0]


class SvgCache:
    data:dict[str, any] = {}
    @staticmethod
    def add(path): 
        if path not in SvgCache.data:
            value = _load_svg(path)
            SvgCache.data[path] = value
    
    @staticmethod
    def get(path:str): return SvgCache.data[path]