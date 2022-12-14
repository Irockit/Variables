from inkex.elements import TextElement, FlowPara, FlowDiv, Tspan, BaseElement

def is_text(node: BaseElement) -> bool: return isinstance(node, (TextElement, FlowPara, FlowDiv))
def is_tspan(node: BaseElement) -> bool: return isinstance(node, Tspan)
def remove_tspans(node: TextElement|FlowPara|FlowDiv) -> None: [ remove_tspan(child) for child in node]
def remove_tspan(node: BaseElement):
    if not is_tspan(node): return
    node.text = None

class Target:
    @staticmethod
    def get(node) -> str: return node.attrib["target"]
    def be(node) -> bool: return node.attrib.has_key('target')

