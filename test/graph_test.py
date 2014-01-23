import unittest
from src.graph import Graph

class TestGraph(unittest.TestCase):

    def test_read_edges(self):
        graph = Graph('test/netfiles/test1.net.xml', False)
        self.assertEqual(graph.edges, ['-11', '-25', '-26', '-28', '-3', '-32', '-34', '-38', '-42', '-5', '11', '25', '26', '28', '3', '32', '34', '38', '42', '5'])
        graph = Graph('test/netfiles/test2.net.xml', False)
        self.assertEqual(graph.edges, ['-105', '-15', '-19', '-3', '-41', '-5', '-84', '-91', '-95', '105', '15', '19', '3', '41', '5', '84', '91', '95'])
        graph = Graph('test/netfiles/test3.net.xml', False)
        self.assertEqual(graph.edges, ['-11', '-13', '-14', '-16', '-3', '-32', '-33', '-37', '-5', '-7', '-9', '11', '13', '14', '16', '3', '32', '33', '37', '5', '7', '9'])

    def test_read_connections(self):
        graph = Graph('test/netfiles/test1.net.xml', False)
        self.assertEqual(graph.connections.items(), [('-5', ['25', '11', '3']), ('26', ['32', '34', '-5']), ('-28', ['26', '-3']), ('-38', ['42', '-28']), ('-42', ['-28', '38']), ('-25', ['11', '3', '5']), ('-26', ['-3', '28']), ('-34', ['-5', '-26', '32']), ('28', ['38', '42']), ('-32', ['34', '-5', '-26']), ('-11', ['3', '5', '25']), ('3', ['28', '26']), ('5', ['-26', '32', '34']), ('-3', ['5', '25', '11'])])
        graph = Graph('test/netfiles/test2.net.xml', False)
        self.assertEqual(graph.connections.items(), [('15', ['41']), ('-105', ['91', '95', '-84']), ('-91', ['95', '-84', '105']), ('-84', ['-41']), ('-41', ['-15']), ('-95', ['-84', '105', '91']), ('41', ['84']), ('-5', ['19', '15', '3']), ('-15', ['3', '5', '19']), ('-3', ['5', '19', '15']), ('-19', ['15', '3', '5']), ('84', ['105', '91', '95'])])
        graph = Graph('test/netfiles/test3.net.xml', False)
        self.assertEqual(graph.connections.items(), [('-5', ['3', '7', '9']), ('-7', ['9', '5', '3']), ('3', ['11', '13']), ('-37', ['33', '-7']), ('-33', ['-7', '37']), ('-32', ['-5', '14', '16']), ('7', ['37', '33']), ('-11', ['13', '-3']), ('33', ['-14', '-9']), ('-13', ['-3', '11']), ('5', ['14', '16', '32']), ('-14', ['16', '32', '-5']), ('-3', ['7', '9', '5']), ('-16', ['32', '-5', '14']), ('9', ['-33', '-14']), ('-9', ['5', '3', '7']), ('14', ['-9', '-33'])])
        
    def test_is_optimalization_needed(self):
        graph = Graph('test/netfiles/test1.net.xml', False)
        graph.edges = ['1', '2', '3', '4', '5']
        graph.set_destination_and_costs('5', {'1':10, '2':10, '3':10, '4':10, '5':10})
        self.assertTrue(graph.is_optimalization_needed(['1','3','5'], {'1':10, '2':10, '3':12, '4':10, '5':10}, 0.1))
        self.assertTrue(graph.is_optimalization_needed(['1','3','5'], {'1':10, '2':8, '3':10, '4':10, '5':10}, 0.1))
        self.assertFalse(graph.is_optimalization_needed(['1','3','5'], {'1':10, '2':10, '3':8, '4':10, '5':10}, 0.1))
        self.assertFalse(graph.is_optimalization_needed(['1','3','5'], {'1':10, '2':12, '3':10, '4':10, '5':10}, 0.1))

    def test_dijkstra_simple(self):
        graph = Graph('test/netfiles/test1.net.xml', False)
        costs = {}
        for edge in graph.edges:
            costs[edge] = 1
        graph.set_destination_and_costs(graph.edges[-1], costs)
        self.assertEqual(graph.dijkstra(graph.edges[1], costs), ['-25','5'])

    def test_dijkstra_complex(self):
        graph = Graph('test/netfiles/test4.net.xml', False)
        costs = {}
        for edge in graph.edges:
            costs[edge] = 1
        graph.set_destination_and_costs('30668', costs)
        self.assertEqual(graph.dijkstra('-31439', costs), ['-31439','-30057','-28887','28866','-23377','-22520','-21950','-17064','-16421','-15637','-3694','-3348','-158','144','-212','213','-370','420','-809','1807','-2481','2488','2556','-3837','3836','4158','4982','12338','-20947','-20171','20161','20824','-22781','-22135','22133','22780','27742','29467','30668'])

if __name__ == '__main__':
    unittest.main()