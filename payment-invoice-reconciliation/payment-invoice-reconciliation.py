# Payment Invoice Reconciliation
# https://trueinterview.io/questions/payment-invoice-reconciliation
# Python 3, 713 ms. Accepted on TrueInterview.

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
from typing import List

class Solution:
    def process_invoice(self, invoices: List[str]) -> tuple[dict[str, Invoice], dict[str, Invoice]]:
        invoice_map = {} # {id: Invoice}
        amount_ealier_inv = {} #{amount: Invoice}
        for invoice in invoices:
            _id, due_date, amount = [s.strip() for s in invoice.split(",")]
            if _id not in invoice_map:
                invoice_map[_id] = Invoice(_id, due_date, amount)
            if amount not in amount_ealier_inv or (due_date, _id) < (amount_ealier_inv[amount].due_date, amount_ealier_inv[amount]._id):
                amount_ealier_inv[amount] = Invoice(_id, due_date, amount)
        return invoice_map, amount_ealier_inv

    def get_forgiveness_inv(self, amount: int, forgiveness: int, amount_ealier_inv: dict[int, Invoice]) -> Invoice | None:
        lower = amount - forgiveness
        upper = amount + forgiveness
        found = None
        for _amount in range(lower, upper + 1):
            _amount = str(_amount)
            if _amount in amount_ealier_inv:
                candidate = amount_ealier_inv[_amount]
                if not found or (candidate.due_date, candidate._id) < (found.due_date, found._id):
                    found = candidate
        return found

    def reconcilePayment(self, payment: str, invoices: List[str], forgiveness: int = 0) -> str:
        try:
            processed_invoices, amount_ealier_inv = self.process_invoice(invoices)
            fields = [p.strip() for p in payment.split(",", 2)]
            pid = fields[0]
            if len(fields) < 2:
                return f"Payment {pid} could not be matched to any invoice"
            amount = fields[1]
            try:
                int(amount)
            except:
                return f"Payment {pid} could not be matched to any invoice"
            memo = fields[2] if len(fields) == 3 else ""
            inv_id = None
            try:
                inv_id = memo.split(":")[1].strip()
            except:
                pass

            if inv_id and inv_id[:4] == "inv-":
                if inv_id in processed_invoices:
                    due_date = processed_invoices[inv_id].due_date
                    return f"Payment {pid} paid {amount} for invoice {inv_id} due on {due_date}"
                else:
                    return f"Payment {pid} could not be matched to any invoice"
            elif amount in amount_ealier_inv:
                inv_id = amount_ealier_inv[amount]._id
                due_date = amount_ealier_inv[amount].due_date
                return f"Payment {pid} paid {amount} for invoice {inv_id} due on {due_date}"
            else:
                inv = self.get_forgiveness_inv(int(amount), forgiveness, amount_ealier_inv)
                if inv:
                    return f"Payment {pid} paid {amount} for invoice {inv._id} due on {inv.due_date}"
            return f"Payment {pid} could not be matched to any invoice"
        except Exception as e:
            print(e)

class Invoice:
    def __init__(self, _id, due_date, amount):
        self._id = _id
        self.due_date = due_date
        self.amount = amount

#region Provided code - reads the input and prints your answer, no changes needed
import sys


def main():
    data = sys.stdin.read()
    if data.endswith("\n"):
        data = data[:-1]
    if data == "":
        lines = [""]
    else:
        lines = data.split("\n")
    lines = [ln.rstrip("\r") for ln in lines]

    idx = 0
    payment = lines[idx] if idx < len(lines) else ""
    idx += 1

    n = 0
    if idx < len(lines):
        try:
            n = int(lines[idx].strip())
        except (ValueError, TypeError):
            n = 0
    idx += 1

    invoices = []
    for _ in range(n):
        if idx < len(lines):
            invoices.append(lines[idx])
            idx += 1

    forgiveness = 0
    if idx < len(lines):
        try:
            forgiveness = int(lines[idx].strip())
        except (ValueError, TypeError):
            forgiveness = 0

    print(Solution().reconcilePayment(payment, invoices, forgiveness))


main()
#endregion
