This distributed system stores key-value pair according to the length of the key. 
There are 3 nodes and the system is scalable to any number of nodes. <br/>

These are the following steps to start the application :- <br/>
1) Setup kafka either in local or run kafka in docker( go to kafka docker and follow the instruction or you can visit `https://github.com/wurstmeister/kafka-docker`)
2) Go to nodes folder and follow the instructions to setup nodes.
3) Start you Flask application by running command `python3 app.py`.

After completing all the steps:-
1) Request `http://localhost:5000/insert` with data = {"key":" ", "value":" "}
2) Request `http://localhost:5000/get_items` with data = {"key": " "}


