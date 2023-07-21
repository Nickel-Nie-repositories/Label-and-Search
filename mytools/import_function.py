"""
这个方案实现“动态导入函数”不成功，
当这个函数定义在main文件，并在main文件中调用时，运行良好，
但是一旦放到其他文件再调用，就会报错：
ModuleNotFoundError: No module named 'mytools.infer'
把这个函数定义在main文件，然后把这个函数传进别的类里再调用也会报错。
原因暂时未知；
猜测为，paddleOCR中的import时使用了一些环境或者路径相关的参数，而我们在局部空间下的exec中调用import时缺少了这些参数。
"""

"""
搞了半天是我把自己的文件夹也命名成tools的问题，改成mytools就没问题了。。。
"""


def import_function(source_path):
    import ast

    # 首先我们读取整个py文件，把源码当成字符串取出来：
    with open(source_path, 'r', encoding="UTF-8") as fin:
        source = fin.read()
    # 然后，我们解析这个字符串，生成语法树：
    tree = ast.parse(source, mode='exec')

    # 对于这个语法树，遍历它，我们希望把所有满足条件的函数名找出来：
    # 要按自身需求遍历语法树，就要定义一个继承 ast.NodeVisitor 的类，重写其中的方法
    class FuncFinder(ast.NodeVisitor):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.function_names = []

        def visit_FunctionDef(self, node):
            # 如果这个函数定义的节点，函数满足 str -> str 则将函数名加入列表。
            # print(ast.dump(node))
            # 首先要求只有一个参数，然后要求那个参数具有annotation：str
            if len(node.args.args) == 1:
                if type(node.args.args[0].annotation) == ast.Name and node.args.args[0].annotation.id == "str":
                    if isinstance(node.returns, ast.Name) and node.returns.id == "str":
                        print(node.name)
                        self.function_names.append(node.name)
            self.generic_visit(node)

    # 这个类的运行规则如下：
    # 当调用这个类的实例的visit方法时，输入一个树（即树的根节点）
    # 它会根据这个节点的类型（一般根节点都是module节点）调用不同的 visit_XXX() 方法，如果找不到，它会直接调用 generic_visit 方法
    # 在不同的visit_XXX()方法中，它会针对性的进行一些处理（原始的父类是空处理），然后调用 generic_visit 方法
    # 在 generic_visit 方法里，它也可以进行一些处理（原始为空），然后它会递归地对该节点的子节点进行上述同样的处理。
    # （因此，你可以重写generic_visit方法进行一些通用处理，但是记得调用父类的generic_visit以完成递归）

    # 遍历这个语法树：
    finder = FuncFinder()
    finder.visit(tree)
    print(finder.function_names)

    # 编译这个语法树：
    code = compile(tree, filename='blah', mode='exec')
    namespace = {}
    exec(code, namespace)

    # 从namespace里获取其中的方法：
    # F = namespace[finder.function_names[0]]
    functions = [namespace[name] for name in finder.function_names]

    return finder.function_names, functions


