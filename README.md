Python Trigger
====

简介
--
> * Python Trigger 是一个以 python 编写，提供基于事件回调触发其他事件的触发器框架，本身不会提供任何独立功能，但可以为你节省编写功能插件结构的时间
> * 你可以选择用任何你熟悉的语言编写插件 —— 只要最后可以对接上 python 的接口

Hello World
--
> * Python Trigger 的插件初始拥有三种事件：plugin_onload 、 plugin_onunload 和 plugin_start，继承 FFxivPythonTrigger.PluginBase 实现
> 
> 事件 | 用处 
> --- |:---:
> plugin_onload| 插件初始化（不建议使用__init__作为初始化）
> plugin_start | 成功初始化后开始运行插件逻辑（一般用于挂起进程）（需要以async模式编写）
> plugin_onunload| 插件卸载（关闭运行进程，清理、储存资料）
> * 同时请设定插件的name作为插件识别用途
> * 请注意，在plugin_onload中挂起的进程可能造成堵塞其他插件初始化或是主进程将不会等待其完结便结束，因此长期维持的线程建议用plugin_start 进行操作
* 透过PluginBase的 FPT 属性，可以访问框架提供的一些便利功能

> * 为提供插件间功能的互通，提供插件层面的api注册与使用
> * self.FPT.api：
> 
> 函数| 用处 
> --- |:---:
> register_attribute(name:string,object:any)| 注册api，让其他程序可以进行调用
> * 在创建后，其他插件即可透过'self.FPT.api.注册名字'访问该object
> * 透过该方法注册的api将会在插件卸载后同时卸载

> * 为提供插件数据的持久化，提供storage方法进行规范化的储存方式
> * self.FPT.storage：
> 
> 函数、变量| 用处 
> --- |:---:
> data| 持久化储存实体，dict属性
> path| 插件分配的文件夹路径
> > load()| 将json数据加载至data（加载插件时自动调用）
> store()| 将data的数据json 处理后进行储存 (插件卸载自动调用）

> * 为对程序的输出进行规范化，提供log函数
> * self.FPT：
> 
> 函数| 用处 
> --- |:---:
> log(msg:string,level:number=logging.info)| 列印在等级logger 的 print_level 或以上的log(默认为logging.info)并且写进log文件（好像还没写）

> * 插件功能大体上可以分为两种 ： 一，创建事件、二，响应事件
> * self.FPT：
> 
> 函数| 用处 
> --- |:---:
> process_event(event:FFxivPythonTrigger.EventBase)| 传入一个事件object，透过事件的id属性进行分发
> register_event(event_id:any, callback:callable)| 注册一个该事件id的回调，回调将传入该事件object，建议为async function
> * 注册的事件回调将会在插件卸载后同时卸载
