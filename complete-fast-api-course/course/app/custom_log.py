from fastapi import Request


def log(tag="[APP]", message="", request: Request = None):
    with open("log.txt", "a+") as log:
        log.write(f"{tag}: {message}\n")
        log.write(f"\t{request.url}\n")
