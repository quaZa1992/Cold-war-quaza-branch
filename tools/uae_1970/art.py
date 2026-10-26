# IMPERIA CW — Cold War: uae 1970 — art.
"""Native MD artwork aliases for the approved UAE 1970 focus programme.

The compiler owns writing the returned files. Importing this module and calling
``build`` never alter textures, global GFX registrations or the focus-view GUI.
"""

from pathlib import Path
import re
from event_pictures import gfx_output


ROOT = Path(__file__).resolve().parents[2]
PREFIX = "COLDWAR_UAE_"

STARTING_SPIRIT_ICONS = {
    "treaty_dependence": "GFX_idea_guided_by_england",
    "fragmented_authority": "GFX_idea_disjointed_government",
    "unequal_development": "GFX_idea_poor_economy",
    "scarce_specialists": "GFX_idea_neglected_education",
    "water_power": "GFX_idea_water_crisis",
    "narrow_revenues": "GFX_idea_fossil_fuel_industry",
    "expatriate_workforce": "GFX_idea_uae_expat",
    "maritime_livelihoods": "GFX_idea_maritime_industry",
}

PROGRAMME_ICONS = {
    "union": "GFX_idea_national_unity",
    "monarchy": "GFX_idea_monarchy2",
    "constitutional": "GFX_idea_political_freedom",
    "arab": "GFX_idea_nationalism",
    "left": "GFX_idea_collective_soceity",  # Native MD sprite spelling.
    "islah": "GFX_idea_religion_sunni",
    "oil": "GFX_idea_fossil_fuel_industry",
    "commerce": "GFX_idea_trade",
    "society": "GFX_idea_dutch_economic_education",
    "defence": "GFX_idea_army_officer",
    "diplomacy": "GFX_idea_international_treaty2",
    "british": "GFX_idea_british_imperialism",
}

TREATY_ICONS = {
    "starting": "GFX_idea_guided_by_england",
    "scheduled": "GFX_idea_international_treaty",
    "protection": "GFX_idea_british_imperialism",
    "fulfilled": "GFX_idea_national_unity",
    "friendship": "GFX_idea_international_treaty2",
}


def _full_id(identifier):
    identifier = str(identifier)
    return identifier if identifier.startswith(PREFIX) else PREFIX + identifier


def focus_icon(focus_id):
    """The exact ``icon`` value for a compiled focus."""
    return "GFX_" + _full_id(focus_id)


def spirit_picture(spirit_id):
    """The idea ``picture`` value, without the engine's ``GFX_idea_`` prefix."""
    return _full_id(spirit_id)


def programme_picture(group_id):
    """The dynamic-modifier/idea ``picture`` value for one approved programme."""
    return _full_id(group_id) + "_programme"


def _native_textures(source="interface/goals.gfx"):
    """Resolve the unchanged native MD registrations, not our emitted aliases."""
    text = (ROOT / source).read_text(encoding="utf-8-sig")
    pattern = re.compile(
        r'\b(?:spriteType|SpriteType)\s*=\s*\{\s*name\s*=\s*"([^"]+)"'
        r'\s+texture[Ff]ile\s*=\s*"([^"]+)"'
    )
    return {match[1]: match[2].replace("\\", "/") for match in pattern.finditer(text)}


def _sprite(name, texture):
    return [
        "\tspriteType = {",
        f'\t\tname = "{name}"',
        f'\t\ttexturefile = "{texture}"',
        "\t}",
    ]


def _shine(name, texture):
    # This is the native interface/goals_shine.gfx grammar. The logical .lua
    # effect alias is supplied by HOI4; it is not a texture to create or rename.
    lines = [
        "\tspriteType = {",
        f'\t\tname = "{name}_shine"',
        f'\t\ttexturefile = "{texture}"',
        '\t\teffectFile = "gfx/FX/buttonstate.lua"',
    ]
    for rotation in (-90, 90):
        lines.extend([
            "\t\tanimation = {",
            f'\t\t\tanimationmaskfile = "{texture}"',
            '\t\t\tanimationtexturefile = "gfx/interface/goals/shine_overlay.dds"',
            f"\t\t\tanimationrotation = {rotation}.0",
            "\t\t\tanimationlooping = no",
            "\t\t\tanimationtime = 0.75",
            "\t\t\tanimationdelay = 0",
            '\t\t\tanimationblendmode = "add"',
            '\t\t\tanimationtype = "scrolling"',
            "\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }",
            "\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }",
            "\t\t}",
        ])
    lines.extend(["\t\tlegacy_lazy_load = no", "\t}"])
    return lines


def build(data):
    """Return dedicated plain/shine GFX files using approved native pixels.

    Focuses use ``GFX_<full focus ID>``. National spirits use picture values
    returned by ``spirit_picture`` or ``programme_picture``. Accepted UK/UAE
    treaty spirits share appropriate native national-spirit art, with separate IDs.
    """
    native = _native_textures()
    native_ideas = _native_textures("interface/MD_ideas.gfx")
    approved_icons = {node["icon"] for node in data["nodes"]}
    aliases = {}
    focuses = {}

    def register(alias, icon, national_spirit=False):
        registry = native_ideas if national_spirit else native
        if not national_spirit and icon not in approved_icons:
            raise ValueError(f"Unapproved UAE artwork: {icon}")
        if icon not in registry:
            raise ValueError(f"Missing native MD sprite: {icon}")
        texture = registry[icon]
        if national_spirit and not texture.lower().startswith("gfx/interface/ideas/"):
            raise ValueError(f"National spirit must use native idea artwork: {icon}")
        path = ROOT / texture
        if not path.is_file():
            raise FileNotFoundError(path)
        # Every selected approved native source is DDS. Preserve its decoded
        # dimensions, alpha and pixels by referencing it directly.
        with path.open("rb") as stream:
            magic = stream.read(4)
        if path.suffix.lower() != ".dds" or magic != b"DDS ":
            raise ValueError(f"Expected an existing native DDS texture: {path}")
        if alias in aliases and aliases[alias] != texture:
            raise ValueError(f"Conflicting UAE sprite alias: {alias}")
        aliases[alias] = texture
        return texture

    for node in data["nodes"]:
        alias = focus_icon(node["id"])
        focuses[alias] = register(alias, node["icon"])

    for spirit in data["starting_spirits"]:
        suffix = spirit["id"].removeprefix(PREFIX)
        register("GFX_idea_" + spirit_picture(spirit["id"]), STARTING_SPIRIT_ICONS[suffix], national_spirit=True)

    for group in data["groups"]:
        register("GFX_idea_" + programme_picture(group["id"]), PROGRAMME_ICONS[group["id"]], national_spirit=True)

    for agreement in data.get("british_treaties", {}).get("variants", []):
        for role in ("uk_spirit", "uae_spirit"):
            register("GFX_idea_" + spirit_picture(agreement[role]), TREATY_ICONS[agreement["id"]], national_spirit=True)

    # The prime minister's office is separate from the president/party leader.
    # Politics owns these status-only ideas; use native civil-office spirit art.
    for suffix in ("prime_minister_maktoum", "prime_minister_rashid"):
        register("GFX_idea_" + spirit_picture(suffix), "GFX_idea_generic_government", national_spirit=True)

    plain = [
        "# COLDWAR UAE 1970 | native MD focus art and dedicated national-spirit art.",
        "spriteTypes = {",
    ]
    shine = [
        "# COLDWAR UAE 1970 | native MD completion shine and matching source masks.",
        "spriteTypes = {",
    ]
    for alias, texture in sorted(aliases.items()):
        plain.extend(_sprite(alias, texture))
    for alias, texture in sorted(focuses.items()):
        shine.extend(_shine(alias, texture))
    plain.append("}")
    shine.append("}")
    return {
        **gfx_output(),
        "interface/COLDWAR_UAE_1970_goals.gfx": "\n".join(plain) + "\n",
        "interface/COLDWAR_UAE_1970_goals_shine.gfx": "\n".join(shine) + "\n",
    }
