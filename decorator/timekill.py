import timeit

def clock(func):
    def clocked(*args):
        # 1、执行方法前的时间
        t0 = timeit.default_timer()
        # 2、执行被注释的制定方法
        result = func(*args)
        # 3、获得执行方法的时间
        elapsed = timeit.default_timer() - t0

        # 获得方法名
        name = func.__name__
        # 拼接参数
        arg_str = ', '.join(repr(arg) for arg in args)
        print('%s() method had cost  %0.8fs' % ( name,elapsed))
        return result

    return clocked
