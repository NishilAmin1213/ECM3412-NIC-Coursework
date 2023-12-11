You must have BeautifulSoup matplotlib and lxml imstalled in order to run this code
this can be done by using 'pip install beautifulsoup4 lxml matplotlib'

In order to run a simulation, the main.py file must be executed.

The XML files should be scored in a folder named 'data' at the same level as the main.py file
this should be such that from main.py, the following paths are valid: './data/brazil58.xml', './data/burma14.xml'

In order to modify parameters, open main.py and modify the parameters passed in when creating and using the ACO Object
this is on line 16 and 19.

For parameters such as the path, heuristic and method, please refer to the arrays in main.py,
select the index of the desired option from the array, these are used in line 16 and 19
