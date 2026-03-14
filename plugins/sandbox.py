def safe_execute(plugin, data):
    """
    Basic plugin sandbox security
    """

    allowed_methods = ["execute"]

    for attr in dir(plugin):

        if attr.startswith("_"):
            continue

        if attr not in allowed_methods:
            raise Exception(
                f"Unsafe plugin attribute detected: {attr}"
            )

    return plugin.execute(data)