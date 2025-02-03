import genesis as gs

gs.init(backend=gs.cpu)

scene = gs.Scene()

plane = scene.add_entity(
    gs.morphs.Plane(),
)
franka = scene.add_entity(
    # gs.morphs.URDF(
    #     file='urdf/panda_bullet/panda.urdf',
    #     fixed=True,
    # ),
    # gs.morphs.MJCF(file="xml/franka_emika_panda/panda.xml"),
    gs.morphs.URDF(
        file = 'avater/abb_gofa/abb_gofa.urdf',
        fixed=True,
        #'urdf/shadow_hand/shadow_hand.urdf',
    )

)

scene.build()
for i in range(1000):
    scene.step()
