from pyblocks.blocks.definition import block

@block(label="Create Instance: {var_name} = {class_name}({args})",
       category="Classes",
       color="#cba6f7",
       description="Create an instance of a class")
def create_instance(var_name: str, class_name: str, args: str) -> str:
    args = args.strip()
    return f"{var_name} = {class_name}({args})"

@block(label="Call Method: {var_name}.{method_name}({args})",
       category="Classes",
       color="#cba6f7",
       description="Call a method on an object")
def call_method(var_name: str, method_name: str, args: str) -> str:
    args = args.strip()
    return f"{var_name}.{method_name}({args})"
