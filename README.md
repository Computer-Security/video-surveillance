# video-surveillance

### Code Structure
```
.
├── Pi-Spy-iOS                              ## ios client side code
│   ├── Pi-Spy
│   │   ├── ...
└── Server                                  ## server (raspberry pi) side code
    ├── CertificatesPush.pem                ## certificate for push notification
    ├── key.pem
    ├── dbuser.py                           ## user model in database
    ├── user.py 
    ├── device_token                        ## ios device token
    ├── push_notification.py                ## code for sending push notifications                 
    └── server.py                           ## code for server
```
