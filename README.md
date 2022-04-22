# COM526-AE2 Sudoku Solver

## System Requirements

1. [Python](https://www.python.org/) installation ( > 3.8.0 )
2. Install the following Python packages and their dependencies:
    * [numpy](https://www.numpy.org) ( > 1.19.5 )
    * [pandas](https://pandas.pydata.org) ( > v 1.4.2 )
    * [opencv-python](https://github.com/skvark/opencv-python) ( > 4.5.5.64 )
    * [matplotlib](https://matplotlib.org) ( > 3.5.1 )
    * [scikit-learn](http://scikit-learn.org) ( > 1.0.2 )
3. (Optional) For image recognition functions:
    * [tensorflow](https://www.tensorflow.org/) ( **2.4.2** ). Detailed instructions can be found 
    [here](https://www.tensorflow.org/install/pip) and [here](https://www.tensorflow.org/install/gpu).
    
## Running the Application

1. Clone this repository
2. Ensure the above packages are installed
3. Download this [kaggle download](https://www.kaggle.com/datasets/bryanpark/sudoku) and save it to the project folder
as "sudoku.csv".
3. Run the code from within the code directory with:

        python menu.py
        
        
#### Solving Quizzes

The application loads quizzes from the "sudoku.csv" file. This 
[kaggle download](https://www.kaggle.com/datasets/bryanpark/sudoku), 
included in this repo, file contains both quizzes and solutions. You can replace this file with your own quizzes, just
ensure that the formatting and name are the same.

Within the application menu, choose option 

        1: Solve quizzes
        
and follow the prompts.

### Image recognition

The image recognition functions require tensorflow to be installed, as instructed in the 
[System Requirements](System-Requirements). 

Within the application menu, choose option 

        2: Image recognition
        
and follow the prompts.

* Paths can be from the root of the application.

* Images can be .png or .jpg.

* During the process, you will be able to see the outputs for different stages, to resume the program press any key.

* The 'BoardCells' & 'CleanedBoardCells' folders will contain outputs that you can view.


### Run benchmark

You can run a benchmark on your .csv of Sudoku puzzles by choosing option

        3: Run benchmark
        
The results of the benchmark will be written to the 'benchmarks.csv' in the project folder. 