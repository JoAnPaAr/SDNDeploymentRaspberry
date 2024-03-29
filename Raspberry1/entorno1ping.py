#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():
    
    info('***Create a network...\n')
    #Se indica el tipo de conexion que sera Link y el tipo de conmutador que sera switchOvs
    net = Mininet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )
    
    #Se crea una instancia del controlador con la IP del dispositivo en el que se va a ejecutar
    #el controlador
    c0 = net.addController('c0', controller=RemoteController, ip='192.168.1.151', port=6633 )
    
    info('*** Add switches\n')
    #Se crea una instancia de Switch
    s11 = net.addSwitch('s11')
    
    info('*** Add hosts\n')
    #Se crean los terminales de la topologia
    h11 = net.addHost('h11',cls=Host, ip='10.0.0.11/24')
    h12 = net.addHost('h12',cls=Host, ip='10.0.0.12/24')
    h13 = net.addHost('h13',cls=Host, ip='10.0.0.13/24')

    info('*** Add links\n')
    #Se vinculan las terminales al switch de la topologia
    net.addLink(s11,h11)
    net.addLink(s11,h12)
    net.addLink(s11,h13)
    
    info('*** Starting controllers\n')
    #Conecta la topologia al controlador
    c0.start()

    info('*** Creating interfaces\n')
    #Se indica al conmutador cual es el controlador al que debe conectarse
    s11.start([c0])
    #Creando el tunel GRE entre la raspberry actual y raspberry2
    s11.cmd("ip link add s11-tfg2 type gretap local 192.168.1.151 remote 192.168.1.152 ttl 64")
    s11.cmd("ip link set s11-tfg2 up")
    
    #Anyadiendo las interfaces al switch de la topologia
    Intf("s11-tfg2",node=s11)
    net.start()
    CLI(net)
    
    info('***Stopping network')
    #Elimina las interfaces que se han creado para esta topologia
    s11.cmd("ip link del dev s11-tfg2")
    net.stop()
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
