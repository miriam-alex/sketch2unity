import csv
from jinja2 import Template

# Architectural reference context — pulled from your image descriptions
ARCH_REFERENCES = {
    "A": "Industrial infrastructure aesthetic — steel, raw brick, utilitarian.",
    "B": "Brutalist-influenced residential in dark brick with bold geometric massing.",
    "C": "Romanesque Revival — warm red brick, arched windows, rounded turrets.",
    "D": "Contemporary institutional — curved glass curtain wall, clean and corporate.",
    "E": "Mid-century modernist — red brick tower, exposed walkways, utilitarian.",
    "F": "Neoclassical civic — light gray stone, grand staircase, columned entry.",
    "G": "Industrial utilitarian — corrugated metal cladding, minimal fenestration.",
    "H": "Contemporary mid-rise — light brick, large windows, vertical accent fins.",
    "I": "Vernacular outer-borough — red brick tower over ground-floor retail.",
    "J": "Mid-century modest — flat brick facade, regular punched windows.",
    "K": "Contemporary mixed-use infill — glass and metal curtain wall over retail.",
    "L": "Eclectic mixed-era — older brick walk-ups alongside modern stucco infill.",
    "M": "Pre-war tenement — dark red brick, fire escapes, flat cornice line.",
    "N": "Modern high-rise commercial — glass curtain wall, dense urban core.",
    "O": "Mid-century utilitarian — light gray brick, flat and unornamented.",
    "P": "Mixed-scale urban layering — older masonry beside contemporary glass tower.",
    "Q": "Brownstone row houses — Italianate/Greek Revival, stoops, warm sandstone.",
    "R": "Federal/Greek Revival townhouses — cream brick, iron railings, restrained elegance.",
    "S": "Pre-war tenement walk-ups — rough stone/brick, ornate fire escapes, ground retail.",
    "T": "Mid-century modernist slab — light brick, ribbon windows, street setback.",
}

with open("ri_site_parsing.md") as f:
    base_prompt = f.read()
    PROMPT_TEMPLATE = Template(base_prompt + """
                               
    ## 👤 Participant Design Input

    ### Spatial Description
    {{ description }}

    ### Architectural Style Intent
    {{ arch_style }}
    {% if arch_context %}
    ### Architectural Reference (Image {{ arch_letter }})
    The participant referenced image {{ arch_letter }}: {{ arch_context }}
    Use this as a material and massing reference when generating image prompts.
    {% endif %}""")

    with open("participants.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            letter = row["arch_reference_letter"].strip().upper()
            arch_context = ARCH_REFERENCES.get(letter, "")
            
            prompt = PROMPT_TEMPLATE.render(
                description=row["description"],
                arch_style=row["arch_style"],
                arch_letter=letter if letter else None,
                arch_context=arch_context
            )
            
            with open(f"custom_prompts/{row['participant']}-prompt.txt", "w") as out:
                out.write(prompt)