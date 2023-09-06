## 基于yolov5的apex自瞄辅助

#### 环境准备：

 `pip install -r ./requirements.txt` 

或者 `pip install -r ./requiremens.txt -i http://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com` 

第二个为挂国内代理安装，建议先安装好cuda和pytorch之后再来安装requirements，cuda老版本安装的地址----> https://developer.nvidia.com/cuda-toolkit-archive 这个比较难找

#### 运行：

终端输入，`python -m apex-yolov5.main` 

使用终端跑不占用资源，使用pycharm跑需要改一些import路径

本人环境(MyDevice)：

| 显卡(GPU) | 1660ti      |
| ------- | ----------- |
| cuda    | v11.2       |
| python  | 3.9.9       |
| pytorch | 1.8.2+cu111 |
|         |             |

最好的模型：apex2.pt，那个apex.pt 也可以用一用。AI辅助打起来会让你去适应它，会有很强的自瞄效果，打不过内存挂，会让有一定基础的玩家如虎添翼，但是打多了之后，如果不用自瞄，水平会直接回到新人水平，在高端局，用着自瞄，局限性很大，只能说这个辅助仅做学习交流，很多时候只会毁掉自己的游戏技术，兴趣。

按住第一个侧键即可打开自瞄锁定，也可以修改代码将自瞄设置为按下左键或右键。有时候会出现游戏内按下侧键不锁定的情况，请以管理员权限运行脚本

![](example.gif)

### todo

- [x] 平滑输入
- [x] 腰射锁定
- [x] 赫姆洛克点射锁定


