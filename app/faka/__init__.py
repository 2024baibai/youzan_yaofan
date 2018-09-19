# -*- coding=utf-8 -*-
from flask import Blueprint

faka = Blueprint('faka', __name__)

from . import views
