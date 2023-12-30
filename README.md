# Aircraft-Tire-Selector
This program automatically processes key aircraft design requirements (load input and maximum speed). Through multivariate optimization, aircraft tire design options are recommended to the aircraft landing gear designers for selection. 

## Repository structure 
```
- main.py
- models.py: the Tire class that stores parameters and defines functions of a typical aircraft tire 
- /manufacturer_data: testing and validation with manufacturer's public data
  |-- _methods.py: import models.py from root directory 
  |-- model_eval.py: calculate difference between calculated and provided values 
  |-- eval_analysis.py: analysis of the evaluating results from model_eval.py 
- /optimizations: store all alternative optimization methods used, evaluated with optimization on bias tires only 
  |-- _models.py: import models.py from root directory 
  |-- bayesOps.py: Bayesian optimization method 
  |-- csp.py: method for solving constraint satisfaction problems 
  |-- genAlg.py: genetic algorithm method 
  |-- gradients.py: method utilizing the openMDAO framework 
  |-- pso.py: particle swarm optimization method 
  |-- randSearch.py: random search method 
  |-- selector.py: select optimal tire given load requirements from manufacturer data
```

## Development guide 
Follow instructions below when developing: 

### Local development 

When you try to make changes to the code repository, always start from a **branch** of the "main" branch, or other branches. A branch can be created either in GitHub or in the version control icon at the bottom left corner of your VS Code. The former one (in GitHub) is preferred, so that others can also see your progress. 

Before making changes to your local code repository: 
1. Check if your local repository is up to date.
    - Run `git fetch --all` in terminal to retrieve the latest updates in all branches from the remote code repository. 
    - If updates are shown near the refresh icon at the bottom left corner of your VS Code, make sure to click and **pull** the new commits from the cloud. 
    - If your branch is behind the main branch, you may want to **rebase** your branch to the current main branch. This can be done in the "Source Control" tab of the left panel. 
3. Make sure you are working in your local virtual environment, where you should see `(venv)` in front of the `(base)` in your terminal's command lines. If not, run the following command in terminal to activate the virtual environment: 
    - In MacOS: `source venv/bin/activate`. 
    - In Windows: `source venv/Scripts/activate`.
4. Update your local virtual environment to the new `requirements.txt`, if any changes were made from others' commits. 
    - Run the following command in terminal: `pip install -r requirements.txt`. 
5. Now you can make your changes to the code. Meanwhile, please follow guidelines in the `dev_notes.md` file. 

After changes are made locally and ready for upload: 
1. Make sure all modified files are saved. 
2. Make sure `requirements.txt` is upated to include any new packages that you have used. Run the following command and the file will be updated automatically: `pip freeze > requirements.txt`. 
3. In the "Source Control" icon in the left panel, **stage** and **commit** all changes, provide a brief summary of your commit, and **push** your commit to the cloud (GitHub). 

After changes are pushed to your own branch, create a **pull request** (PR) with more detailed description of your commits and ask for **review** before **merging** to the "main" branch. However, PRs don't need to be created for every commit, where one PR may include multiple commits. 

### First time setup 
1. Clone this repository to your local IDE as you would do for other code repositories. 
2. Create a virtual environment in your local code repository  with the following command in terminal: `python3 -m venv venv`. 
    - In Windows, you may need to replace `python3` with `python` or `py`. 
3. Make sure your virtual environment is activated. 
    - In MacOS, use `source venv/bin/activate`. 
    - In Windows, use `source venv/Scripts/activate`.  
    - After successful activation, you should see `(venv)` added in front of `(base)` at the beginning of your terminal command line. 
4. Download/upgrade all Python packages required for this code repository, as outlined in the `requirements.txt`, to your local virtual environment. 
    - Use the following command: `pip install -r requirements.txt`.  
