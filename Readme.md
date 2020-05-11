# Flatty
Very simple way to make your generators flat

## Usage examples

When you extract data from MySQL, process data, then load into MongoDB, you 
should write code like in example:

```python
def transform_from_mysql():
# some code to fetch data
# ... 
    for row in result:
        # ...
        # some code to process data
        # ...
        load_into_mongo(processed_row)
# ...    
``` 

This code will work, but you cannot reuse function `transform_from_mysql`, 
if you need change process logic, or change mongoDB for Cassandra.

You can write 3 separate functions using flatty and reuse it:

```python
import flatty

def transform_mysql() -> dict:
    # fetch data
    for row in cursor:
        yield row

def process(row: dict) -> dict:
    ...

def load_mongo(row: dict):
    ...

chain = flatty.next_fn(transform_mysql)
chain.next_fn(process)
chain.next_fn(load_mongo)
chain.execute()

``` 

Every next function will get result of previous as argument

Use it with generators :)   
