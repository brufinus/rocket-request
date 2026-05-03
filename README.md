# Rocket Request

A Python program to determine the least number of rocket launches required for
a set of items in the factory management game Factorio.

The program takes items in Factorio as input and shows how to distribute them
amongst your silos for each launch.

This program uses a first-fit-decreasing algorithm to output a partition of the
items into silos such that the sum of weight does not exceed 1000 kg.

## Usage

Requires Python.

Example usage and program output:

```bash
$ python main.py
Number of Rocket silos: 4
Add items to the silo. Enter 'done' once finished.
Item: belt
Count: 124
Item: inserter
Count: 12
Item: splitter
Count: 8
Item: chem plant
Count: 4
Item: thruster
Count: 2
Item: crusher
Count: 3
Item: assembling2
Count: 4
Item: pipe
Count: 15
Item: asteroidcollector
Count: 4
Item: car
Count: 1
Item: done

Total launches required: 5
Required launch cycles: 2
╔════════════════════════╗
║      Cycle 1 of 2      ║
╚════════════════════════╝

        Silo 1 [██████████] (1000/1000 kg):
                Item                              Count
                ---------------------------------------
                Car                                   1

        Silo 2 [██████████] (1000/1000 kg):
                Item                              Count
                ---------------------------------------
                Chemical plant                        4
                Crusher                               2
                Thruster                              2

        Silo 3 [██████████] (1000/1000 kg):
                Item                              Count
                ---------------------------------------
                Transport belt                        2
                Splitter                              8
                Inserter                             12
                Assembling machine 2                  4
                Asteroid collector                    4
                Crusher                               1

        Silo 4 [██████████] (1000/1000 kg):
                Item                              Count
                ---------------------------------------
                Transport belt                      100
╔════════════════════════╗
║      Cycle 2 of 2      ║
╚════════════════════════╝

        Silo 1 [███░░░░░░░] (295/1000 kg):
                Item                              Count
                ---------------------------------------
                Transport belt                       22
                Pipe                                 15

Consolidated silo contents:

        Silo 1 (1295 kg):
                Item                              Count
                ---------------------------------------
                Transport belt                       22
                Pipe                                 15
                Car                                   1

        Silo 2 (1000 kg):
                Item                              Count
                ---------------------------------------
                Chemical plant                        4
                Crusher                               2
                Thruster                              2

        Silo 3 (1000 kg):
                Item                              Count
                ---------------------------------------
                Transport belt                        2
                Splitter                              8
                Inserter                             12
                Assembling machine 2                  4
                Asteroid collector                    4
                Crusher                               1

        Silo 4 (1000 kg):
                Item                              Count
                ---------------------------------------
                Transport belt                      100
```
