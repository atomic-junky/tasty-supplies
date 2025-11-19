import json
import re
from beet import NamespaceFile, DataPackNamespace

from core.models.context import TSContext
from core.bucket import Bucket


class Token:
    def __init__(self, path: str, source: str, expression: str):
        self.path = path
        self.source = source
        self.expression = expression

    def split_expression(self) -> list[str]:
        return self.expression.split(".")


def convert_data(ctx: TSContext, bucket: Bucket) -> None:
    expr_regex = r"\"\$(.+)\""

    tokens: list[Token] = []

    for path, namespace in list(ctx.data.all()):
        content = str(namespace.get_content())
        matches = re.finditer(expr_regex, content, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            if matchNum > 0:
                source = match.group()
                expression = match.group(1)

                tokens.append(Token(path, source, expression))

    for token in tokens:
        split_expr = token.split_expression()
        expr_type = split_expr[0]

        if expr_type == "item":
            replace_item_expr(ctx, bucket, token)
        elif expr_type == "recipe":
            pass


def replace_item_expr(ctx: TSContext, bucket: Bucket, token: Token) -> None:
    split_expr = token.split_expression()
    expr_item = split_expr[1]
    expr_property = split_expr[2]
    item = bucket.get(expr_item)

    result = ""

    if hasattr(item, expr_property):
        result = getattr(item, expr_property)
    else:
        raise "Invalid property '%s' in expression '%s'." % (
            expr_property,
            token.expression,
        )

    if not isinstance(result, (dict, str)):
        raise "Invalid type result of property '%s'." % expr_property

    if isinstance(result, dict):
        result = json.dumps(result)

    file = list(ctx.data.all(token.path))[0]
    namespace_file = file[1]
    content = str(namespace_file.get_content())
    content = content.replace(token.source, result, 1)

    try:
        json_content = json.loads(content)
        namespace_file.set_content(
            json.dumps(
                json_content,
                indent=4,
                sort_keys=True,
            )
        )
    except ValueError as e:
        namespace_file.set_content(content)
