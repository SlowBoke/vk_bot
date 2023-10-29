# -*- coding: utf-8 -*-

import peewee
from playhouse.sqlite_ext import JSONField

database_proxy = peewee.Proxy()


class BaseModel(peewee.Model):

    class Meta:
        database = database_proxy


class UserState(BaseModel):
    """User's state inside a scenario."""
    user_id = peewee.IntegerField(unique=True)
    scenario_name = peewee.CharField()
    step_name = peewee.CharField()
    context = JSONField()


class Registration(BaseModel):
    """Gained data used for registration"""
    name = peewee.CharField()
    email = peewee.CharField()

