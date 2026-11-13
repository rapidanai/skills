def preview_total(subtotal, preferred):
    discount = 0.10 if preferred else 0
    return subtotal * (1 - discount)


def checkout_total(subtotal, preferred):
    discount = 0.05 if preferred else 0
    return subtotal * (1 - discount)
