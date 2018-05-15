#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nose.tools import ok_, eq_

# テストケース
# test で始まる名前の関数で書けばOK
def test_1_is_true():
	ok_(bool(1))

def test_1_plus_2():
	eq_(1 + 2, 3)

if __name__ == '__main__':
	pass

