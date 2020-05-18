# covid-usa
Covid-19 data visualization filtered by state.


> brew cask install dash<br/>
> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py<br/>
> pip install plotly==4.7.1 <br/>
> python covid-us.py<br/>

Covid-19 data provided by [The New York Times](https://github.com/nytimes/covid-19-data)<br/>
Modified code from [dataviz.shef](http://dataviz.shef.ac.uk/tutorials/dash/)<br/>
Issues with starting server:<br/>
You already have a process bound to the default port (8000)<br/>
Try:<br/>
> ps -fA | grep python <br/>
> 501 81651 12648   0  9:53PM ttys000    0:00.16 python -m SimpleHTTPServer

The second number is the process number; stop the server by sending it a signal:
>kill 81651<br/>
> python covid-us.py<br/>
