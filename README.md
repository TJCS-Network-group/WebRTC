# WebRTC

`建议在同一台服务器上开不同repo协同编辑，可以用不同端口`

阻止main.py更新即可（当然，端口这种东西其实应该放配置文件）

```
git update-index --assume-unchanged main.py
```

如果需要恢复对文件的版本控制，执行以下操作

```
git update-index --no-assume-unchanged main.py
```