"""
Views and scripts the visualization of our argumentation graph

.. sectionauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
"""


def includeme(config):
    config.scan('graph.views')
