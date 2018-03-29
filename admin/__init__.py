"""
Views for the admin interface

.. sectionauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""

def includeme(config):
    config.scan("admin.views")
