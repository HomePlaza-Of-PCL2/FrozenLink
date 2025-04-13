# FrozenLink 蓝冰链接 - 为你的服务器创建面板，不出启动器即可实时监测服务器状态

***该项目为 PCL2 服务器监测面板，服务群体：服主以及服务器管理员。***
#### 预览图

![image](https://github.com/user-attachments/assets/e67cc580-08a9-4b9e-963a-7fa4363aeef9)

------

### 环境需求
+ python >= 3.7.2

### 部署
1. 下载 app.py 文件并 cd 到文件目录
2. 运行`python -m pip install requests`安装依赖
3. 运行`echo. > config.json`（`Windows`）或`touch config.json`（Linux or MacOS）生成默认配置文件
4. 打开 config.json 输入以下配置 （***注意：下方未提起的配置项请不要随意修改***）  
（获取apikey的方法请见[文档](https://docs.mcsmanager.com/zh_cn/apis/get_apikey.html)）
  ```
{
    "ip": "<面板的 IP 地址（包含协议）>",
    "apikey": "<面板的 apiKey（参加上方说明）>",
    "debug": <调试模式开关（选填 true/false）>,
    "serverConfig": {
        "serverName": "<服务器名称>",
        "serverIP": "<服务器 IP 地址>",
        "serverPORT": "<服务器端口>"
    }
}
  ```  
5. 运行
```
python app.py
```


----
### 注意事项  
该项目的mc服务器状态API使用的是 ***https://api.mcsrvstat.us/*** 如果出现主页响应缓慢可能是 api 的锅 qwq

快捷加入服务器启动的是当前选择的版本 ***（本来是想做成启动对应版本的，但是没法通配指定版本。比如你想玩1.21.1的生电服你肯定是要启动带有辅助mod的版本，而我没办法帮你选择带有辅助模组的版本，只能帮你启动1.21.1原版。所以这个功能被我砍掉了，但是服务器信息卡片上会显示服务器版本）***  

这个 repo 于原 iceLink 不同，并 ***没有管理端与客户端的区别*** ，因为 FrozenLink 的设计初衷是让 ***服务器的管理员*** 可以实时监测服务器状态，而不是普通玩家。

### 鸣谢
YuShanNan
https://github.com/YuShanNan/ChiLing-HomePage-PCL2  
Light-Beacon
https://github.com/Light-Beacon/PCL2-NewsHomepage


### 声明


该项目使用 CC BY-NC-SA 4.0 协议


项目灵感提供者以及`iceLink`冰点链接作者：icelly_QAQ 
本项目作者：CreeperIsASpy / 仿生猫梦见苦力怕
