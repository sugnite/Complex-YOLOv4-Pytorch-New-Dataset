# Complex YOLOv4

[![python-image]][python-url]
[![pytorch-image]][pytorch-url]

The PyTorch Implementation based on YOLOv4 of the paper: [Complex-YOLO: Real-time 3D Object Detection on Point Clouds](https://arxiv.org/pdf/1803.06199.pdf)

---

## Demo

![demo](./docs/demo_yolov3.gif)

## Features
- [x] Realtime 3D object detection based on YOLOv4
- [x] [Distributed Data Parallel Training](https://github.com/pytorch/examples/tree/master/distributed/ddp)
- [x] TensorboardX
- [ ] Tried to use [CIoU](https://arxiv.org/pdf/1911.08287.pdf) / [GIoU](https://arxiv.org/pdf/1902.09630v2.pdf) loss function.

## 2. Getting Started
### 2.1. Requirement

```shell script
pip install -U -r requirements.txt
```

For [`mayavi`](https://docs.enthought.com/mayavi/mayavi/installation.html) and [`shapely`](https://shapely.readthedocs.io/en/latest/project.html#installing-shapely) 
libraries, please refer to the installation instructions from their official websites.


### 2.2. Data Preparation
Download the 3D KITTI detection dataset from [here](http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d).

The downloaded data includes:

- Velodyne point clouds _**(29 GB)**_: input data to VoxelNet
- Training labels of object data set _**(5 MB)**_: input label to VoxelNet
- Camera calibration matrices of object data set _**(16 MB)**_: for visualization of predictions
- Left color images of object data set _**(12 GB)**_: for visualization of predictions

Please make sure that you construct the source code & dataset directories structure below.

For 3D point cloud preprocessing, please refer to the previous works:
- [VoxelNet-Pytorch](https://github.com/skyhehe123/VoxelNet-pytorch)
- [Complex-YOLOv3](https://github.com/ghimiredhikura/Complex-YOLOv3)
- [Complex-YOLOv2](https://github.com/AI-liu/Complex-YOLO)


### 2.3. Complex-YOLO architecture

![architecture](./docs/complex_yolo_architecture.PNG)

This work has been based on YOLOv4 for 2D object detection. Please refer to [the original paper of YOLOv4](https://arxiv.org/abs/2004.10934) 
and [the Pytorch implementation](https://github.com/Tianxiaomo/pytorch-YOLOv4) which is the great work from *Tianxiaomo*

### 2.4. How to run

#### 2.4.1. Visualize the dataset (both BEV images from LiDAR and camera images)

```shell script
cd src/data_process
python kitti_dataloader.py --batch_size 1 --num_workers 1
```

#### 2.4.2. Inference

```shell script
python test.py --gpu_idx 0
```

#### 2.4.3. Training

##### 2.4.3.1. Single machine, single gpu

```shell script
python train.py --gpu_idx 0
```

##### 2.4.3.2. Multi-processing Distributed Data Parallel Training
We should always use the `nccl` backend for multi-processing distributed training since it currently provides the best 
distributed training performance.

- **Single machine (node), multiple GPUs**

```shell script
python train.py --dist-url 'tcp://127.0.0.1:29500' --dist-backend 'nccl' --multiprocessing-distributed --world-size 1 --rank 0
```

- **Two machines (two nodes), multiple GPUs**

_**First machine**_

```shell script
python train.py --dist-url 'tcp://IP_OF_NODE1:FREEPORT' --dist-backend 'nccl' --multiprocessing-distributed --world-size 2 --rank 0
```
_**Second machine**_

```shell script
python train.py --dist-url 'tcp://IP_OF_NODE2:FREEPORT' --dist-backend 'nccl' --multiprocessing-distributed --world-size 2 --rank 1
```

To reproduce the results, you can run the bash shell script

```bash
./train.sh
```

## Contact

If you think this work is useful, please give me a star! <br>
If you find any errors or have any suggestions, please contact me (**Email:** `nguyenmaudung93.kstn@gmail.com`). <br>
Thank you!


## Citation

```bash
@article{Complex-YOLO,
  author = {Martin Simon, Stefan Milz, Karl Amende, Horst-Michael Gross},
  title = {Complex-YOLO: Real-time 3D Object Detection on Point Clouds},
  year = {2018},
  journal = {arXiv},
}

@article{YOLOv4,
  author = {Alexey Bochkovskiy, Chien-Yao Wang, Hong-Yuan Mark Liao},
  title = {YOLOv4: Optimal Speed and Accuracy of Object Detection},
  year = {2020},
  journal = {arXiv},
}
```


## Folder structure

```
${ROOT}   
└── dataset/    
    └── kitti
        ├── training
        |   ├── image_2 <-- for visualization
        |   ├── calib
        |   ├── label_2
        |   ├── velodyne
        └── testing  
        |   ├── image_2 <-- for visualization
        |   ├── calib
        |   ├── velodyne 
└── src/
    └── config/
    └── data_process/
    └── models/
    └── utils/
    └── demo.py
    └── test.py
    └── train.py
    └── train.sh
├── README.md 
├── requirements.txt
```

## Usage

```
usage: train.py [-h] [--seed SEED] [--saved_fn FN] [-a ARCH] [--cfgfile PATH]
                [--pretrained_path PATH] [--img_size IMG_SIZE]
                [--multiscale_training] [--no-val] [--num_samples NUM_SAMPLES]
                [--num_workers NUM_WORKERS] [--batch_size BATCH_SIZE]
                [--subdivisions SUBDIVISIONS] [--print_freq N]
                [--tensorboard_freq N] [--checkpoint_freq N] [--start_epoch N]
                [--num_epochs N] [--lr LR] [--minimum_lr MIN_LR]
                [--momentum M] [-wd WD] [--optimizer_type OPTIMIZER]
                [--lr_type SCHEDULER] [--burn_in N]
                [--steps [STEPS [STEPS ...]]] [--world-size N] [--rank N]
                [--dist-url DIST_URL] [--dist-backend DIST_BACKEND]
                [--gpu_idx GPU_IDX] [--no_cuda]
                [--multiprocessing-distributed] [--evaluate]
                [--resume_path PATH]

The Implementation of Complex YOLOv4

optional arguments:
  -h, --help            show this help message and exit
  --seed SEED           re-produce the results with seed random
  --saved_fn FN         The name using for saving logs, models,...
  -a ARCH, --arch ARCH  The name of the model architecture
  --cfgfile PATH        The path for cfgfile (only for darknet)
  --pretrained_path PATH
                        the path of the pretrained checkpoint
  --img_size IMG_SIZE   the size of input image
  --multiscale_training
                        If true, use scaling data for training
  --no-val              If true, dont evaluate the model on the val set
  --num_samples NUM_SAMPLES
                        Take a subset of the dataset to run and debug
  --num_workers NUM_WORKERS
                        Number of threads for loading data
  --batch_size BATCH_SIZE
                        mini-batch size (default: 64), this is the totalbatch
                        size of all GPUs on the current node when usingData
                        Parallel or Distributed Data Parallel
  --subdivisions SUBDIVISIONS
                        subdivisions during training
  --print_freq N        print frequency (default: 10)
  --tensorboard_freq N  frequency of saving tensorboard (default: 10)
  --checkpoint_freq N   frequency of saving checkpoints (default: 3)
  --start_epoch N       the starting epoch
  --num_epochs N        number of total epochs to run
  --lr LR               initial learning rate
  --minimum_lr MIN_LR   minimum learning rate during training
  --momentum M          momentum
  -wd WD, --weight_decay WD
                        weight decay (default: 1e-6)
  --optimizer_type OPTIMIZER
                        the type of optimizer, it can be sgd or adam
  --lr_type SCHEDULER   the type of the learning rate scheduler (steplr or
                        ReduceonPlateau)
  --burn_in N           number of burn in step
  --steps [STEPS [STEPS ...]]
                        number of burn in step
  --world-size N        number of nodes for distributed training
  --rank N              node rank for distributed training
  --dist-url DIST_URL   url used to set up distributed training
  --dist-backend DIST_BACKEND
                        distributed backend
  --gpu_idx GPU_IDX     GPU index to use.
  --no_cuda             If true, cuda is not used.
  --multiprocessing-distributed
                        Use multi-processing distributed training to launch N
                        processes per node, which has N GPUs. This is the
                        fastest way to use PyTorch for either single node or
                        multi node data parallel training
  --evaluate            only evaluate the model, not training
  --resume_path PATH    the path of the resumed checkpoint
```

[python-image]: https://img.shields.io/badge/Python-3.x-ff69b4.svg
[python-url]: https://www.python.org/
[pytorch-image]: https://img.shields.io/badge/PyTorch-1.5-2BAF2B.svg
[pytorch-url]: https://pytorch.org/