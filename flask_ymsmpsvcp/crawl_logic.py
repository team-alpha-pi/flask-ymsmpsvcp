import re
import treelib
from treelib import Tree
import contextlib
from collections import namedtuple
from typing import OrderedDict
from copy import deepcopy
from .node_data import Branch, Leaf


Route = namedtuple('Route', ['path', 'options'])

path_pattern = re.compile(r'\/\w+')


class Routes:

    def __init__(self, rules: list, settings_info: dict, hidden: set = set()):

        # Sort routes by path order
        routes = sorted((Route(path=r.rule, options=deepcopy(r.methods)) for r in rules), 
                         key=lambda x: x.path)

        # Combine the route options
        # Map from route to
        self.routes = OrderedDict()

        for route in routes:
            # Remove irrelevant routes (irrelevant for the protocol)
            for option in ('HEAD', 'OPTIONS'):
                with contextlib.suppress(KeyError):
                    route.options.remove(option)

            if route.path not in self.routes:
                self.routes[route.path] = route.options
            else:
                self.routes[route.path] |= route.options

        # Set the hidden pathes
        # self.hidden = hidden | {'/', '/<path:path>'}
        self.hidden = hidden | {'/'}
        self._build_tree(settings_info)

    def _create_branch(self, path: str, current_description: dict):
        """
        Recoursively create a branch and all of it's children
        """

        # Get the current node we're building
        try:
            node = self.tree[path]
        except treelib.exceptions.NodeIDAbsentError as e:
            raise KeyError(str(e)) from e

        # Build all of our child nodes
        child_nodes = []
        # Iterate over the tree children 
        for child_id in node.successors(self.tree.identifier):
            # The paths are used as IDs in the tree, so child_id is the actual path
            child_node = self.tree[child_id]
            node_options = current_description['options']
            child_node_dict = node_options[child_node.tag]

            if child_node.is_leaf():
                actions = self.routes[child_id]
                child_nodes.append(Leaf.from_data(child_id, actions, **child_node_dict))
            else:
                child_nodes.append(self._create_branch(child_id, child_node_dict))

        # Populate the node data with the create branch
        node.data = Branch.from_data(
            uri=path,
            child_nodes=child_nodes,
            **current_description
        )

        return node.data

    @property
    def root(self):
        return self.tree.get_node(self.tree.root).data

    def hide(self, name):
        self.hidden.add(name)

    def unhide(self, name):
        self.hidden.remove(name)

    def _path_superset(self):
        """
        Returns a superset to all the possible routes (nodes and leaves alike).
        Routes to all the nodes are created by parsing the leave paths.
        For example if there's a leaf route '/a/b/c', '/a', and '/a/b' will be added
        """
        superset = set()
        for path in self.routes:
            partial_path = []
            for match in re.findall(path_pattern, path):
                partial_path.append(match)
                superset.add(''.join(partial_path))

        return superset

    def _build_tree(self, descriptions: dict):
        self.tree = Tree()

        paths = self._path_superset()

        self.tree.create_node('configuration', '/')  # root node

        # Looping over sorted paths because parents need to be created first
        # and /b comes before /b/a when using `sorted`
        for path in sorted(paths):
            # Split on the last '/'
            parent, _, end = path.rpartition('/')
            # The left part is the parent of the full path
            parent = parent or '/'

            # Create the actual node object
            # This tree objects supports O(1) searching by the identifier.
            # Using the path as identifier will allow very simple access to the data
            self.tree.create_node(tag=end, identifier=path, parent=parent)

        self._create_branch('/', descriptions)
