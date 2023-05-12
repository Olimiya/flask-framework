# 专门的测试代码
from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from functools import wraps

app = Flask(__name__)
# replace with your own secret key
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


# 测试装饰器合并


def log(msg):
    def decorator(f):
        def wrapper(*args, **kwargs):
            print(msg)
            return f(*args, **kwargs)
        return wrapper
    return decorator


def repeat(n):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for i in range(n):
                f(*args, **kwargs)
        return wrapper
    return decorator


@log("test")
@repeat(4)
def greet(name):
    print(f'Hello, {name}!')


print("greet: ", greet.__name__)
greet('world')


def composed(*decs):
    @wraps(f)
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco


@composed(log("test"), repeat(4))
def greet1(name):
    print(f'Hello, {name}!')


print("greet1: ", greet1.__name__)
greet1('world')
# greet1('world')


def composed_with_args(msg, n):
    deco2 = repeat(n)
    deco1 = log(msg)

    def deco(f):
        return deco1(deco2(f))
    return deco


@composed_with_args("test", 4)
def greet2(name):
    print(f'Hello, {name}!')


print("greet2: ", greet2.__name__)
greet2('world')
