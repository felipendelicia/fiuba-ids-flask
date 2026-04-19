from flask import request


def build_links(total, offset, limit):
    """Construye los links HATEOAS para navegar entre páginas"""
    base_url = request.base_url

    # Mantener filtros actuales (equipo, fecha, fase, etc.) en los links
    extra = ""
    for key, value in request.args.items():
        if key not in ('_offset', '_limit'):
            extra += f"&{key}={value}"

    def make_url(off):
        return f"{base_url}?_offset={off}&_limit={limit}{extra}"

    last_offset = max(0, ((total - 1) // limit) * limit) if total > 0 else 0
    prev_offset = max(0, offset - limit)
    next_offset = min(last_offset, offset + limit)

    return {
        "_first": {"href": make_url(0)},
        "_prev": {"href": make_url(prev_offset)},
        "_next": {"href": make_url(next_offset)},
        "_last": {"href": make_url(last_offset)}
    }
