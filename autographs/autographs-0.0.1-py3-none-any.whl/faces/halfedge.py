
import geopandas as gpd
import pysal as ps
import numpy as np
import matplotlib.pyplot as plt


class Vertex:
    def __init__(self, label, point, data=None):
        """
        Initializes a vertex object.
        :label:     Label (i.e. name) for this vertex.
        :point:     Position of the vertex in an embedding.
        :data:      Data associated with this vertex.
        :returns:   None
        """

        """
        Properties.
        :label:     Label of the vertex.
        :point:     Where this vertex has been mapped to in an embedding.
        :data:      Any data associated with this vertex.
        :edges:     Dict of outgoing edges from this vertex, keyed by neighbor.
        """
        self.label = label
        self.point = point
        self.data = data
        self.edges = {}

    def add_edge(self, v):
        """
        Add an outgoing edge to this vertex.
        :v:         Head of the edge.
        :returns:   None
        """
        self.edges[v] = Edge(self, v)

    @property
    def x(self):
        """
        Get the x-coordinate in (an assumed) 2d embedding.
        :returns: Number; x-coordinate.
        """
        return self.point[0]

    @property
    def y(self):
        """
        Get the y-coordinate in (an assumed) 2d embedding.
        :returns: Number; y-coordinate.
        """
        return self.point[1]

    @property
    def xy(self):
        """
        Get the (x,y) coordinate pair in (an assumed) 2d embedding.
        :returns: Tuple; (x,y) coordinate pair.
        """
        return self.x, self.y

    def __eq__(self, other):
        """
        Checks equality between two Vertex objects.
        :other:     Vertex to be compared to.
        :returns:   Boolean; are `self` and `other` the same?
        """
        return self.label == other.label or self.point == other.point

    def __hash__(self):
        """
        Implements a hashing method so that we can quickly look up vertices
        without sacrificing performance.
        :returns: None
        """
        return hash((self.label, self.point))

    def __str__(self):
        """
        String representation of the Vertex.
        :returns: String containing the label of the vertex.
        """
        return str(self.label)


class Edge:
    def __init__(self, tail, head):
        """
        Initializes an edge object.
        :tail:      Vertex the edge is coming from.
        :head:      Vertex the edge is going to.
        :returns:   None
        """

        """
        Properties.
        :tail:      Starting vertex of this edge.
        :head:      Ending vertex of this edge.
        :traversed: Has this edge been traversed yet?
        :next:      Points to the next edge in the cyclic ordering.
        """
        self.tail = tail
        self.head = head
        self.traversed = False
        self.next = None

    def __eq__(self, other):
        """
        Checks equality between two Edge objects.
        :other:     Edge object to be compared to.
        :returns:   Boolean; are `self` and `other` the same?
        """
        return self.tail == other.tail and self.head == other.head

    def __str__(self):
        """
        String reperesentation of the edge.
        :returns:   A tuple containing the two labels of the vertices at `head` and
                    `tail`.
        """
        return str((self.tail.label, self.head.label))

    def __hash__(self):
        """
        Implements a hashing method to store edges in sets.
        :returns: Edge hashed on a (tail, head) tuple.
        """
        return hash((self.tail, self.head))


class HalfEdge:
    def __init__(self, path):
        """
        Initializes a half-edge structure for the given file.
        :path:      Path to a data file.
        :returns:   None
        """

        """
        Properties.
        :adjacency:     Adjacency matrix with each vertex's neighbors ordered
                        (by angle, with respect to the ray (0,1)).
        :faces:         Faces of the graph, denoted by edges.
        :centroids:     List of centroids.
        :df:            DataFrame for (insert block)-level data.
        """
        self.adjacency = {}
        self.faces = []
        self.centroids = None
        self.df = None

        # Get the file and create vertices (and their adjacencies).
        self.df = gpd.read_file(path)
        contiguity = ps.weights.Contiguity.Rook.from_dataframe(self.df)
        self.centroids = self.df.centroid

        # Initialize vertices.
        for label, _ in enumerate(contiguity):
            x, y = self.centroids[label].xy
            v = Vertex(label, (x[0], y[0]))
            self.adjacency[v] = None

        # Go over the adjacency matrix, adding half-edges. Create an external
        # list of unordered neighbors, then order them.
        for index, vertex in enumerate(self.adjacency.keys()):
            unordered = []

            # Since we don't have the neighbors properly set up, we have to
            # iterate over them in a weird way. However, it ends up alright.
            for uncoded_neighbor in contiguity[index].keys():
                # Get the correct neighbor.
                neighbor = list(self.adjacency.keys())[uncoded_neighbor]
                
                # Find the angle between `vertex` and `neighbor`. Basically just
                # took this code from Eugene.
                xdelta = vertex.x - neighbor.x
                ydelta = vertex.y - neighbor.y
                angle = np.arctan2(xdelta, ydelta)
                unordered.append((neighbor, angle))

            # Order the collection of vertices by neighbor, freeze the order in a
            # tuple, then stick it in the adjacency matrix.
            ordered = sorted(unordered, key=lambda n: n[1])
            self.adjacency[vertex] = tuple([tup[0] for tup in ordered])

        # Initialize edge pointers so, if we need to, we can come back and find
        # individual faces. Just keep going `next` -> `next` -> ... -> `next`
        # until we get back to our starting place.
        self._edge_pointers()

    def _get_next_neighbor(self, current, neighbor):
        """
        Returns the proper next neighbor in the cyclic ordering.
        :current:   Current vertex.
        :neighbor:  Current neighbor; from here, we want to figure out
                    where to go next.
        :return:    Vertex; proper neighbor in the ordering.
        """
        ordered_neighbors = self.adjacency[neighbor]
        index_from = ordered_neighbors.index(current)
        return ordered_neighbors[(index_from + 1) % len(ordered_neighbors)]

    def _edge_pointers(self):
        """
        Sets the `next` pointer for each edge.
        :returns: None
        """
        # Add all the outgoing edges to their respective vertices' edge sets.
        for vertex in self.adjacency:
            for neighbor in self.adjacency[vertex]:
                # Add each edge
                vertex.add_edge(neighbor)

        # Go over the vertices again, but this time, set the `next` pointers
        # for each edge. This will help us identify faces, but also be able to
        # pick a random edge and see which face it bounds.
        for vertex in self.adjacency:
            for neighbor in self.adjacency[vertex]:
                # If this edge has already been traversed, burn the program to
                # the ground. Abandon ship. ~Beware, ye who enter here.~
                if vertex.edges[neighbor].traversed:
                    break

                # Track where we are in the graph. Also, make a list of vertices
                # in the order we encounter them; this way, we can just stitch
                # the vertices in the list together to determine directed edges.
                # Finally, create the final list of edges.
                current = None
                current_neighbor = neighbor
                cycle = []
                edges = []

                # Keep going until we reach the start.
                while current is not vertex:
                    if current is None:
                        current = vertex
                     
                    # Find the next in-order neighbor.
                    next_neighbor = self._get_next_neighbor(current, current_neighbor)

                    # Add the current neighbor to the cycle.
                    cycle.append(current_neighbor)

                    # Reset the tracking variables.
                    current = current_neighbor
                    current_neighbor = next_neighbor

                # Get the list of cycles, and mark them as traversed.
                for i in range(len(cycle)):
                    # Here, we're just getting vertex at index `i` and the vertex
                    # at index `i+1`. They must have an edge between them. Then,
                    # we mark them as traversed, and continue.
                    edge = cycle[i].edges[cycle[(i + 1) % len(cycle)]]
                    edge.traversed = True
                    edges.append(edge)

                # Stitch the cycles together.
                for j in range(len(edges)):
                    # Again, we are getting the the edge at index `j` and the
                    # edge at index `j+1`.
                    edges[j].next = edges[(j + 1) % len(edges)]

                # Assign the faces!
                current_edge = None
                face = []

                while current_edge is not edges[0]:
                    # Gotta have a starting point!
                    if current_edge is None:
                        current_edge = edges[0]

                    # Otherwise, denote the edges.
                    tl, hl = current_edge.tail.label, current_edge.head.label
                    face.append((tl, hl))

                    # Sweet jesus I spent *such* a long time trying to figure out
                    # why my code wouldn't finish running... and then I realized
                    # I didn't do this. Update the current_edge pointer.
                    current_edge = current_edge.next

                # Append the faces!
                self.faces.append(face)

    def show_map(self):
        """
        Shows the underlying map overlaid with the dual graph.
        :returns:   None
        """
        # Set the base map to be whatever the shapefile bounds, then plot all
        # the centroids.
        basemap = self.df.plot(color="w", edgecolor="lightgray")
        self.centroids.plot(ax=basemap, markersize=1)

        # Iterate over the adjacency matrix, and plot lines from each centroid
        # to neighboring centroids.
        for vertex in self.adjacency:
            for neighbor in self.adjacency[vertex]:
                basemap.plot([vertex.x, neighbor.x], [vertex.y, neighbor.y], linestyle="-", linewidth=1)

        # Don't forget to show the plot!
        plt.show()        


if __name__ == "__main__":
    he = HalfEdge("../test/data/2018_19_counties/county.shp")

    # Test for faces.
    for face in he.faces:
        print(face)

    he.show_map()