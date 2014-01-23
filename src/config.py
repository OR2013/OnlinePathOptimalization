import re

class Config(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def generate_sumocfg(self):
        '''Generate sumocfg file'''

        with open('./config/'+self.prefix+'.sumocfg', 'w') as f:
            f.write('''<configuration>
    <input>
        <net-file value="{0}.net.xml"/>
        <route-files value="{0}.rou.xml"/>
        <gui-settings-file value="{0}.settings.xml"/>
    </input>

    <traci_server>
        <remote-port value="8813"/>
    </traci_server>
</configuration>'''.format(self.prefix))
    
    def generate_settings(self):
        '''Generate sumo settings file'''

        with open('./config/'+self.prefix+'.settings.xml', 'w') as f:
            f.write('''<viewsettings>
    <viewport zoom="500"/>
    <delay value="100"/>
</viewsettings>''')

    def get_test_car(self):
        '''Get car which moves will be simulated'''

        with open('./config/'+self.prefix+'.rou.xml', 'r') as f:
            vehicles = []
            content = f.read()
            pattern = re.compile(r'<vehicle id="(\d+)".*?>')
            iterator = pattern.finditer(content)
            for match in iterator:
                vehicles.append(match.group(1))
        return vehicles[len(vehicles) / 2]
