def vx_bins2binby(start, end, step=1):
    """
    Generate binning parameters for Vaex's `binby` function based on the given start, end, and step.

    Parameters:
        start (float): The starting value of the binning range.
        end (float): The ending value of the binning range.
        step (float, optional): The step size for binning. Defaults to 1.

    Returns:
        dict: A dictionary containing binning parameters suitable for `binby` function in Vaex.
            - 'limits': Tuple containing the lower and upper limits of the binning range, centered on whole number bins.
            - 'shape': Number of bins calculated based on the provided range and step size.

    Example:
        >>> vx_bins2binby(0, 10, 2)
        {'limits': (-1.0, 11.0), 'shape': 6}
    """
    return {'limits': (-step/2, end + step/2), 'shape': int(end/step) + 1}