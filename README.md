# PlotInterface

Download this project, using Git:
    `git clone https://github.com/GAGvozdik/PlotInterface.git`

Use terminal and go to `cd PlotInterface/`.

File `requirements.txt` contains list of dependencies, that can be installed using 
    `pip install numpy matplotlib pyqt5` 
or 
    `pip install -r requirements.txt`.

Installation in virtual environment is recommended.

Run `mainApp.py`.

`classes` - contains helpful classes with basic interface `classes/interface.py`, `classes/graphObjects` and examples: `classes/examples.py`, `classes/example1.py` ...

`classes/examples.py` contains list of examples, that you can see after running `mainApp.py`. You can comment or remove examples, that you don`t need.
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
`styles/DarkTheme.qss` contains styles, that were applyed in `mainApp.py`
```
                    ...
    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)
                    ...
```



