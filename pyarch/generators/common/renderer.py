from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"

environment = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    undefined=StrictUndefined,
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)


def render_template(template_name: str, **context: object) -> str:
    template = environment.get_template(template_name)
    return template.render(**context)


def create_file_from_template(
    template_name: str,
    output_path: Path,
    **context: object,
) -> Path:
    content = render_template(template_name, **context)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path
