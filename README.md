# smiecioInator 

Solo project for AI course. The task involved programming an autonomous garbage truck moving on a 10x10 grid. Obstacles were generated on the grid, which the garbage truck had to avoid (houses), as well as obstacles it could choose to avoid or not (holes, depending on their profitability to avoid). Route to the next truck destination was determined thanks to implementing A* algorithm.

Neural networks were trained and used in the project for recognizing the type of collected garbage, while decision trees were employed for making decisions whether to head to the landfill, empty the garbage truck's contents, or go for another piece of garbage.

## Setup

In order to run this project, after cloning the repository, you have to create and activate virtual environment. 

```bash
python -m venv venv
cd venv/Scripts
activate
cd ../..
```

In order to run this project, you also have to install required libraries.

```bash
pip install -r requirements.txt
```

After completing these steps you can run project!

## Usage

To test the capabilities of the garbage truck, after launching the grid window, you should press the "L" key on the keyboard to load the trained models.

As soon as they will be loaded, you will see notifications about it in the terminal. Garbage truck will start working after pressing "G". Most probably it will go to pick up trash. After that, you can press "G" for next steps/decisions.
