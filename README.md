# Quarto Multinode using SocketIO
Server and Client implementation of Quarto game using SocketIo library.


The following instructions help you set up your environment for the
project.

I highly and strongly recommend that you do it *the virtual environment
way*.
 
## **Description**:

In this two-player game two users can play over a local network.
This project consists of two nodes (clients, players) and a server. The
server is responsible for managing the game and passing data between
nodes as the players take their turn playing the game.
These two nodes connect to the server using sockets. (which I will
discuss later).
There are two main points in this project.
 1. writing a fully functional turn-based two-player game,
 2. separating the game into two nodes, and connecting them to the
 server through sockets


The game is played on a 4×4 board. There are 16 unique pieces to play
with, each of which is either:
    - tall or short
    - black or white
    - square or circular
    - hollow-top or solid-top
Players take turns choosing a piece which the other player must then
place on the board. A player wins by placing a piece on the board which
forms a horizontal, vertical, or diagonal row of four pieces, all of which
have a common attribute (all short, all circular, etc.).

## **Screenshots**:

<table>
 <tr>
  <td><img src="https://github.com/user-attachments/assets/bd9b4da4-828a-4219-9221-f377b293d5e8"></td>
 </tr>
 <tr>
  <td><img src="https://github.com/user-attachments/assets/a9ba41a3-d6af-4258-93a6-0f8297f21d58"></td>
 </tr>
</table>

## **Building**:

### **Windows (the virtual environment way)**

Open `cmd`or `powershell` in the folder which `server.py` and
`client.py`are in:

-   open the directory and hold `SHIFT` button and `Right-Click` . then
    you must see the option `Open command window here` or
    `Open PowerShell here`.
-   In **Windows 11** hold `SHIFT` button and press `RightClick`. While
    holding `SHIFT` click on `Show more options`. then you must see the
    option `Open command window here` or `Open PowerShell here`.

Install `virtualenv` package using `pip`:

``` {.md-fences .md-end-block .ty-contain-cm .modeLoaded spellcheck="false" lang="shell"}
pip3 install virtualenv
```

Create a `virtual environment` named `quarto_venv`:

``` {.CodeMirror-line role="presentation"}
virtualenv quarto_venv
```

activate your newly created `virtualenvironment`:

``` {.md-fences .md-end-block .ty-contain-cm .modeLoaded spellcheck="false" lang="powershell"}
.\quarto_venv\Scripts\activate
```

-   **note**: If you\'re using `powershell` and got an error about
    `PSSecurityException` execute the following command and execute the
    above command again.

    ``` {.md-fences .md-end-block .ty-contain-cm .modeLoaded lang="powershell" spellcheck="false"}
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
    ```

now execute following command:

``` {.CodeMirror-line role="presentation"}
pip install -r req.txt
```

the above command installs some python packages we need for this
project.

then run `server.py`:


``` {.CodeMirror-line role="presentation"}
python server.py
```

on a separate command line run `client.py`:


``` {.CodeMirror-line role="presentation"}
python client.py
```

after running `client.py` , you should see some logs like following on
`server.py` execution:


``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "GET /socket.io/?transport=polling&EIO=4&t=1639342185.6107757 HTTP/1.1" 200 243 0.000432
```

``` {.CodeMirror-line role="presentation"}
itgWKqS9A51uiinoAAAB connected!
```

``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "POST /socket.io/?transport=polling&EIO=4&sid=UEZimvolDphNpVJeAAAA HTTP/1.1" 200 143 0.001755
```

``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "GET /socket.io/?transport=polling&EIO=4&sid=UEZimvolDphNpVJeAAAA&t=1639342185.6165655 HTTP/1.1" 200 189 0.000128
```

**note**: The most important piece of log is
`itgWKqS9A51uiinoAAAB connected!` which `itgWKqS9A51uiinoAAAB` is the
socket id that defers time to time.

**You\'re good to go.**

 

### **Windows (not recommended)**

Open `cmd`or `powershell` in the folder which `server.py` and
`client.py`are in:

-   open the directory and hold `SHIFT` button and `Right-Click` . then
    you must see the option `Open command window here` or
    `Open PowerShell here`.
-   In **Windows 11** hold `SHIFT` button and press `RightClick`. While
    holding `SHIFT` click on `Show more options`. then you must see the
    option `Open command window here` or `Open PowerShell here`.

execute following command:


``` {.CodeMirror-line role="presentation"}
pip install -r req.txt
```

the above command installs some python packages we need for this
project.

then run `server.py`:


``` {.CodeMirror-line role="presentation"}
python server.py
```

on a separate terminal run `client.py`:


``` {.CodeMirror-line role="presentation"}
python client.py
```

after running `client.py` , you should see some logs like following on
`server.py` execution:


``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "GET /socket.io/?transport=polling&EIO=4&t=1639342185.6107757 HTTP/1.1" 200 243 0.000432
```

``` {.CodeMirror-line role="presentation"}
itgWKqS9A51uiinoAAAB connected!
```

``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "POST /socket.io/?transport=polling&EIO=4&sid=UEZimvolDphNpVJeAAAA HTTP/1.1" 200 143 0.001755
```

``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "GET /socket.io/?transport=polling&EIO=4&sid=UEZimvolDphNpVJeAAAA&t=1639342185.6165655 HTTP/1.1" 200 189 0.000128
```

**note**: The most important piece of log is
`itgWKqS9A51uiinoAAAB connected!` which `itgWKqS9A51uiinoAAAB` is the
socket id that defers time to time.

**You\'re good to go.**

 
### **Linux (the virtual environment way)**

Open a terminal in the directory which `server.py` and `client.py`are in
and install `virtualenv` package using `pip`:


``` {.CodeMirror-line role="presentation"}
sudo pip3 install virtualenv
```

Create a `virtual environment` named `quarto_venv`:


``` {.CodeMirror-line role="presentation"}
virtualenv quarto_venv
```

activate your newly created `virtualenvironment`:


``` {.CodeMirror-line role="presentation"}
source quarto_venv/bin/activate
```

now execute following command:


``` {.CodeMirror-line role="presentation"}
pip install -r req.txt
```

the above command installs some python packages we need for this
project.

then run `server.py`:


``` {.CodeMirror-line role="presentation"}
python3 server.py
```

on a separate terminal run `client.py`:


``` {.CodeMirror-line role="presentation"}
python3 client.py
```

after running `client.py` , you should see some logs like following on
`server.py` execution:


``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "GET /socket.io/?transport=polling&EIO=4&t=1639342185.6107757 HTTP/1.1" 200 243 0.000432
```

``` {.CodeMirror-line role="presentation"}
itgWKqS9A51uiinoAAAB connected!
```

``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "POST /socket.io/?transport=polling&EIO=4&sid=UEZimvolDphNpVJeAAAA HTTP/1.1" 200 143 0.001755
```

``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "GET /socket.io/?transport=polling&EIO=4&sid=UEZimvolDphNpVJeAAAA&t=1639342185.6165655 HTTP/1.1" 200 189 0.000128
```

**note**: The most important piece of log is
`itgWKqS9A51uiinoAAAB connected!` which `itgWKqS9A51uiinoAAAB` is the
socket id that defers time to time.

**You\'re good to go.**

 

### **Linux (not recommended)**

Open a terminal which `server.py` and `client.py`are in and execute
following command:


``` {.CodeMirror-line role="presentation"}
pip install -r req.txt
```

the above command installs some python packages we need for this
project.

then run `server.py`:


``` {.CodeMirror-line role="presentation"}
python3 server.py
```

on a separate terminal run `client.py`:


``` {.CodeMirror-line role="presentation"}
python3 client.py
```

after running `client.py` , you should see some logs like following on
`server.py` execution:


``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "GET /socket.io/?transport=polling&EIO=4&t=1639342185.6107757 HTTP/1.1" 200 243 0.000432
```

``` {.CodeMirror-line role="presentation"}
itgWKqS9A51uiinoAAAB connected!
```

``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "POST /socket.io/?transport=polling&EIO=4&sid=UEZimvolDphNpVJeAAAA HTTP/1.1" 200 143 0.001755
```

``` {.CodeMirror-line role="presentation"}
127.0.0.1 - - [2021-12-13 00:19:45] "GET /socket.io/?transport=polling&EIO=4&sid=UEZimvolDphNpVJeAAAA&t=1639342185.6165655 HTTP/1.1" 200 189 0.000128
```

**note**: The most important piece of log is
`itgWKqS9A51uiinoAAAB connected!` which `itgWKqS9A51uiinoAAAB` is the
socket id that defers time to time.

**You\'re good to go.**
