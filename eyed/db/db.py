#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

#
# SQLAlchemy
#
from sqlalchemy import engine_from_config, pool
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
import pkg_resources

#
# スクリプトを実行するディレクトリ設定
#
base_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.abspath(os.path.join(base_path, '../'))
os.chdir(base_path)

#
# SQL エンジンの取得
#
config = Config(pkg_resources.resource_filename('eyed', 'alembic.ini'))
Engine = engine_from_config(
	config.get_section(config.config_ini_section),
	prefix = 'sqlalchemy.',
	poolclass = pool.NullPool
)

#
# SQL接続用セッションオブジェクト化
#
Session = sessionmaker(bind = Engine)

#
# セッションの取得
#
def createSession():
	return Session()

#
# Entry Point
#
if __name__ == "__main__":
	session = Session() 
	print session

