import openseespy.opensees as ops
import opsvis as opsv
import matplotlib.pyplot as plt

# Units

m = 1
KN = 1
Pa = 1

# Materiales

E = 1*Pa
A = 1
I = 1

ops.wipe()

ops.model('basic', '-ndm', 2, '-ndf', 3)

Wy = -4*KN/m

# Set Nodes

ops.node(1, 0., 0.)
ops.node(2, 4., 0.)
ops.node(3, 6., 0.)

ops.fix(1, 1, 1, 0)
ops.fix(2, 0, 1, 0)

opsv.plot_model()
plt.title('Modelo_puntos')

ops.geomTransf('Linear', 1)

ops.element('elasticBeamColumn', 1, 1, 2, A, E, I, 1)
ops.element('elasticBeamColumn', 2, 2, 3, A, E, I, 1)

ops.timeSeries('Constant', 1)
ops.pattern('Plain', 1, 1)

ops.eleLoad('-ele', 2, '-type', '-beamUniform', Wy, 0)

opsv.plot_model()
plt.title('Definig elements')

opsv.plot_loads_2d()
plt.title('Elements loads')


# Analysis commandas

ops.constraints('Plain')
ops.numberer('Plain')
ops.system('BandSPD')

ops.test('NormDispIncr', 1.0e-6, 6, 2)
ops.algorithm('Linear')
ops.integrator('LoadControl', 1)
ops.analysis('Static')
ops.analyze(1)

ops.printModel()

opsv.plot_defo()

ops.recorder('Element', '-file', "Elements.out",'-time','-ele', 1, 'forces')

#sfacN, sfacV, sfacM = 5.e-5, 5.e-5, 5.e-5
sfacN, sfacV, sfacM = 5.e-2, 5.e-2, 5.e-2

opsv.section_force_diagram_2d('N', sfacN)
plt.title('Axial force distribution')

opsv.section_force_diagram_2d('T', sfacV)
plt.title('Shear force distribution')

opsv.section_force_diagram_2d('M', sfacM)
plt.title('Bending moment distribution')

plt.show()
exit()