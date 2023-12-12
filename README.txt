You must have BeautifulSoup matplotlib and lxml imstalled in order to run this code
this can be done by using 'pip install beautifulsoup4 lxml matplotlib'

The XML files should be scored in a folder named 'data' at the same level as the main.py file
this should be such that from main.py, the following paths are valid: './data/brazil58.xml', './data/burma14.xml'

In order to run a simulation, the main.py file must be executed.


Within this the 'trial' function is used to run a simulation 'n' times.
Below highlights the parameters that trial takes
'''
    tiral(path, no. ants, q, alpha, beta, max_evals, heuristic, number of trials)
'''
The below code runs trial function, however it will run it '5' times as specified in the final parameter.
It will run an ACO on burma with a transition rule heuristic, 100 ants, 0.5 for q, 0.51 for e, and
1 and 2 for alpha and beta respectively
    trial(paths[0], 100, 0.5, 1, 2, 0.51, 10000, heuristics[0], 5)
'''

By default the code will run the above trial.

For parameters such as the path, heuristic and method, please refer to the arrays in main.py,
select the index of the desired option from the array, these are used when calling the trial function.

