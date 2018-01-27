#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# SQLAlchemy
#
from sqlalchemy import engine_from_config, pool
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
import pkg_resources

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
# セッションの取得
#
Session = sessionmaker(bind = Engine)

#
# Entry Point
#
if __name__ == "__main__":
	session = Session() 
	print session
