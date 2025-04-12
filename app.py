import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
from math import floor


HOMEPAGE = '''
<StackPanel.Resources>
    <SolidColorBrush x:Key="IconBrush" Color="#4A90E2"/>
    
    <Style x:Key="AnimatedPathStyle" TargetType="Path">
        <Setter Property="RenderTransformOrigin" Value="0.5,0.5"/>
        <Setter Property="RenderTransform">
            <Setter.Value>
                <RotateTransform Angle="0"/>
            </Setter.Value>
        </Setter>
        <Style.Triggers>
            <EventTrigger RoutedEvent="MouseLeftButtonDown">
                <BeginStoryboard>
                    <Storyboard>
                        <DoubleAnimation 
                            Storyboard.TargetProperty="(Path.RenderTransform).(RotateTransform.Angle)"
                            From="0" To="360" Duration="0:0:0.5"/>
                    </Storyboard>
                </BeginStoryboard>
            </EventTrigger>
        </Style.Triggers>
    </Style>
</StackPanel.Resources>
 
<local:MyCard Margin="0,0,0,0">
    <TextBlock Text="%(ServerName)s"
        HorizontalAlignment="Left" 
        FontSize="20" 
        FontFamily="Microsoft Yahei Ui"
        Margin="12,12,12,12"
        FontWeight="Bold"/>
    <TextBlock Text="使用 iceLink 主页 v0.1.5 版本创建"
        HorizontalAlignment="Left" 
        FontSize="16" 
        Margin="80,14,12,12"/>
    <TextBlock Text="给 iceLink 点个 star 吧~"
        Foreground="{DynamicResource ColorBrush2}"
        HorizontalAlignment="Right" 
        FontSize="16" 
        Margin="12,12,50,12"/>
    <local:MyIconButton 
        Margin="0,10,15,10" 
        Width="15" 
        Height="15" 
        HorizontalAlignment="Right" 
        ToolTip="刷新" 
        EventType="刷新主页">
        <Path 
            Stretch="Uniform"
            Width="15" 
            Height="15" 
            Style="{StaticResource AnimatedPathStyle}"
            Data="M960 416V192l-73.056 73.056a447.712 447.712 0 0 0-373.6-201.088C265.92 63.968 65.312 264.544 65.312 512S265.92 960.032 513.344 960.032a448.064 448.064 0 0 0 415.232-279.488 38.368 38.368 0 1 0-71.136-28.896 371.36 371.36 0 0 1-344.096 231.584C308.32 883.232 142.112 717.024 142.112 512S308.32 140.768 513.344 140.768c132.448 0 251.936 70.08 318.016 179.84L736 416h224z"             
            Fill="{StaticResource IconBrush}"/>
    </local:MyIconButton>
</local:MyCard>



<local:MyCard Title="MC服务器信息" Margin="0,64,0,15">
    <Grid>
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="*"/>
            <ColumnDefinition Width="Auto"/>
        </Grid.ColumnDefinitions>
        
        <StackPanel Grid.Column="0">
            <TextBlock 
                Text="%(ServerName)s"
                FontSize="18"
                FontWeight="Bold"
                HorizontalAlignment="Left"
                VerticalAlignment="Top"
                Margin="18,30,0,15"/>  
            <TextBlock 
                Text="服务器版本：%(ProtocolName)s"
                FontSize="18"
                FontWeight="Bold"
                HorizontalAlignment="Left"
                VerticalAlignment="Top"
                Margin="18,0,88,15"/>
            <TextBlock 
                Text="在线玩家：%(PlayerCountString)s"
                FontSize="18"
                FontWeight="Bold"
                HorizontalAlignment="Left"
                VerticalAlignment="Top"
                Margin="18,0,15,15"/>
        </StackPanel>
        
        <StackPanel Grid.Column="1" VerticalAlignment="Center" Margin="0,22,15,0">
            <local:MyButton 
                Text="加入服务器" 
                Margin="0,0,15,8" 
                EventType="启动游戏" 
                EventData="\current|%(ServerIP)s" 
                ToolTip="将会以当前版本加入 %(ServerIP)s" 
                Height="35" 
                Width="80"/>
            <local:MyButton 
                Text="复制地址" 
                Margin="0,8,15,0" 
                EventType="复制文本" 
                EventData="%(ServerIP)s" 
                ToolTip="复制服务器地址" 
                Height="35" 
                Width="80"/>
        </StackPanel>
    </Grid>
</local:MyCard>


<local:MyCard Title="仪表盘" Margin="0,0,0,15">
    <Grid Margin="15,0,15,15">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/> <!-- 第一行 -->
            <RowDefinition Height="*"/> <!-- 第二行 -->
        </Grid.RowDefinitions>
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="*"/> <!-- 第一列 -->
            <ColumnDefinition Width="15"/> <!-- 分隔列（可选） -->
            <ColumnDefinition Width="*"/> <!-- 第二列 -->
        </Grid.ColumnDefinitions>

        <!-- 左上区块 -->
        <Border Grid.Row="0" Grid.Column="0" Margin="0,35,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock Text="实例运行状态" 
                    FontSize="16" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <TextBlock Text="正在运行数 / 全部实例总数" 
                    FontSize="10" 
                    Margin="16,5,5,0"
                    Foreground="#666666"
                    FontWeight="Bold"/>
                <TextBlock 
                    Text="%(RunningInstances)s / %(TotalInstances)s"
                    FontSize="30"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"/>
            </StackPanel>
        </Border>

        <!-- 右上区块 -->
        <Border Grid.Row="0" Grid.Column="2" Margin="0,35,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock Text="节点在线数" 
                    FontSize="16" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <TextBlock Text="在线节点 / 总节点" 
                    FontSize="10" 
                    Margin="16,5,5,0"
                    Foreground="#666666"
                    FontWeight="Bold"/>
                <TextBlock 
                    Text="%(RunningNodes)s / %(TotalNodes)s"
                    FontSize="30"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"/>
            </StackPanel>
        </Border>

        <!-- 左下区块 -->
        <Border Grid.Row="1" Grid.Column="0" Margin="0,15,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock Text="系统资源信息" 
                    FontSize="16" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <TextBlock Text="面板主机 CPU，RAM 使用率" 
                    FontSize="10" 
                    Margin="16,5,5,0"
                    Foreground="#666666"
                    FontWeight="Bold"/>
                <TextBlock 
                    Text="%(CPUUsage)s% %(RAMUsage)s%"
                    FontSize="30"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"/>
            </StackPanel>
        </Border>

        <!-- 右下区块 -->
        <Border Grid.Row="1" Grid.Column="2" Margin="0,15,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock Text="面板登录次数" 
                    FontSize="16" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <TextBlock Text="登录失败次数 : 登录成功次数" 
                    FontSize="10" 
                    Margin="16,5,5,0"
                    Foreground="#666666"
                    FontWeight="Bold"/>
                <TextBlock 
                    Text="%(FailedLogin)s : %(TotalLogin)s"
                    FontSize="30"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"/>
            </StackPanel>
        </Border>
    </Grid>
</local:MyCard>

<local:MyCard Title="主节点：%(NodeName)s" Margin="0,0,0,15">
    <Grid Margin="15,0,15,15">
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="*"/> <!-- 第一列 -->
            <ColumnDefinition Width="15"/> <!-- 分隔列 -->
            <ColumnDefinition Width="*"/> <!-- 第二列 -->
        </Grid.ColumnDefinitions>

        <!-- 左侧区块 -->
        <Border Grid.Column="0" Margin="0,35,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock 
                    Text="节点地址" 
                    FontSize="13" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <local:MyTextButton 
                    Text="%(NodeIP)s"
                    FontSize="35"
                    FontWeight="Bold"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"
                    EventType="复制文本"
                    EventData="%(NodeIP)s"
                    Foreground="#000000"/>
            </StackPanel>
        </Border>

        <!-- 右侧区块 -->
        <Border Grid.Column="2" Margin="0,35,0,0" BorderThickness="1" BorderBrush="#44000000" CornerRadius="5">
            <StackPanel>
                <TextBlock
                    Text="节点版本" 
                    FontSize="13" 
                    Margin="15,15,15,0"
                    FontWeight="Bold"/>
                <TextBlock 
                    Text="%(NodeVersion)s"
                    FontSize="15"
                    FontWeight="Bold"
                    HorizontalAlignment="Center"
                    VerticalAlignment="Top"
                    Margin="0,15,0,15"/>
            </StackPanel>
        </Border>
    </Grid>
</local:MyCard>

<StackPanel Orientation="Horizontal" HorizontalAlignment="Center" Margin="0,0,0,15">
    <local:MyTextButton Text="iceLink" EventType="打开网页" EventData="https://github.com/icelly-QAQ/PCL2-HomePage_iceLink" FontSize="12" Foreground="#666666"/>
    <TextBlock Text=" By " Foreground="#666666" FontSize="12"/>
    <local:MyTextButton Text="icelly_QAQ" EventType="打开网页" EventData="https://github.com/icelly-QAQ" FontSize="12" Foreground="#666666"/>
</StackPanel>
'''


class DataGetter:
    def __init__(self):
        with open('config.json', "r+", encoding='utf-8') as f:
            config = json.load(f)
        self.url = f"{config['ip']}/api/overview?apikey={config['apikey']}"
        self.apiurl = \
            f"https://api.mcsrvstat.us/3/{config['serverConfig']['serverIP']}:{config['serverConfig']['serverPORT']}"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = json.loads(requests.get(self.url, headers=headers).text)

        content_text = re.sub(r"(?<!%)%(?!\()", "%%", HOMEPAGE)
        svinfo = self.get_server_info()
        meta = {'ServerName': config["serverConfig"]["serverName"],
                'ProtocolName': svinfo['protocol']['name'],
                'PlayerCountString': f'{svinfo["players"]["online"]}/{svinfo["players"]["max"]}',
                'ServerIP': config["serverConfig"]["serverIP"],
                'RunningInstances': data['data']['remote'][0]['instance']['running'],
                'TotalInstances': data['data']['remote'][0]['instance']['total'],
                'RunningNodes': data['data']['remoteCount']['available'],
                'TotalNodes': data['data']['remoteCount']['total'],
                'CPUUsage': floor(data['data']['chart']['system'][3]['cpu']),
                'RAMUsage': floor(data['data']['chart']['system'][3]['mem']),
                'FailedLogin': data['data']['record']['loginFailed'],
                'TotalLogin': data['data']['record']['logined'],
                'NodeName': data['data']['remote'][0]['remarks'],
                'NodeIP': data['data']['remote'][0]['ip'],
                'NodeVersion': data['data']['remote'][0]['version']}
        content_text = content_text.replace("}", "}}").replace("{", "{{")
        self.homepage = (content_text % meta).replace("}}", "}").replace("{{", "{")
        self.write_into_file()

    def get_server_info(self):
        headers = {
            'User-Agent': 'PCL2-Home/1.0 (https://github.com/icellye/PCL2-home)',
            'Accept': 'application/json'
        }
        resp = requests.get(self.apiurl, headers=headers)
        return json.loads(resp.text)

    def print_nested_dict(self, d, indent=0):
        """递归打印嵌套字典，使用缩进增强可读性"""
        for key, value in d.items():
            # 打印当前键（带缩进）
            print(' ' * indent + f"{key}:", end=' ')

            # 处理嵌套字典或普通值
            if isinstance(value, dict):
                print()  # 换行后开始子字典
                self.print_nested_dict(value, indent + 4)  # 递归调用，增加缩进
            else:
                print(value)  # 直接打印非字典值

    def write_into_file(self):
        with open("app.xaml", "w+", encoding='utf-8') as f:
            f.write(self.homepage)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 设置响应状态码
        self.send_response(200)

        # 设置响应头（指定内容类型为纯文本）
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        # 发送响应内容（需编码为字节流）
        self.wfile.write(DataGetter().homepage.encode('utf-8'))


def run_server():
    try:
        server_address = ('', 3000)  # 侦听所有接口的8000端口
        httpd = HTTPServer(server_address, RequestHandler)
        print("Server started on port 3000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("KeyboardInterrupt accepted. Exiting")
        exit()


if __name__ == "__main__":
    run_server()
