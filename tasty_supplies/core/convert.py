import json
import re

from core.models.context import TSContext
from core.bucket import Bucket
from core.logger import log


class Token:
    def __init__(self, path: str, source: str, expression: str):
        self.path = path
        self.source = source
        self.expression = expression

    def split_expression(self) -> list[str]:
        parts = []
        buf = ""
        paren = 0
        for c in self.expression:
            if c == "(":
                paren += 1
            elif c == ")":
                paren -= 1
            if c == "." and paren == 0:
                parts.append(buf)
                buf = ""
            else:
                buf += c
        if buf:
            parts.append(buf)
        return parts

    def get_method_and_args(self) -> tuple[str | None, dict | None]:
        last = self.split_expression()[-1]
        if match := re.match(r"(\w+)\((.*)\)", last):
            method = match[1]
            args_str = match[2]
            args = {}
            for arg in re.findall(r"(\w+)\s*=\s*([^,]+)", args_str):
                key, value = arg
                try:
                    value = float(value)
                except ValueError:
                    value = value.strip('"')
                args[key] = value
            return method, args
        return None, None


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
        elif expr_type == "merge":
            replace_merge_expr(ctx, token)
        elif expr_type == "recipe":
            pass


def get_vanilla_file(ctx: TSContext, path: str):
    files = list(ctx.vanilla.data.all(path))
    if not files:
        raise FileNotFoundError(f"Vanilla file '{path}' not found in context.")
    namespace_file = files[0][1]
    content = str(namespace_file.get_content())
    return json.loads(content)


def deep_merge(dest, key, value):
    # Fusionne value dans dest[key]
    if key not in dest or not isinstance(dest[key], list):
        dest[key] = value
    else:
        # Si les deux sont des listes, on concatène
        dest[key] += value
    return dest


def replace_merge_expr(ctx: TSContext, token: Token) -> None:
    processed = getattr(ctx, "_processed_merge_exprs", None)
    if processed is None:
        processed = set()
        setattr(ctx, "_processed_merge_exprs", processed)

    processed_key = (token.path, token.expression)
    if processed_key in processed:
        log.debug("Merge for %s already handled, skipping.", processed_key)
        return

    split_expr = token.split_expression()

    merge_path = split_expr[1:]
    merge_expr_key = f"$merge.{'.'.join(merge_path)}" if merge_path else "$merge"

    file = list(ctx.data.all(token.path))[0]
    namespace_file = file[1]
    content = str(namespace_file.get_content())

    merge_entries: dict[str, list] = {}

    def capture_pairs(pairs: list[tuple[str, object]]):
        obj = {}
        for key, value in pairs:
            if isinstance(key, str) and key.startswith("$merge"):
                merge_entries.setdefault(key, []).append(value)
                continue
            if key in obj:
                log.warning("Duplicate key '%s' detected outside merge scope.", key)
            obj[key] = value
        return obj

    try:
        custom_json = json.loads(content, object_pairs_hook=capture_pairs)
    except Exception as e:
        log.error(f"Failed to parse JSON content: {e}")
        return

    merge_values = merge_entries.get(merge_expr_key, [])
    if not merge_values:
        log.warning("No merge values found for key %s.", merge_expr_key)
        return

    try:
        vanilla_json = get_vanilla_file(ctx, token.path)
    except FileNotFoundError as e:
        log.error(f"Vanilla file not found: {e}")
        return

    def deep_merge_json(a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            for k, v in b.items():
                if k in a:
                    a[k] = deep_merge_json(a[k], v)
                else:
                    a[k] = v
            return a
        if isinstance(a, list) and isinstance(b, list):
            return a + b
        return b

    def parse_path_component(component):
        """Parse a path component to handle both dict keys and array indices.

        Returns (key_or_index, is_index) tuple.
        """
        if component.isdigit():
            return int(component), True
        return component, False

    def ensure_path(obj, path):
        """Navigate to the parent of the final key, handling both dicts and arrays."""
        current = obj
        for i, component in enumerate(path[:-1]):
            key_or_index, is_index = parse_path_component(component)

            if is_index:
                # Navigate through array index
                if not isinstance(current, list) or key_or_index >= len(current):
                    log.error(
                        "Array index %d out of bounds or current is not a list",
                        key_or_index,
                    )
                    return None, None
                current = current[key_or_index]
            else:
                # Navigate through dict key
                if not isinstance(current, dict):
                    log.error(
                        "Expected dict at path component %d but got %s",
                        i,
                        type(current),
                    )
                    return None, None
                if key_or_index not in current or not isinstance(
                    current[key_or_index], (dict, list)
                ):
                    current[key_or_index] = {}
                current = current[key_or_index]

        return current, path[-1] if path else None

    def apply_merge_value(target_json, path, value):
        if not path:
            return deep_merge_json(target_json, value)

        parent, final_component = ensure_path(target_json, path)
        if parent is None or final_component is None:
            log.error("Failed to navigate path: %s", path)
            return target_json

        final_key, is_index = parse_path_component(final_component)

        if is_index:
            # Merge into array element
            if not isinstance(parent, list):
                log.error("Expected list for array index but got %s", type(parent))
                return target_json
            if final_key >= len(parent):
                log.error("Array index %d out of bounds", final_key)
                return target_json

            current_value = parent[final_key]
            if isinstance(value, list):
                if not isinstance(current_value, list):
                    log.debug(
                        "Overriding non-list value at index %d with list merge.",
                        final_key,
                    )
                    parent[final_key] = []
                parent[final_key].extend(value)
            elif isinstance(value, dict):
                if not isinstance(current_value, dict):
                    parent[final_key] = {}
                parent[final_key] = deep_merge_json(parent[final_key], value)
            else:
                parent[final_key] = value
        else:
            # Merge into dict key
            if not isinstance(parent, dict):
                log.error("Expected dict for key but got %s", type(parent))
                return target_json

            if final_key not in parent:
                parent[final_key] = [] if isinstance(value, list) else {}

            current_value = parent[final_key]
            if isinstance(value, list):
                if not isinstance(current_value, list):
                    log.debug(
                        "Overriding non-list value at %s with list merge.", final_key
                    )
                    parent[final_key] = []
                parent[final_key].extend(value)
            elif isinstance(value, dict):
                if not isinstance(current_value, dict):
                    parent[final_key] = {}
                parent[final_key] = deep_merge_json(parent[final_key], value)
            else:
                parent[final_key] = value

        return target_json

    for merge_value in merge_values:
        vanilla_json = apply_merge_value(vanilla_json, merge_path, merge_value)

    vanilla_json = deep_merge_json(vanilla_json, custom_json)

    namespace_file.set_content(
        json.dumps(
            vanilla_json,
            indent=4,
            sort_keys=True,
        )
    )

    processed.add(processed_key)


def is_method_expression(expression: str) -> bool:
    method_regex = r"^\$(.+)\((.*)\)$"
    return re.match(method_regex, expression) is not None


def replace_item_expr(ctx: TSContext, bucket: Bucket, token: Token) -> None:
    split_expr = token.split_expression()
    expr_item = split_expr[1]
    item = bucket.get(expr_item)

    if item is None:
        raise ValueError("Item '%s' not found." % expr_item)

    method, args = token.get_method_and_args()
    if method:
        attr = getattr(item, method, None)
        if attr is None:
            raise TypeError(f"Method '{method}' not found on item '{expr_item}'.")
        if callable(attr):
            result = attr(**args)
        else:
            raise TypeError(
                f"Attribute '{method}' of item '{expr_item}' is not callable (it's a property, not a method)."
            )
    else:
        expr_property = split_expr[2]
        attr = getattr(item, expr_property, None)
        if attr is None:
            raise TypeError(
                "Invalid property '%s' in expression '%s'."
                % (
                    expr_property,
                    token.expression,
                )
            )
        if callable(attr):
            raise TypeError(
                f"Attribute '{expr_property}' of item '{expr_item}' is a method, not a property. Use parentheses to call it."
            )
        result = attr

    if not isinstance(result, (dict, str)):
        raise TypeError("Invalid type result of property.")

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
