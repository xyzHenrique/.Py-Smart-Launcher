
i = ["x", "y"]
def foo(x=list(["x", "y"])) -> str:
    print(x)

foo("z")