# IoT-Chain
Internet of Things, more generally referred to as ‘IoT’ among the masses is the next major step towards achieving sustainable absolute automaton and advancing in the field of assistive technology to control menial chore. Electronic devices are connected over a network with these devices being able to communicate with each other. This forms the basic structure of IoT.  
Traditional IoT architecture can be considered to be centralized to a comparable extent. The data that is collected as a result of provision of services to the users is stored in central servers which are managed by influential groups or corporations. This leaves the data prone to misuse and theft.  
IoT chain is a lite server side application layer for IoT devices . This application layer provides a way for
generalization of architecture to achieve swift integration. It is based majorly on Blockchain technology. Decentralization is at the forefront of any innovation that takes this forward. Using blockchain, the data which is collected by virtue of users using the services is stored in a a decentralized form where no single person or group has access to all the data and even if they do have access it is immutable. This increases security. IoT chain adopts certain technical algorithms to work on blockchain, these novel algorithms make it unique and safe operating system for IoT centered machinery.   

  
 ### Technical Details:
  <ul>
  <li><b> PBFT </b>  </li> 
   BFT or the Byzantine fault tolerance is a feature that arises in distributed systems such as a blockchain based network when the system is able to reach a consensus (i.e. to approve a transaction) even when a few nodes do not respond to the particular course of action. There are various methods proposed to handle this in distributed systems. The PBFT or Practical Byzantine Fault tolerance is a state machine replication algorithm which bases itself on the regularity of message passing. It has three basic stages, namely ‘pre-prepare’, ‘prepare’ and ‘confirm’. If the total number of nodes in a particular network is ‘N’, then the PBFT algorithm is able to deliver a fault tolerance of (N-1)/3. It is a consensus algorithm; different consensus algorithms are deemed to create different performance and IoT chain uses PBFT. Blockchain based on PBFT consensus algorithm has already been applied in various commercial and public products worldwide. Some of these include a digital currency project by the Central Bank of China, Bumeng Blockchain and IBM’s hyperledger. By adhering to PBFT consensus, IoT chain has improved performance by carefully striking the balance between extensibility and performance needs by adjusting nodal weights   
  <li><b> DAG </b> </li>
   Blockchain’s linked-list type data structure is facing a lot of issues as number of users expand. It is increasing transaction fees in case of certain decentralized currencies and reducing the overall performance. IoT chain uses a DAG type of topological structure which is short for Directed Acyclic Graph. DAG changes the generically used longest-chain consensus to heaviest-chain consensus which solves the problem of emerging centralization in blockchain, binding proof of work with each transaction that is approved in a skillful manner. Using DAG, we are able to improve the throughput capacity of the network, lowering transaction costs. 
</ul>   

 Smart IoT devices which can carry a group of tasks replacing a human have given rise to terminologies such as a ‘Cyber  Physical system’ or a CPS. It is basically integration of IoT with a platform for intelligent analysis of the system. CPS can be considered as a more advanced IoT which is able to compute big chunks of information and do tasks in which traditional IoT systems might be render themselves unable.  

IoT chain’s reliability can be understood clearly by taking a simple example. Creating an analogy, let us assume a GPS system. Now, certain intrinsic features of this GPS system is that it is a network in the first place, this network has a lot of users using it i.e. mobile devices connected to it. Satellites orbiting the Earth are constantly sending out information about the location to the devices. This information transfer between the devices and the satellite can be considered as a transaction. The Satellite can be considered as a central device and user’s GPS enabled phones to be secondary devices. Whenever a transaction or an information transfer occurs, the data is exchanged and IoT chain’s blockchain infrastructure helps to secure the data transfer. This is done by defining data with hash codes and not by generic codes. Location data of one user should not be available to any other user on the network for privacy concerns, IoT chain’s security features help in achieving the same goal.  

 IoT chain aims at an architecture where a network works on different levels not based on user hierarchy but on connectivity and the type of processing which is done on each level. Such system architecture is portable to be used across various devices. This can greatly increase the stability of the IoT ecosystem and make it more intelligent. 

   


## Quick Setup:

Code to clone and break reference:
```bash
git clone https://github.com/InfoScienceLabs/IoT-Chain
cd IoT-Chain
rm -rf .git
```

Code to install Flask (only necessary once):
```bash
pip3 install flask
```

Code to configure your flask app (you may need to set these once each time you open a new terminal):
```bash
export FLASK_APP=main.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8080
export FLASK_DEBUG=1
```

Code to run flask:
```bash
flask run
```

**If you're developing in the cs50 IDE, ignore this next part.**
If you're developing locally, you can probably save time on the environment variables, by installing the [python-dotenv](https://pypi.org/project/python-dotenv/) package, which automatically loads the settings we're currently setting with `export`:
```bash
pip3 install python-dotenv
```

If that installation works, you should be able to create a file called `.env` and add the `export` statements above to it, that way these configurations won't need to be made every time. 

[troubleshooting](#troubleshooting-package-installation)

## Virtual Environments (optional)

If you're running this locally, you will likely want to run this program inside a virtual environment - that way changes to your Python configuration don't persist and impact other Python programs on your machine. If you're running this program in a remote environment like Cloud Shell, Cloud9, or cs50, adding a virtual environment within those containers may complicate things more than helping them. 

To create a virtual environment (you only need to do this once), run this code in terminal:
```bash
python3 -m venv venv
```

To ENTER your virtual environment (you'll need to do this every time you open up a new terminal), run this code:
```bash
. venv/bin/activate
```

To EXIT your virtual environment (you'll want to do this if you decide to change projects - think of it like shutting this one down), you just need one word:
```bash
deactivate
```

If you're using a virtual environment like Codenvy, the virtual environment produces more problems than it solves, so consider skipping this step.

## Python packages

To start, the only package you need to run is `flask` for (hopefully) obvious reasons.

To install flask, run this code in terminal.
```bash
pip3 install flask
```
Remember, if you're using a virtual environment, these packages will only be installed IN the virtual environment (which is part of why we don't recommend it in cs50 where we won't need it - students will accidentally forget where they've configured different settings).

### Troubleshooting package installation

If your IDE throws errors on either of these commands saying that you aren't authorized, your account may not be authorized to install packages on the IDE you're using. There are two ways to work around this. The first is by adding the user flag:
```bash
pip3 install --user flask
```
The other way around this is to try adding the 'switch user and do' command ('sudo' for short):
```bash
sudo pip3 install flask
```


The settings will not be stored between sessions, so every time you open a new terminal, you'll need to run these commands, which are stored in the `run-variables.md` file for your convenience:
```bash
export FLASK_APP=main.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8080
export FLASK_DEBUG=1
```

After that you should be able to execute the `flask run` command normally.

## Authors

* **INFO SCIENCE LABS** - *Initial work* - [Info Science Lab](https://github.com/Infosciencelabs)

See also the list of [contributors](https://github.com/Infosciencelabsdev/Garuda/graphs/contributors) who participated in this project.
## Contact Us
  Email:- info@infoscience.co
## License
This project is licensed under the Apache License- see the [LICENSE](LICENSE) file for details


