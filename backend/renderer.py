def compose(expressions, geometry, decorations, palette, expression_id, deco_ids):
    tok = {
        "ink": palette["ink"], "corner": palette["corner"], "accent": palette["accent"],
        "body": palette["body"], "panel": palette.get("panel") or geometry["colors"]["panel"],
        "scene": palette["scene"], "blush": palette["blush"], "fluid": palette["fluid"],
    }

    def tokify(fragment):
        fragment = (fragment
                    .replace("#222222", "{{ink}}")
                    .replace("#D44A36", "{{corner}}")
                    .replace("#6EC6E8", "{{accent}}"))
        for k, v in tok.items():
            fragment = fragment.replace("{{" + k + "}}", v or "")
        return fragment

    sh = geometry["shadow"]
    W, H = geometry["body"]
    r = geometry["body_radius"]
    x1, y1 = geometry["corner"][0]
    y2 = geometry["corner"][1][1]
    body_path = (f"M{r} 0H{W - r}A{r} {r} 0 0 1 {W} {r}V{H - r}"
                 f"A{r} {r} 0 0 1 {W - r} {H}H{r}A{r} {r} 0 0 1 0 {H - r}V{r}A{r} {r} 0 0 1 {r} 0Z")
    corner_path = f"M{x1} {y1}H{W - r}A{r} {r} 0 0 0 {W} {H - r}V{y2}Z"

    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 560" width="780" height="560">']
    parts.append('<defs>'
                 f'<filter id="soft-shadow" filterUnits="userSpaceOnUse" x="-80" y="-80" width="760" height="540" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="{sh["blur_std_deviation"]}"/></filter>'
                 f'<filter id="contact-shadow" filterUnits="userSpaceOnUse" x="-80" y="-80" width="760" height="540" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="{sh["contact"]["blur_std_deviation"]}"/></filter>'
                 '</defs>')
    if tok["scene"]:
        parts.append(f'<rect width="780" height="560" fill="{tok["scene"]}"/>')
    parts.append('<g transform="translate(90 90)">')
    parts.append(f'<rect x="0" y="{sh["offset_y"]}" width="{W}" height="{H}" rx="{r}" fill="{sh["color"]}" opacity="{sh["opacity"]}" filter="url(#soft-shadow)"/>')
    parts.append(f'<rect x="0" y="{sh["contact"]["offset_y"]}" width="{W}" height="{H}" rx="{r}" fill="{sh["color"]}" opacity="{sh["contact"]["opacity"]}" filter="url(#contact-shadow)"/>')
    parts.append(f'<path d="{body_path}" fill="{tok["body"]}"/>')
    parts.append(f'<path d="{corner_path}" fill="{tok["corner"]}"/>')
    ex = next((e for e in expressions if e["id"] == expression_id), None)
    if ex is None:
        raise ValueError(f"找不到表情 {expression_id}")
    parts.append(tokify(ex["fragment"]))
    for did in deco_ids:
        d = next((x for x in decorations if x["id"] == did), None)
        if d is None:
            raise ValueError(f"找不到装饰 {did}")
        parts.append(tokify(d["fragment"]))
    parts.append("</g></svg>")
    return "".join(parts)


