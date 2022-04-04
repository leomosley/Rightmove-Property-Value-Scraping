# Rigthmove Property Value Scraper


## Packages
Below are the required packages for this program. 
```python
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import random
import datetime
import csv
import os
from decimal import Decimal
from os import listdir
from os.path import isfile, join
```
The `boroughList` dictionary will need to be imported from the `boroughList.py` 

```python
from boroughList import boroughList
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
