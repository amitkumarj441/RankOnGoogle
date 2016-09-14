### RankOnGoogle

Python and an embedded php script to rank your name on Google

# p.php

  1. Makes html UI
  2. Prepare the input (site name and keywords)
  3. Call python file (page.py) to get search results
  4. Process the output from python

# page.py

  1. With the input information for the site and keywords, it uses modified version of pygoogle.py.
  2. The pygoogle.py is based on Google AJAX Search Module.
  3. After all the process, the page.py returns the url and the rank to the p.php.
  

# KLienberg Algorithm

  
