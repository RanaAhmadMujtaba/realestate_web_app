from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)

def render_error(error_code, error_title, error_message):
    return render_template(
        "error.html",
        error_code=error_code,
        error_title=error_title,
        error_message=error_message
    ), error_code

@errors.app_errorhandler(400)
def bad_request(e):
    return render_error(400, "Bad Request", "The request could not be understood by the server.")

@errors.app_errorhandler(401)
def unauthorized(e):
    return render_error(401, "Unauthorized", "You need to log in to access this page.")

@errors.app_errorhandler(403)
def forbidden(e):
    return render_error(403, "Forbidden", "You don’t have permission to access this page.")

@errors.app_errorhandler(404)
def page_not_found(e):
    return render_error(404, "Page Not Found", "The page you’re looking for doesn’t exist.")

@errors.app_errorhandler(405)
def method_not_allowed(e):
    return render_error(405, "Method Not Allowed", "This request method is not allowed.")

@errors.app_errorhandler(408)
def request_timeout(e):
    return render_error(408, "Request Timeout", "The server timed out waiting for the request.")

@errors.app_errorhandler(429)
def too_many_requests(e):
    return render_error(429, "Too Many Requests", "You have sent too many requests in a given time.")

@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_error(500, "Internal Server Error", "Something went wrong on our end.")

@errors.app_errorhandler(502)
def bad_gateway(e):
    return render_error(502, "Bad Gateway", "The server received an invalid response.")

@errors.app_errorhandler(503)
def service_unavailable(e):
    return render_error(503, "Service Unavailable", "The server is temporarily unavailable.")

@errors.app_errorhandler(504)
def gateway_timeout(e):
    return render_error(504, "Gateway Timeout", "The server did not respond in time.")
