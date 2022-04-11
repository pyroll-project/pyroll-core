class MaxIterationCountExceededError(RuntimeError):
    """Error that is raised, when the maximum iteration count in a solution loop is exceeded."""

    def __init__(self):
        super().__init__("The maximum iteration count of this loop was exceeded.")
