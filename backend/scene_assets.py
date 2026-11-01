"""Small foreground props sharing the character's palette and safe attachment area."""

FRAGMENTS = {
    'book': ('书本', '<path d="M245 286Q280 276 315 291Q350 276 385 286V355Q350 345 315 360Q280 345 245 355Z" fill="{{panel}}"/><path d="M311 291H319V358H311Z" fill="{{accent}}"/><path d="M257 300H297V306H257ZM257 315H297V321H257ZM332 300H372V306H332ZM332 315H372V321H332Z" fill="{{ink}}" opacity=".45"/>'),
    'wallet': ('账本', '<rect x="255" y="281" width="120" height="80" rx="12" fill="{{accent}}"/><rect x="265" y="290" width="100" height="62" rx="6" fill="{{panel}}"/><path d="M283 304H321V310H283ZM283 320H312V326H283Z" fill="{{ink}}"/><circle cx="344" cy="324" r="14" fill="{{corner}}"/>'),
    'check': ('完成', '<circle cx="315" cy="322" r="40" fill="{{accent}}"/><path d="M289 322L307 341L344 305L336 297L307 325L297 314Z" fill="{{panel}}"/>'),
    'search': ('查找', '<circle cx="303" cy="312" r="29" fill="{{accent}}"/><circle cx="303" cy="312" r="18" fill="{{panel}}"/><path d="M321 330L330 321L365 350L354 361Z" fill="{{ink}}"/>'),
    'bell': ('提醒', '<path d="M280 335V312Q280 283 315 283Q350 283 350 312V335L362 345H268Z" fill="{{accent}}"/><circle cx="315" cy="351" r="10" fill="{{corner}}"/><circle cx="315" cy="285" r="6" fill="{{corner}}"/>'),
    'chart': ('进度', '<rect x="255" y="281" width="120" height="80" rx="8" fill="{{panel}}"/><path d="M273 330H290V348H273ZM305 312H322V348H305ZM337 294H354V348H337Z" fill="{{accent}}"/>'),
}


def scene_decorations():
    return [dict(id='scene-'+key, name=name, group='foreground', bbox=[245, 280, 385, 365],
                 covers_eyes=False, fragment=fragment) for key, (name, fragment) in FRAGMENTS.items()]
