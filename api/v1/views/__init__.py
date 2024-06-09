#!/usr/bin/python3
"""
    Create and configure the Flask Blueprint for the API
"""
from flask import Blueprint

# Initialize the Blueprint for the API views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import all the views if the Blueprint is initialized
if app_views:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.amenities import *
    from api.v1.views.users import *
    from api.v1.views.places import *
    from api.v1.views.places_reviews import *
    from api.v1.views.places_amenities import *
