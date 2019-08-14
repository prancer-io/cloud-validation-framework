Rules are not limited to simple comparison statements. You have access to a few functions and a comprehensive number of operators.

# Operators

We have talked about the equality `=` comparison operator so far, but as you can see from the list below, you have access to all common operators from mathematical and boolean expressions.

**Arithmetic operators**

| Operator | What it does |
|:--------:|--------------|
| `+` | Addition operator |
| `-` | Subtraction operator |
| `*` | Multiplication operator |
| `/` | Division operator |
| `%` | Modulo operator |
| `^^` | Exponent operator |

**Boolean operators**

| Operator | What it does |
|:--------:|--------------|
| `||` | Or operator |
| `&&` | And operator |
| `!` | Not operator |

**Comparison operators**

| Operator | What it does |
|:--------:|--------------|
| `=` | Compares for equality |
| `<` | Compares for less than |
| `>` | Compares for greater than |
| `<=` | Compares for less than or equal to |
| `>=` | Compares for greater than or equal to |

**Lookup operators**

| Operator | What it does |
|:--------:|--------------|
| `{m}` | Retrieves the snapshot data for snapshot id `m` |

**List operators**

| Operator | What it does |
|:--------:|--------------|
| `m[]` | Retrieves the complete list from `m` |
| `m[n]` | Retrieves the `n`'th item from the list `m` |
| `m['n'='o']` | Retrieves the item that matches predicate `n` equals `o` from the list `m` |

**Dictionnary operators**

| Operator | What it does |
|:--------:|--------------|
| `m.n` | Retrieves the property `n` from the dictionnary `m`  |

# Functions

Functions work just like any other programming language, use the identifier and pass the parameters inside of parentheses and they will yield something.

**Data control**

| Operator | What it does |
|:--------:|--------------|
| `exists(n)` | Ensures that `n` does not resolve to `None` |

**Data aggregation**

| Operator | What it does |
|:--------:|--------------|
| `count(n)` | Counts the number of items in `n` |

# Mixing operators and functions

You can create very complex expressions with what you have seen so far. There is almost no limit to what you can do with the rules engine. Here are a few complex examples:

**Compare that the dnsServers of two different snapshots**

    {2}.properties.dhcpOptions.dnsServers[] = {3}.properties.dhcpOptions.dnsServers[]

**Ensure you have at least 4 DNS servers defined**

    count({2}.properties.dhcpOptions.dnsServers[]) + count({3}.properties.dhcpOptions.dnsServers[]) = 4

The only limit is your imagination and the data that you have on hand.