# Shipping Cost Calculator
# https://trueinterview.io/questions/shipping-cost-calculator
# Python 3, 559 ms. Accepted on TrueInterview.

#region Provided setup - imports and helper types, no changes needed
from __future__ import annotations
import sys, math, string, re, random, json, collections, heapq, bisect, functools, itertools, operator
from typing import *
from collections import *
from heapq import *
from bisect import *
from functools import *
from itertools import *
#endregion
class Solution:
    def tiered_cost(self, tiers, quantity):
        total, remaining = 0, quantity
        for tier in tiers:
            if remaining <= 0:
                break
            if tier["maxQuantity"] is None:
                units = remaining
            else:
                units = min(remaining, tier["maxQuantity"] - tier["minQuantity"])
            total += tier["cost"] if tier["type"] == "fixed" else units * tier["cost"]
            remaining -= units
        return total

    def computeShippingCost(self, order: Dict[str, Any], shipping_cost: Dict[str, Any]) -> int:
        configs = shipping_cost[order["country"]]
        product_configs = {}

        for config in configs:
            product_configs[config["product"]] = config

        total = 0
        for item in order["items"]:
            quantity = item["quantity"]
            config = product_configs[item["product"]]
            if "cost" in config: # Part 1 flat per-unit rate
                total += quantity * config["cost"]
                continue
            
            total += self.tiered_cost(config["costs"], quantity)
        return total
            
#region Provided code - reads the input and prints your answer, no changes needed
import sys
import json

def main():
    data = sys.stdin.read().strip()
    if not data:
        return
    lines = data.split('\n')
    if len(lines) < 2:
        return
    order = json.loads(lines[0])
    shipping_cost = json.loads(lines[1])
    result = Solution().computeShippingCost(order, shipping_cost)
    print(result)

if __name__ == '__main__':
    main()
#endregion
