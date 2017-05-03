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
    ├── push_notification.py                ## code for sending push notifications         
    ├── pi_surveillance.py                   ## camera control script
    └── server.py                           ## code for server
```
