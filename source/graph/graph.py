from typing import Dict, List, Union


class Node:
    ID = 0

    def __init__(self, name: str = ''):
        self._id = Node.ID
        self._name = name

        Node.ID += 1

    def __repr__(self) -> str:
        return '{} {} ({})'.format(self.__class__.__name__, self._id, self._name)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name


class Edge:
    ID = 0

    def __init__(self, source: Node, target: Node, name: str = ''):
        self._id = Edge.ID
        self._name = name
        self._source = source
        self._target = target

        Edge.ID += 1

    def __repr__(self) -> str:
        return '{} {} ({} -> {}) [{}]'.format(self.__class__.__name__, self._id, self._source, self._target, self._name)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def source(self) -> Node:
        return self._source

    @property
    def target(self) -> Node:
        return self._target


class Graph:
    def __init__(self):
        self._nodes = {}
        self._edges = []

    def __repr__(self) -> str:
        return '{} ({}, {})'.format(self.__class__.__name__, len(self._nodes), len(self._edges))

    def __str__(self) -> str:
        s = self.__repr__()
        s += '\n---'
        for _, n in self._nodes.items():
            s += '\n- {}'.format(n)
        s += '\n---'
        for e in self._edges:
            s += '\n - {}'.format(e)
        return s

    @property
    def nodes(self) -> Dict[int, Node]:
        return self._nodes

    @property
    def edges(self) -> List[Edge]:
        return self._edges

    def print(self):
        print(self)

    def node(self, node: Union[int, str]) -> Union[Node, None]:
        if isinstance(node, int):
            return self._nodes[node]
        elif isinstance(node, str):
            for _, n in self._nodes.items():
                if n.name == node:
                    return n
        return None

    def edge(self, edge: Union[int, str]) -> Union[Edge, None]:
        if isinstance(edge, int):
            return self._edges[edge]
        elif isinstance(edge, str):
            for e in self._edges:
                if e.name == edge:
                    return e
        return None

    def neighbours(self, node: Node) -> List[Node]:
        return [e.target for e in self._edges if e.source.id == node.id]

    def add_node(self, node: Node):
        self._nodes[node.id] = node

    def remove_node(self, node: Node):
        del self._nodes[node.id]

    def add_edge(self, edge: Edge):
        self._edges.append(edge)

    def remove_edge(self, edge: Edge):
        self._edges.remove(edge)

    @staticmethod
    def check_cycles(graph, check_all: bool = False) -> List[List[Node]]:
        """
        Tarjan's algorithm: https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
        Complexity: O(|E| + |V|)
        :param graph: Graph
        :param check_all: bool          If False, stop at first cycle, otherwise get all cycles.
        :return: List[List[Node]]       A list of list that contains all cycles in the graph.
        """
        cycles = []
        stack = []
        index = [-1 for _ in range(0, len(graph.nodes))]
        low_link = [-1 for _ in range(0, len(graph.nodes))]
        on_stack = [False for _ in range(0, len(graph.nodes))]

        def strongconnected(_id: int, i: int):
            v = _id
            index[v] = i
            low_link[v] = i
            on_stack[v] = True
            stack.append(v)
            i += 1

            # Advance to all neighbours.
            for e in graph.neighbours(graph.nodes[v]):
                w = e.id
                if index[w] == -1:
                    strongconnected(w, i)

                    # Exit condition for one cycle.
                    if len(cycles) == 1 and not check_all:
                        return

                    low_link[v] = min(low_link[v], low_link[w])
                elif on_stack[w]:
                    low_link[v] = min(low_link[v], index[w])

            if low_link[v] == index[v]:
                temp_stack = []
                w = stack.pop()
                on_stack[w] = False
                temp_stack.append(graph.nodes[w])
                while w != v:
                    w = stack.pop()
                    on_stack[w] = False
                    temp_stack.append(graph.nodes[w])

                # Add only strongly connected components that consist of at least 2 nodes.
                if len(temp_stack) > 1:
                    cycles.append(temp_stack)

                # Exit condition for one cycle.
                if len(cycles) == 1 and not check_all:
                    return

        # Check strongly connected components for evey node.
        for _, n in graph.nodes.items():
            if index[n.id] == -1:
                strongconnected(n.id, 0)

                # Exit condition for one cycle.
                if len(cycles) == 1 and not check_all:
                    return cycles

        return cycles
