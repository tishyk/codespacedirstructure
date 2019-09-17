def sum(a: str, b: str) -> str:
    """Comments"""
    return ''.join(sorted(a + b, key=lambda x: "XVI".index(x))) \
        .replace("IIIII", "V") \
        .replace("VV", "X") \
        .replace("XXXXX", "L")
