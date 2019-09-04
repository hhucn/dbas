"""
Views for the admin interface
"""


def includeme(config):
    config.scan("admin.views")
