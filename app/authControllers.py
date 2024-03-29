def setupAuthController(app):
    """
    Set up CORS headers on the response.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        Flask: The modified Flask application instance.
    """

    @app.after_request
    def after_request(response):
        """
        Add CORS headers to the response.

        Args:
            response (object): The Flask response object.

        Returns:
            object: The modified Flask response object.
        """
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    return app
