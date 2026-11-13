from orders import preview_total


def show_preview(subtotal, preferred):
    return f"Total: {preview_total(subtotal, preferred):.2f}"
