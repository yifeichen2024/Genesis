import genesis as gs

gs.init(backend=gs.cpu)

# scene = gs.Scene()

scene = gs.Scene(
    viewer_options=gs.options.ViewerOptions(
        camera_pos=(0, -3.5, 2.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=30,
        max_FPS=60,
    ),
    sim_options=gs.options.SimOptions(
        dt=0.01,
    ),
    show_viewer=True,
)

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
        file = 'avater/avatar_genesis.urdf',
        fixed=True,
        # 'avater/avatar_genesis.urdf'
        #'urdf/shadow_hand/shadow_hand.urdf',
        # 'avater/abb_gofa/abb_gofa.urdf'
    )

)

cam = scene.add_camera(
    res=(640, 480),
    pos=(3.0, -3.0, 1.5),
    lookat=(0.5, 0.5, 0.5),
    fov=20,
    GUI=True,
)
scene.build()

cam.start_recording()
for i in range(500):
    scene.step()
    cam.render()
    
cam.stop_recording(save_to_filename="avater/video/avatar.mp4", fps=60)