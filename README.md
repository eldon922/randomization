# Randomization

Privacy preserving data mining become a serious concern nowadays. There is a demand to make sure all data which used in data mining process to be secure and doesn't violate any privacy infringement. This software use randomization techniques to eliminate privacy in data but still can be used for data mining. Two randomization techniques are implemented in this software that is Random Rotation Perturbation and Random Projection Perturbation.

This software intended to be built for a research namely **Analysis of Random Rotation Perturbation and Random Projection Perturbation Techniques in Randomizing Data for Data Mining**.

### Prerequisites

This software can be run in any environment which support Python 3. You need to install the following program. The following prerequisites installation instruction will be provided in the next section.

1. Python 3 - https://www.python.org/
2. Kivy 2 - https://kivy.org/
3. Plyer - https://github.com/kivy/plyer
4. Sklearn - https://scikit-learn.org/
5. Pandas - https://pandas.pydata.org/

## Getting Started

The following instruction will demonstrate how to install the dependency and run the software in Microsoft Windows environment from the source code using Python.

1. Install Python 3 using executable file installer. Download [here](https://www.python.org/downloads/) and follow the instruction there

2. Place this software source code in your local drive at a directory

3. Go to the directory then open command prompt in that directory

4. Create a Python virtual environment first (Note: actually you can skip this step to not use virtual environment but it's a better practice to use it)
    ```
    python -m venv venv
    ```

5. Activate the newly created Python virtual environment
    ```
    venv\Scripts\activate
    ```

6. Install Kivy 2
    ```
    pip install kivy[base] kivy_examples --pre --extra-index-url https://kivy.org/downloads/simple/
    ```

7. Install Plyer, Sklearn, Pandas
    ```
    pip install plyer sklearn pandas
    ```

8. Run the main source code. Remember to always run the software using the Python virtual environment, follow step 5
    ```
    python __main__.py
    ```

## Built With

* [Python](https://www.python.org/) - Programming Language
* [Kivy](https://kivy.org/) - UI Python Framework
* [Plyer](https://github.com/kivy/plyer) - Platform-independent Native Functionality API
* [Sklearn](https://scikit-learn.org/) - Machine Learning Python Library
* [Pandas](https://pandas.pydata.org/) - Data Manipulation and Analysis Python Library
* [Numpy](https://numpy.org/) - A Python Library Used for Working with Arrays
* [Scipy](https://www.scipy.org/) - Scientific Computing and Technical Computing Python Library

## Authors

* **Chris Eldon** - Computer Science - *Graduate Student at Parahyangan Catholic University*
