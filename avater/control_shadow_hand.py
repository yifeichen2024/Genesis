import numpy as np 
import genesis as gs 

#===== init =====
gs.init(backend=gs.gpu)

#===== Create a scene =====
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

shadow_hand = scene.add_entity(
    gs.morphs.URDF(
        file = 'urdf/shadow_hand/shadow_hand.urdf',
    )
)
# Try addin the force field to the plane.
shadow_hand_force = scene.add_force_field()

cam = scene.add_camera(
    res=(640, 480),
    pos=(2.0, -2.0, 1.5),
    lookat=(0, 0, 0.2),
    fov=20,
    GUI=True,
)
scene.build()


# get joints 
joint_names = [
    "forearm_joint",
    "wrist_joint",
    "thumb_joint1",
    "thumb_joint2",
    "thumb_joint3",
    "thumb_joint4",
    "thumb_joint5",
    "index_finger_joint1",
    "index_finger_join2",
    "index_finger_joint3",
    "index_finger_joint4",
    "middle_finger_joint1",
    "middle_finger_joint2",
    "middle_finger_joint3",
    "middle_finger_joint4",
    "ring_finger_joint1",
    "ring_finger_joint2",
    "ring_finger_joint3",
    "ring_finger_joint4",
    "little_finger_joint1",
    "little_finger_joint2",
    "little_finger_joint3",
    "little_finger_joint4",
    "little_finger_joint5"
]

dofs_idx = [shadow_hand.get_joint(name).dof_idx_local for name in joint_names]
print(dofs_idx.__len__())

# 设置位置增益 (kp)
shadow_hand.set_dofs_kp(
    kp=np.array([4500] * 24),  # 24 个关节的位置增益
    dofs_idx_local=dofs_idx,
)

# 设置速度增益 (kv)
shadow_hand.set_dofs_kv(
    kv=np.array([450] * 24),  # 24 个关节的速度增益
    dofs_idx_local=dofs_idx,
)

# 设置力范围 (force range)
shadow_hand.set_dofs_force_range(
    lower=np.array([-87] * 24),  # 24 个关节的最小力
    upper=np.array([87] * 24),   # 24 个关节的最大力
    dofs_idx_local=dofs_idx,
)
cam.start_recording()

# for i in range(500):
#     if i < 50:
#         shadow_hand.set_dofs_position(np.array([0, 0,              
#                                                 0, 0, 0, 0, 0,     
#                                                 0, 0, 0, 0,        
#                                                 0, 0, 0, 0,        
#                                                 0, 0, 0, 0,        
#                                                 0, 0, 0, 0, 0]), dofs_idx)
#     elif i < 200:
#         shadow_hand.set_dofs_position(np.array([0, 0.5,              
#                                                 0, 0.2, 0.2, 0, 0,     
#                                                 0, 0.2, 0.5, 0,        
#                                                 0, 0.2, 0.5, 0,        
#                                                 0, 0.2, 0.5, 0,        
#                                                 0, 0.2, 0.2, 0, 0]), dofs_idx)   
#     else:
#         shadow_hand.set_dofs_position(np.array([0, 0.5,              
#                                                 0, 0.2, 0, 0.2, 0,     
#                                                 0, 0.5, 0, 0.5,        
#                                                 0, 0.5, 0, 0.5,        
#                                                 0, 0.5, 0, 0.5,        
#                                                 0, 0.2, 0, 0.2, 0]), dofs_idx)   

#     print("Joint position: ", shadow_hand.get_dofs_position(dofs_idx))
    
#     scene.step()
#     cam.render()

# PD 控制
for i in range(1250):
    if i == 0:
        # 初始目标位置
        shadow_hand.control_dofs_position(
            np.array([0] * 24),  # 24 个关节的目标位置
            dofs_idx,
        )
    elif i == 250:
        # 中间目标位置
        shadow_hand.control_dofs_position(
            np.array([0.2] * 24),  # 24 个关节的目标位置
            dofs_idx,
        )
    elif i == 500:
        # 回到初始位置
        shadow_hand.control_dofs_position(
            np.array([0] * 24),  # 24 个关节的目标位置
            dofs_idx,
        )
    elif i == 750:
        # 控制前 12 个关节的位置，后 12 个关节的速度
        shadow_hand.control_dofs_position(
            np.array([0] * 12),  # 前 12 个关节的位置
            dofs_idx[:12],
        )
        shadow_hand.control_dofs_velocity(
            np.array([0.5] * 12),  # 后 12 个关节的速度
            dofs_idx[12:],
        )
    elif i == 1000:
        # 力控制
        shadow_hand.control_dofs_force(
            np.array([0] * 24),  # 24 个关节的目标力
            dofs_idx,
        )

    # 打印控制力和实际力
    print("control force:", shadow_hand.get_dofs_control_force(dofs_idx))
    print("internal force:", shadow_hand.get_dofs_force(dofs_idx))
    print(shadow_hand_force)
    scene.step()
    cam.render()

# save recordings
cam.stop_recording(save_to_filename="avater/video/shadow_hand_control.mp4", fps=60)