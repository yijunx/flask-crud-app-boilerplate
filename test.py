from functools import wraps


def decoratorarg(arg1,arg2):
    print("inside decoratorarg arg1={} arg2={}".format(arg1,arg2))
    def decorator(func):
        print("inside decorator arg1 ={} arg2 ={}".format(arg1,arg2))
        def wrapper(*args,**kwargs):
            msg = kwargs['msg']
            print(f"msg is {msg}")
            print("inside wrapper arg1={} arg2={}".format(arg1,arg2))
            func(*args,**kwargs)
        print("returning wrapper")
        return wrapper
    print("returning decorator")
    return decorator

@decoratorarg(1,2)
def func(msg):
    print("inside function")

print("\ncalling func")
func(msg="aaa")

        