# 💡 Challenge: Aggregations

For this take-home exercise, we'd like you to **build an aggregation algorithm** using the data file provided.

The Peregrine platform is commonly used to analyze large datasets of semi-structured data. One tool for understanding a dataset is to visualize its values as an aggregation. This aggregation presents the distinct values from a dataset along with counts of their occurrences.

For example, given a list

```json
["apple", "apple", "banana", "orange", "orange", "orange"]
```

a sorted aggregation `[value, count]` of the data might look like:

```json
[
  ["orange", 3],
  ["apple", 2],
  ["banana", 1]
]
```

## ⚙️ Functionality

**Given a JSON file containing a list of objects, write a program that takes a query and returns a sorted property aggregation based on the objects matching the query.**

### The data

- An object has a **model** key that is either person, vehicle, or case
- An object has a **properties list**, where each property is a JSON object with three keys:
  - **slug** - A string identifier for the given property.
  - **type** - The data type of the property value. There are three data types:
    - string
    - integer
    - boolean
  - **value** - The object's value for the given property.

You can assume that **slug and type are non-nullable** and that value **will always match the given type or be null.**

**An example object**

```json
{
  "model": "person",
  "properties": [
    {
      "slug": "first_name",
      "type": "string",
      "value": "john"
    },
    {
      "slug": "last_name",
      "type": "string",
      "value": "doe"
    },
    {
      "slug": "age",
      "type": "integer",
      "value": 32
    }
  ]
}
```

### The program

1. An algorithm to **filter data** based on model and property filters.
   1. **Multiple models should union**
      1. If case and person model filters are specified, return data matching case OR person.
   2. **Multiple key-value pairs should intersect**
      1. If first_name:ben and hair_color:brown filters are specified, return data having first_name equal to ben AND hair_color equal to brown.
   3. **Multiple values should union**
      1. If first_name:ben,elise filter is specified, return data having first_name equal to ben OR elise.
2. Output an aggregation of the filtered data.
   1. Your program should return an object mapping **property slugs to a 2-dimensional array of sorted aggregations** where an aggregation is [value, count] and the sort is based on the count.

**Example commands**

```bash
> python main.py --models person
{'age': [(36, 136), (35, 96), ...], 'first_name': [('victor', 131), ('sarah', 113), ...]}

> python main.py --models vehicle --properties make:toyota
{'impounded': [(False, 108), ...], 'make': [('toyota', 159)], ...]}

> python main.py --properties year:2008,2006
{'city': [('vallejo', 38), ('oakland', 29), ...], ...}
```
