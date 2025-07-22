import operator
from typing import Any, Iterable, Sequence

import pytest
from pydantic import BaseModel

from src.db.managers.manager import DBManager
from src.db.models import Base


def parametrize_with_dict(argnames: list[str], cases: Iterable[dict[str, Any]]):
    def decorator(func):
        return pytest.mark.parametrize(
            argnames,
            [
                pytest.param(*[case[arg_name] for arg_name in argnames], id=str(case.get('case_id') or idx))
                for idx, case in enumerate(cases)
            ],
        )(func)

    return decorator


def compare_model_with_attrs(model: Base | None, expected_attrs: dict[str, Any]) -> None:
    if not expected_attrs:
        assert model is None
    else:
        for attr, value in expected_attrs.items():
            if isinstance(value, BaseModel):
                compare_model_with_attrs(getattr(model, attr), value.dict())
            assert (getattr(model, attr)) == (value), f'{attr=}, {getattr(model, attr)=}, {value=}'


def compare_models_with_attrs(models: Sequence[Base], expected_models_attrs: list[dict[str, Any]]) -> None:
    assert len(models) == len(expected_models_attrs)
    for model, expected_attrs in zip(models, expected_models_attrs):
        compare_model_with_attrs(model, expected_attrs)


def compare_not_ordered_lists(s, t):
    t = list(t)
    try:
        for elem in s:
            t.remove(elem)
    except ValueError:
        return False
    return not t


class _ANY_NOT_NONE(object):
    'A helper object that compares equal to everything not None.'

    def __eq__(self, other):
        return other is not None

    def __ne__(self, other):
        return other is not None

    def __repr__(self):
        return '<ANY_NOT_NONE>'


ANY_NOT_NONE = _ANY_NOT_NONE()


# функции ниже я украл отсюда
# https://stackoverflow.com/questions/27265939/comparing-python-dictionaries-and-nested-dictionaries
# их можно использовать для того чтобы найти дифф между огромными вложенными словариками с ANY

def do_compare(data1, data2, data1_name='left', data2_name='right', path=''):
    if operator.eq(data1, data2) and not path:
        print('Both data have same content')
    else:
        if isinstance(data1, dict) and isinstance(data2, dict):
            compare_dict(data1, data2, data1_name, data2_name, path)
        elif isinstance(data1, list) and isinstance(data2, list):
            compare_list(data1, data2, data1_name, data2_name, path)
        else:
            if data1 != data2:
                value_err = 'Value of %s%s (%s) not same as %s%s (%s)\n' \
                            % (data1_name, path, data1, data2_name, path, data2)
                print(value_err)
        # findDiff(data1, data2)


def compare_dict(data1, data2, data1_name, data2_name, path):
    old_path = path
    for k in data1.keys():
        path = old_path + '[%s]' % k
        if k not in data2:
            key_err = 'Key %s%s not in %s\n' % (data1_name, path, data2_name)
            print(key_err)
        else:
            do_compare(data1[k], data2[k], data1_name, data2_name, path)
    for k in data2.keys():
        path = old_path + '[%s]' % k
        if k not in data1:
            key_err = 'Key %s%s not in %s\n' % (data2_name, path, data1_name)
            print(key_err)


def compare_list(data1, data2, data1_name, data2_name, path):
    data1_length = len(data1)
    data2_length = len(data2)
    old_path = path
    if data1_length != data2_length:
        value_err = 'No: of items in %s%s (%s) not same as %s%s (%s)\n' \
                    % (data1_name, path, data1_length, data2_name, path, data2_length)
        print(value_err)
    for index, item in enumerate(data1):
        path = old_path + '[%s]' % index
        try:
            do_compare(data1[index], data2[index], data1_name, data2_name, path)
        except IndexError:
            pass


async def add_all(db_manager: DBManager, *models):
    async with db_manager.session() as session:
        for m in models:
            session.add(m)
            await session.flush()
