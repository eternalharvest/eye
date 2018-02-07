# EYE
 EYE is a developped for monitoring agent for distributed enviroment

# Supported Protocol
- ICMP
- BACnet

# Install EYED
  You can easily install EYED by pip command from Github repositry.

```python
pip install git+https://github.com/ThousandMileEye/eye.git
```

# How to use?
  After execute pip, you can launch EYED RPC Server by eye commad.

```bash
eyed
```

## Check the system settings.
### Check Network Interfaces
```bash
(eye) $ eye show interfaces
lo0 [{'peer': u'127.0.0.1', 'netmask': u'255.0.0.0', 'addr': u'127.0.0.1'}]
~ 省略 ~
```

### Start bacnetd
```bash
(eye) $ eye start bacnetd [interface-name]
```

# Manage eyed as a service
  If you would like to use eyed as a service, You can use supervisor daemon.
Supervisor is a quite useful tool for mange python services as a daemon.
You can install supervisord by apt or yum command.

```bash
sudo apt-get install supervisor
```

  Following command is a example for register and start eyed as a service on the supervisord.
```
supervisorctl add eyed
supervisorctl start eyed
```

