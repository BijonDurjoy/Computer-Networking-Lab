# Socket Programming with TCP
In this assignment, our main task is:

- Two people can chat with each other. One person can send one or multiple texts back-to-back without waiting for a reply.
- A file server and client. The client can list, store, delete, and download files from the file server.

# Output
- Create a TCP server ![Alt text](https://github.com/BijonDurjoy/Computer-Networking-Lab/blob/9ef7c4b4ebfc70057da687acbfce346634198d14/Socket%20Programming/Images/Screenshot%20from%202025-08-10%2021-08-13.png)
-Chating with another client simonteniously with TCP server:

**Person 1:**
 ![Alt text](https://github.com/BijonDurjoy/Computer-Networking-Lab/blob/9ef7c4b4ebfc70057da687acbfce346634198d14/Socket%20Programming/Images/Screenshot%20from%202025-08-10%2021-08-44.png)
 
**Person 2:**
![Alt Text](https://github.com/BijonDurjoy/Computer-Networking-Lab/blob/9ef7c4b4ebfc70057da687acbfce346634198d14/Socket%20Programming/Images/Screenshot%20from%202025-08-10%2021-09-00.png)

- Send a file to the server by Person 2:
![Alt Text](https://github.com/BijonDurjoy/Computer-Networking-Lab/blob/9ef7c4b4ebfc70057da687acbfce346634198d14/Socket%20Programming/Images/Screenshot%20from%202025-08-10%2021-10-14.png) <br>
In this part Person 2 send a .txt file to the server.


![Alt Text](https://github.com/BijonDurjoy/Computer-Networking-Lab/blob/9ef7c4b4ebfc70057da687acbfce346634198d14/Socket%20Programming/Images/Screenshot%20from%202025-08-10%2021-11-19.png) <br>
Here, Person 1 downloads the file from the server. So both of them can also share files via TCP server

- It is the file structure. where folder server_file contains all the file that are uploaded on the server. and the donloaded file will be situated on the main folder.
![Alt Text](https://github.com/BijonDurjoy/Computer-Networking-Lab/blob/9ef7c4b4ebfc70057da687acbfce346634198d14/Socket%20Programming/Images/Screenshot%20from%202025-08-10%2021-11-31.png)
