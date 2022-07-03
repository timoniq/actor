from .default import Response
import typing
import jinja2


class HTMLResponse(Response):
    def __init__(self, jinja_env, template_fn: str, context: dict):
        template = jinja_env.get_template(template_fn)
        body = template.render(**context).encode("utf-8")
        super().__init__(200, body)
        self.content_type = "text/html"


class HTMLResponseFactory:
    def __init__(self, template_folders: typing.List[str]):
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_folders)
        )

    def form(self, name: str, context: dict) -> HTMLResponse:
        return HTMLResponse(self.jinja_env, name, context)
