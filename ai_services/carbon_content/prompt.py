
soil_carbon_content_prompt = """
Task: Analyze the soil in the provided image. Act as a pedologist (soil scientist) to determine the soil's organic carbon content on a scale of 0.0 to 1.0.

Categorization Logic:

Category 1 (0.00 - 0.02): Highly oxidized, bright red/orange/yellow soils (Oxisols/Ultisols). Very low organic matter.

Category 2 (0.02 - 0.04): Light tan, beige, or grey soils. Low to moderate organic matter.

Category 3 (0.04 - 0.07): Medium to dark brown soils. Healthy organic matter levels.

Category 4 (0.07 - 0.15+): Deep dark brown to near-black soils. Rich in humus/organic carbon.

Output Requirement:

Provide a single Numerical Score (e.g., 0.012) within that category's range.

Constraint: Return ONLY score. Do not provide any additional prose, warnings, or explanations.
"""