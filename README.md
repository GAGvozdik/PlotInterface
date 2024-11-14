# PlotInterface

Download this project, using Git:
    `git clone https://github.com/GAGvozdik/PlotInterface.git`

Use the terminal and go to `cd PlotInterface/`.

File `requirements.txt` contains a list of dependencies, that can be installed using 
    `pip install numpy matplotlib pyqt5 scikit-gstat` 
or 
    `pip install -r requirements.txt`.

Installation in a virtual environment is recommended.

Run `mainApp.py`.

`classes` - contains helpful classes with basic interface `classes/interface.py`, `classes/graphObjects` and examples: `classes/examples.py`, `classes/example1.py` ...

`classes/examples.py` contains examples you can see after running `mainApp.py`. You can comment or remove examples, that you don`t need.
```
class AllExamples(
        # PlotInterface,
        # Example15, 
        Example14, 
        # Example13, 
        Example12, 
        # Example11, 
        # Example10, 
        # Example9,
        # Example8, 
        # Example7, 
        # Example6, 
        # Example5, 
        # Example4, 
        # Example3, 
        # Example2, 
        # Example1
    ):
```
`styles/DarkTheme.qss` contains styles, that were applied in `mainApp.py`
```
                    ...
    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)
                    ...
```

Problems with geon module installing you can solve using official geon docks ```https://scikit-gstat.readthedocs.io/en/latest/install.html```



