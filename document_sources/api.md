# Coding with Python via RPC & API
  EYED は、RPC を利用して捜査を行うことが可能です。CLI も RPCのインタフェースを
利用しているためコマンドから出来ることは、全て RPC を利用することで実現が可能です。

## EYED への 接続を行う
```python
client = RPCClient(host, port)

interfaces = client.getNetworkInterfaces()
for interface in interfaces:
	name = interface['name']
	ipv4 = interface['ipv4']
	click.echo('%s %s' %(name, ipv4))
```

