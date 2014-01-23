import os, sys
import subprocess
from optparse import OptionParser
from graph import Graph
from config import Config

try:
    sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))
    from sumolib import checkBinary
except Exception:
    sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")
import traci

class Simulation(object):
    
    def __init__(self):
        '''Initialize simulation'''

        self.PORT = 8813
        self.DEVNULL = open(os.devnull, 'wb')
        self.get_options()
        self.create_config_dir()
        if not self.options.nogen:
            self.generate_graph()
        self.get_configuration()
        self.graph = Graph('./config/' + self.options.prefix + '.net.xml', self.options.verbose)


    def get_options(self):
        '''Get command line options'''

        optParser = OptionParser()
        optParser.add_option('--nogui', action='store_true', default=False, help='run the command line version of sumo')
        optParser.add_option('--nogen', action='store_true', default=False, help='run without road network generation')
        optParser.add_option('-p', '--prefix', dest='prefix', default='random', help='files names prefix')
        optParser.add_option('-s', '--size', dest='size', default='10', help='road network size')
        optParser.add_option('-a', '--alpha', dest='alpha', default='0.05', help='alpha parameter')
        optParser.add_option('-r', '--rate', dest='rate', default='2', help='repetition rate')
        optParser.add_option('-v', '--verbose', action='store_true', default=False, help='run with detailed information')
        optParser.add_option('-d', '--max-distance', dest='distance', default='500', help='maximum length of edge')
        self.options, args = optParser.parse_args()

        if self.options.nogui:
            self.sumoBinary = checkBinary('sumo')
        else:
            self.sumoBinary = checkBinary('sumo-gui')


    def create_config_dir(self):
        '''Create config directory'''

        try:
            os.mkdir('./config')
        except OSError:
            pass


    def info(self, msg):
        '''Print verbose information'''

        if self.options.verbose:
            print msg


    def generate_graph(self):
        '''Generate road network and trips'''

        self.info('Generating road network...')
        subprocess.Popen(['netgenerate', '--rand', '--random', 'true',  '--rand.iterations', self.options.size, '--rand.max-distance', self.options.distance, '--no-turnarounds', 'true', '-o', './config/'+self.options.prefix+'.net.xml'], stdout=self.DEVNULL, stderr=self.DEVNULL).wait()

        self.info('Generating trips...')
        subprocess.Popen(['python', os.path.join(os.environ['SUMO_HOME'], 'tools/trip/randomTrips.py'), '-e', str(int(self.options.size) * int(self.options.rate) * 2), '-p', self.options.rate ,'-n', './config/'+self.options.prefix+'.net.xml', '-r', './config/'+self.options.prefix+'.rou.xml', '-o', './config/'+self.options.prefix+'.trips.xml', '--fringe-factor', '1000000'], stdout=self.DEVNULL, stderr=self.DEVNULL).wait()
        self.info('Success.')


    def get_configuration(self):
        '''Create configuration files and get test vehicle's ID'''

        self.info('Writing configuration...')
        self.config = Config(self.options.prefix)
        self.config.generate_sumocfg()
        self.config.generate_settings()
        self.info('Success.')

        self.info('Getting test car...')
        self.vehicleID = self.config.get_test_car()
        self.info('Success.')
        

    def get_costs(self):
        '''Get current travel time for all edges in graph'''

        costs = {}
        for edge in self.graph.edges:
            costs[edge] = traci.edge.getTraveltime(edge.encode('utf-8'))
        return costs
    

    def run(self, vehicleID, optimalization):
        '''Execute the TraCI control loop'''
        
        traci.init(self.PORT)
        # wait until chosen car is on the road network
        while not vehicleID in traci.simulation.getDepartedIDList():
            traci.simulationStep()
        # set GUI view to track chosen vehicle
        if not self.options.nogui:
            traci.gui.trackVehicle('View #0', vehicleID)
            traci.vehicle.setColor(vehicleID, (255,0,0,0))
        # get chosen car destination
        if optimalization:
            self.graph.set_destination_and_costs(traci.vehicle.getRoute(vehicleID)[-1], self.get_costs())
        # get simulation reference time
        time = traci.simulation.getCurrentTime()
        while not vehicleID in traci.simulation.getArrivedIDList():
            if optimalization:
                # get ID of edge chosen vehicle is currently on
                edge = traci.vehicle.getRoadID(vehicleID)
                # check whether optimalization is needed
                if edge in self.graph.edges and \
                    traci.vehicle.getLanePosition(vehicleID) >= 0.9 * traci.lane.getLength(traci.vehicle.getLaneID(vehicleID)) and \
                    self.graph.is_optimalization_needed(traci.vehicle.getRoute(vehicleID), self.get_costs(), float(self.options.alpha)):
                    # calculate shortest path using Dijkstra algorithm
                    shortestPath = self.graph.dijkstra(edge, self.get_costs())
                    # set shortest path for chosen vehicle
                    traci.vehicle.setRoute(vehicleID, shortestPath)
            # make next simulation step
            traci.simulationStep()
        # get simulation time
        time = traci.simulation.getCurrentTime() - time
        traci.close()
        sys.stdout.flush()
        # return simulation time
        return time

    def main(self):
        '''Main simulation function'''

        # start SUMO simulator process with on-line path optimalization
        sumoProcess = subprocess.Popen([self.sumoBinary, '-c', './config/'+self.options.prefix+'.sumocfg'], stdout=self.DEVNULL, stderr=self.DEVNULL)
        optTime = self.run(self.vehicleID, True)
        sumoProcess.wait()

        # start SUMO simulator process without on-line path optimalization
        sumoProcess = subprocess.Popen([self.sumoBinary, '-c', './config/'+self.options.prefix+'.sumocfg'], stdout=self.DEVNULL, stderr=self.DEVNULL)
        noOptTime = self.run(self.vehicleID, False)
        sumoProcess.wait()

        # return simulations parameters
        return [str(optTime / 1000.), str(noOptTime / 1000.), self.options.size, self.options.alpha, self.options.rate, self.options.distance]

if __name__ == '__main__':

    result = Simulation().main()
    print ','.join(result)