import os, sys
import re
from collections import defaultdict
from heapq import *

class Graph(object):

    def __init__(self, netfile, verbose):
        '''Initialize graph'''

        self.INFINITY = sys.maxint
        self.netfile = netfile
        self.verbose = verbose
        
        self.info('Reading edges...')
        self.read_edges()
        self.info('Success')

        self.info('Reading connections...')
        self.read_connections()
        self.info('Success')


    def info(self, msg):
        '''Print verbose messages'''
        
        if self.verbose:
            print msg


    def read_edges(self):
        '''Read edges from network file'''

        self.edges = []
        with open(self.netfile, 'r') as f:
            content = f.read()
            pattern = re.compile(r'<edge id="(-?\d+)".*?>')
            iterator = pattern.finditer(content)
            for match in iterator:
                self.edges.append(match.group(1))
        return self.edges

    
    def read_connections(self):
        '''Read connections from network file'''

        self.connections = defaultdict(list)
        with open(self.netfile, 'r') as f:
            content = f.read()
            pattern = re.compile(r'<connection from="(-?\d+)" to="(-?\d+)".*?/>')
            iterator = pattern.finditer(content)
            for match in iterator:
                self.connections[match.group(1)].append(match.group(2))
        return self.connections


    def set_destination_and_costs(self, destination, costs):
        '''Set trip destination and initial travelling costs'''

        self.destination = destination
        self.costs = costs


    def is_optimalization_needed(self, route, costs, alpha):
        '''Check whether route optimalization in needed'''

        for edge in self.edges:
            # cost of edge belonging to route has increased significantly
            if edge in route and (float(costs[edge]) - self.costs[edge]) / self.costs[edge] > alpha:
                return True
            # cost of edge not belonging to route has decreased significantly
            elif edge not in route and (float(self.costs[edge]) - costs[edge]) / self.costs[edge] > alpha:
                return True
        return False


    def dijkstra(self, source, costs):
        '''Compute shortest routes in terms of travelling costs using Dijkstra algorithm'''

        # initialize heap, previous edge dictionary and distance dictionary
        heap = []
        prev = {}
        dist = {}
        for edge in self.edges:
            if edge != source:
                heappush(heap, (self.INFINITY, edge))
                dist[edge] = self.INFINITY
                prev[edge] = 'undef'
        heappush(heap, (0, source))
        prev[source] = 'undef'
        dist[source] = 0
        
        # computing shortest routes
        while len(heap) > 0:
            cost, edge = heappop(heap)
            for neighbour in self.connections[edge]:
                if dist[neighbour] > dist[edge] + costs[neighbour]:
                    # shorter path found
                    dist[neighbour] = dist[edge] + costs[neighbour]
                    prev[neighbour] = edge
                    heappush(heap, (dist[neighbour], neighbour))

        # recovering shortest route from source to destination using previous edge dictionary
        edge = self.destination
        route = [edge]
        # getting previous edge as long as it is defined
        while prev[edge] != 'undef':
            edge = prev[edge]
            route.append(edge)
        route.reverse()
        return route
