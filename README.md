# Rocket Request

A Python program to determine the least number of rocket launches required for
a set of items in the factory management game Factorio.

The program takes items in Factorio as input and shows how to distribute them
amongst your silos for each launch.

This program uses a first-fit-decreasing algorithm to output a partition of the
items into silos such that the sum of weight does not exceed 1000 kg.
