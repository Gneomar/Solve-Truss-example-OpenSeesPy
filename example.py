import openseespy.opensees as ops
import opsvis as opsv
import matplotlib.pyplot as plt


# Units

m = 1
KN = 1
Pa = 1
mm = 1*10**(-3)*m

# Materials

E = 2*10**11*Pa
A = 1200*mm**2

# Remove existing model
ops.wipe()

# set modelbuilder
ops.model('basic', '-ndm', 2, '-ndf', 2)

# Create nodes

ops.node(1, 0.0, 0.0)
ops.node(2, 4.0, 0.0)
ops.node(3, 7.0, 0.0)
ops.node(4, 4.0, 4.0)

# Set boundary conditions

ops.fix(1, 1, 1)
ops.fix(3, 0, 1)

# Define materials

ops.uniaxialMaterial('Elastic', 1, E)

# Define elements

ops.element('Truss', 1, 1, 2, A, 1)
ops.element('Truss', 2, 2, 3, A, 1)
ops.element('Truss', 3, 1, 4, A, 1)
ops.element('Truss', 4, 2, 4, A, 1)
ops.element('Truss', 5, 3, 4, A, 1)

# Create TimeSeries

ops.timeSeries('Linear', 1)

# Create a plain load pattern

ops.pattern('Plain', 1, 1)

# Create the nodal load - command: load nodeID xForce yForce
ops.load(2, 0.0, -84.0*KN)
ops.load(4, -35.0*KN, 0.0)

# ------------------------------
# Start of analysis generation
# ------------------------------

# create SOE
ops.system("BandSPD")

# create DOF number
ops.numberer("RCM")

# create constraint handler
ops.constraints("Plain")

# create integrator
ops.integrator("LoadControl", 1.0)

# create algorithm
ops.algorithm("Linear")

# create analysis object
ops.analysis("Static")

# perform the analysis
ops.analyze(1)

# Graph

opsv.plot_model()
plt.title('Model after defining elements')

opsv.plot_loads_2d()
plt.title('Model with loads')

opsv.plot_defo()
plt.title('Model deformation')

sfacN, sfacV, sfacM = 5.e-5, 5.e-5, 5.e-5

opsv.section_force_diagram_2d('N', sfacN)
plt.title('Axial force distribution')

plt.show()

exit()