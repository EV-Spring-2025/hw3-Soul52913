[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/SdXSjEmH)
# EV-HW3: PhysGaussian

This homework is based on the recent CVPR 2024 paper [PhysGaussian](https://github.com/XPandora/PhysGaussian/tree/main), which introduces a novel framework that integrates physical constraints into 3D Gaussian representations for modeling generative dynamics.

You are **not required** to implement training from scratch. Instead, your task is to set up the environment as specified in the official repository and run the simulation scripts to observe and analyze the results.


## Getting the Code from the Official PhysGaussian GitHub Repository
Download the official codebase using the following command:
```
git clone https://github.com/XPandora/PhysGaussian.git
```


## Environment Setup
Navigate to the "PhysGaussian" directory and follow the instructions under the "Python Environment" section in the official README to set up the environment.


## Running the Simulation
Follow the "Quick Start" section and execute the simulation scripts as instructed. Make sure to verify your outputs and understand the role of physics constraints in the generated dynamics.


## Homework Instructions
Please complete Part 1–2 as described in the [Google Slides](https://docs.google.com/presentation/d/13JcQC12pI8Wb9ZuaVV400HVZr9eUeZvf7gB7Le8FRV4/edit?usp=sharing).

## Requirement
install opencv to open video for the psnr comparing
```bash
$ pip install opencv-python
```
## Report
### Q1
- Material 1 - jelly
- Video
    - https://youtu.be/NhrALTmRiYk
- Material 2 - metal
- To use metal, have to add parameter "yield_stress"
- Video
    - https://youtu.be/NhrALTmRiYk?t=30
### Q2
#### Material 1 - jelly
- "n_grid":
    - 50 -> 25  
    - Video: https://youtu.be/NhrALTmRiYk?t=6
    - PSNR compare to baseline
        - Average PSNR: 22.352728088378907
    ```
    $ python video_psnr.py videos/output_jelly.mp4 videos/output_jelly_ngrid.mp4
    ```
- "grid_v":
    - 0.9999 -> 1.0001  
    - Video: https://youtu.be/NhrALTmRiYk?t=12
    - PSNR compare to baseline
        - Average PSNR: 20.294715530395507
    ```
    $ python video_psnr.py videos/output_jelly.mp4 videos/output_jelly_gridv.mp4
    ```
- "substep_dt":
    - 1e-4 -> 5e-5  
    - Video: https://youtu.be/NhrALTmRiYk?t=18
    - PSNR compare to baseline
        - Average PSNR: 21.003537063598632
    ```
    $ python video_psnr.py videos/output_jelly.mp4 videos/output_jelly_substep.mp4
    ```
- "softening":
    - 0.1 -> 0.001 (Video's subtitle is wrong. Should be 0.001)
    - Video: https://youtu.be/NhrALTmRiYk?t=24
    - PSNR compare to baseline
        - Average PSNR: 41.92756750488281
    ```
    $ python video_psnr.py videos/output_jelly.mp4 videos/output_jelly_softening.mp4
    ```
#### Material 2 - metal
- "n_grid":
    - 50 -> 25  
    - Video: https://youtu.be/NhrALTmRiYk?t=36
    - PSNR compare to baseline
        - Average PSNR: 15.619939559936524
    ```
    $ python video_psnr.py videos/output_metal.mp4 videos/output_metal_ngrid.mp4
    ```
- "grid_v":
    - 0.9999 -> 0.9995  
    - Video: https://youtu.be/NhrALTmRiYk?t=42
    - PSNR compare to baseline
        - Average PSNR: 15.619156120300293
    ```
    $ python video_psnr.py videos/output_metal.mp4 videos/output_metal_gridv.mp4
    ```
    - 0.9999 -> 0.98  
    - Video: https://youtu.be/NhrALTmRiYk?t=48
    - PSNR compare to baseline
        - Average PSNR: 14.864701866149902
    ```
    $ python video_psnr.py videos/output_metal.mp4 videos/output_metal_gridv_0.89.mp4
    ```
- "substep_dt":
    - 1e-4 -> 5e-5  
    - Video: https://youtu.be/NhrALTmRiYk?t=54
    - PSNR compare to baseline
        - Average PSNR: 15.640667121887207
    ```
    $ python video_psnr.py videos/output_metal.mp4 videos/output_metal_substep.mp4
    ```
- "softening":
    - 0.1 -> 0.0001
    - Video: https://youtu.be/NhrALTmRiYk?t=60
    - PSNR compare to baseline
        - Average PSNR: 42.35583294677734
    ```
    $ python video_psnr.py videos/output_metal.mp4 videos/output_metal_softening.mp4
    ```
### Take Away
- "n_grid":
For both of the materials, when n_grid is 100, the simulation will core dump. When n_grid is 25, which is half of the original parameter, the simulation becomes faster. The movement of the plant is smaller. Since we reduce the sesolution of the MPM background grid, we will lose small-scale behaviors and possible numerical artifacts and cause under-resolved stress or velocity fields, which explain why the movement is smaller.
    - Raise: more small-scale behaviors, bigger movement
    - Reduce: less small-scale behaviors, smaller movement
- "grid_v":
For jelly, the grid_v can set to 1.0001. However, for metal, setting grid_v to 1.0001 will cause core dump. Thus, I choose to decrease the grid_v. First, for jelly with grid_v value as 1.0001, the movement sustain much longer and bigger than original one. We suppose that grid_v with value over 1 will make velocity decay slower which lead to this simulation result. For metal with grid_v decrease value, first we set the value to 0.98. In the video, we can barely see the movement. To observe more significant difference, I raise the value to 0.9995. We observe that the movement is much smaller than original one. We suppose that lower value will cause velocity decays faster, which explain why the force decays hastly and makes the plant only bend marginally.
    - Raise: velocity decays slower, bigger movement
    - Reduce: velocity decays faster, smaller movement
- "substep_dt":
For both of the materials, when substep_dt is 1e-5, we can't observe any movement in the video. Thus, we raise a little bit to the half of the original value, 5e-5. For both of the result vide, the movement is much smaller than original one. Just like the result of the n_grid experiment result. We suppose that decreases substep_dt will make number of substeps per frame more. This will cause each substep only moves the object a little, reducing the chance of large, abrupt changes. This makes the movement smaller than original one.
    - Raise: Instable simulation, bigger movement
    - Reduce: Stable simulation, smaller movement
- "softening":
For both of the materials, when softening is 0.0001, which is 1/100 of the original parameter, the plant movement slightly longer than original one. Since we reduces the stiffness of the material response and leads to softer deformation and less rebound, we observe that the velocity decreases slower, which explain why the movement sustains longer and bends more significantly.
    - Raise: Stiffer material, smaller movement
    - Reduce: Softer material, bigger movement
### Bonus
- First, I will have some suspect vide of object with different material as baseline. Then, I will use a model to train these given parameters corresponding to given material. Use psnr of output video as loss. 
### Video Link
- https://youtu.be/NhrALTmRiYk
# Reference
```bibtex
@inproceedings{xie2024physgaussian,
    title     = {Physgaussian: Physics-integrated 3d gaussians for generative dynamics},
    author    = {Xie, Tianyi and Zong, Zeshun and Qiu, Yuxing and Li, Xuan and Feng, Yutao and Yang, Yin and Jiang, Chenfanfu},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
    year      = {2024}
}
```
