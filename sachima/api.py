import inspect
import functools
import importlib
# import sanic
# from sachima.services import server
import numpy as np
import pandas as pd
import json
from nameko.rpc import rpc, RpcProxy
################################


def get_data(r):
    if r == 'r0001':
        data = pd.DataFrame({
            '0': 1.,
            'test1': '20181228',
            'test2': '这是一段测试文字测试字段的长度是否能自动调整',
        })
    else:
        data = pd.DataFrame({
            '0': 1.,
            '字段A': '20181228',
            '字段B': '这是一段测试文字测试字段的长度是否能自动调整',
            '字段C': pd.Series(1, index=list(range(4)), dtype='float32'),
            '字段D': np.array([3] * 4, dtype='int32'),
            '字段E': pd.Categorical(["test", "train", "test", "train"]),
            '字段F': '这是一段测试文字测试字段的长度是否能自动调整',
            '字段G': '这是一段测试文字测试字段的长度是否能自动调整这是一段测试' +
            '文字测试字段的长度是否能自动调整这是一段测试文字测试字段的长度是否能自动调整'
        })

    return json.dumps({
        'itemDatePicker': {
            'id': '日期',
            'type': 'DatePicker',  # RangePicker
        },
        'itemSelect': [
            {
                'id': '测试1',
                'props': {
                    'mode': 'tags',
                    'allowClear': True,
                    'placeholder': '待输入',
                },
                'option': ['111', 'javascript', 'flutter']
            }, {
                'id': 'Test2',
                'props': {
                    # 'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': [1, 2, 3]
            }, {
                'id': '测试5',
                'props': {
                    'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': ['a', 'b', 'c']
            }, {
                'id': '测试4',
                'props': {
                    'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': [1]
            }, {
                'id': '测试6',
                'props': {
                    'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': []
            },
        ],
        # 'index': data.index.to_frame(),
        'columns': data.columns.tolist(),
        'dataSource': data.to_dict('records')
    })


def api(type='grpc', platform='superset'):
    def wrapper(func):
        @functools.wraps(func)
        def api_called(*_args, **kw):
            # before
            _result = func(*_args, **kw)
            # print(_result)  # None
            name = 'r00001'
            publish(type, platform, func, name)
            # 调用supersetpost注册接口

            # after
            return _result
        return api_called
    return wrapper


class Data(object):
    name = 'data'

    @rpc
    def get_report(self, params):
        print(params)
        m = importlib.import_module(params['name'])
        res = m.main()
        print(type(res))
        return test(res)


def test(data):
    print(type(data[0]))
    return json.dumps({
        'itemDatePicker': {
            'id': '日期',
            'type': 'DatePicker',  # RangePicker
        },
        'itemSelect': [
            {
                'id': '测试1',
                'props': {
                    'mode': 'tags',
                    'allowClear': True,
                    'placeholder': '待输入',
                },
                'option': ['111', 'javascript', 'flutter']
            }, {
                'id': 'Test2',
                'props': {
                    # 'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': [1, 2, 3]
            }, {
                'id': '测试5',
                'props': {
                    'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': ['a', 'b', 'c']
            }, {
                'id': '测试4',
                'props': {
                    'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': [1]
            }, {
                'id': '测试6',
                'props': {
                    'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': []
            },
        ],
        # 'index': data.index.to_frame(),
        'columns': data[0].drop(['打款日期','进件时间'], axis=1).columns.tolist(),
        'dataSource': data[0].drop(['打款日期','进件时间'], axis=1).to_dict('records')
    })

def publish(t, p, f, n):
    '''
        class {}(object):
        name = n

        @rpc
        def get(self):
            return f()
    '''

    print('publishing to ' + p + ' using ' + t)
    return 'success'
