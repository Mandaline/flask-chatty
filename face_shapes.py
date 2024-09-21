face_shapes_guide = """
	Round: A round face has soft angles with the width almost equal to the length. The cheeks are typically the widest part, and the jawline is rounded rather than angular.
	Sunglasses Recommendation: Angular frames like square or rectangular sunglasses work well to add definition to soft facial features.

	Square: A square face has a broad forehead, wide cheekbones, and a strong jawline with minimal curvature. The face appears to have straight, sharp lines.
	Sunglasses Recommendation: Rounded or oval sunglasses are ideal for softening the strong angles of a square face.

	Heart-shaped: A heart-shaped face has a broad forehead and a tapered chin. The cheekbones are typically prominent.
	Sunglasses Recommendation: Aviator or round sunglasses help balance the broad forehead and draw attention away from the narrow chin.

	Oval: An oval face is well-proportioned, with the length of the face longer than the width, and a softly rounded jawline.
	Sunglasses Recommendation: Most sunglasses styles complement an oval face, as the balanced proportions allow for versatility.

	Triangle: A triangle face has a narrow forehead and broad jawline, with the width increasing as you move down the face.
	Sunglasses Recommendation: Cat-eye or round frames are ideal for balancing a narrow forehead and adding width to the upper portion of the face.

	Diamond: A diamond face is narrow at both the forehead and chin, with wide cheekbones being the most prominent feature.
	Sunglasses Recommendation: Oval or rimless frames work well to soften the angles of a diamond-shaped face and balance the cheekbones.

	Rectangular: A rectangular face is longer than it is wide, with a straight jawline and evenly spaced cheekbones and forehead. The face may appear angular or sharp.
	Sunglasses Recommendation: Oversized or wrap-around sunglasses help shorten the length of the face and add balance to its features.
"""

face_shapes_guide_prompt = f"""
	Look at this image and decide which face shape is closest to the face in the image.

	Step-by-Step Process:
	Look at the Forehead, Cheekbones, Jawline, and Chin:

	Focus on the width and proportions of these areas to identify which parts of the face are the widest or most prominent.

	Compare the Face to the Following Shape Categories:
  	{face_shapes_guide}

	Task:
	Identify the Face Shape:
	Using the guidelines above, look at the proportions of the face in the image. Decide which of the seven face shape categories (round, square, heart, oval, triangle, diamond, rectangle) best fits the facial structure.
	Provide a Sunglasses Recommendation:
	After identifying the face shape, recommend one or more styles of sunglasses that would complement the identified face shape, based on the guidelines provided above.
"""

sunglass_styles= """
	Aviator:
	Description: Classic teardrop shape, thin metal frame, often with a double bridge. Known for their military origin and sleek look.
	Best for: Square, oval, diamond, triangle, and heart-shaped faces. The curved teardrop lens balances strong jawlines and adds softness to angular features.

	Wayfarer:
	Description: Thick, trapezoidal plastic frame with a flat browline. Known for their timeless and versatile look, popular since the 1950s. This style features a thicker plastic frame and a broad upper rim that goes out to a shark-fin-like point.
	Best for: Oval, round, diamond and heart-shaped faces. The defined shape adds structure to softer facial features and works well with balanced proportions.

	Cat-Eye:
	Description: Upswept, winged frame, popular for a retro, feminine look. The sharp edges lift the eye area for a more dramatic effect.
	Best for: Round, heart, triangle, diamond and oval faces. The upward tilt elongates the face and sharpens softer features, especially on round face shapes.

	Round:
	Description: Circular lenses that give off a retro, vintage vibe. Frames can be thin or thick, often seen in metal or plastic materials.
	Best for: Square, oval, diamond, triangle and heart-shaped faces. The round lenses soften angular lines, providing contrast to sharper features.

	Geometric:
	Description: Sunglasses with angular shapes, such as hexagonal or square lenses. Bold and modern, these styles make a statement.
	Best for: Round and oval faces. The sharp angles add structure to softer features and balance rounded facial shapes.

	Oversized:
	Description: Large lenses that cover more of the face, often seen in high fashion. Provides additional coverage and a bold statement.
	Best for: Oval and round faces though the best-suited face shapes for this style depend on the frame shape of each unique pair.

	Wraparound:
	Description: Curved lenses that wrap around the face for full coverage, often used in sports for their functional protection.
	Best for: Oval and square faces. The wide design balances more angular features, especially in sporty or active environments.

	Rectangle:
	Description: Straight, rectangular lenses that add boldness and structure. Often seen in both casual and sporty styles.
	Best for: Round, diamond, heart-shaped and oval faces. The rectangular shape adds angularity and sharpness to rounder facial features.

	Squared: 
	Square sunglasses are characterized by their angular frames and broad temples. Offering a modern twist on the classic design, they have four nearly equal sides that create a balanced and symmetrical look. 
	Best for: Ideal for softening rounded facial features, these sunglasses are a favorite for those with round or oval face shapes. 

	Oval:
	Oval sunglasses are defined by their smooth, curved design. These frames have rounded edges, lending a gentle and soft aesthetic to the wearer's look. 
	Best for: Heart-shaped, oval, square, round, and diamond faces. Incredibly versatile, they flatter a range of face shapes, especially those with more angular or square features. 

	Browline:
	Description: Frame with a thick browline along the top, while the lower half of the lenses is rimless or thinly rimmed. Vintage style, reminiscent of the 1950s.
	Best for: Oval, round, square, triangle and diamond faces. The strong browline adds definition and draws attention to the upper half of the face.

	Sport:
	Description: Functional design, often with wraparound lenses and impact-resistant materials for active use.
	Best for: Oval and square faces. The sporty design complements sharp or well-proportioned facial features.

	Shield:
	Description: Large, single-lens design that stretches across both eyes, offering a futuristic look with maximum sun protection.
	Best for: Oval, round and square faces. The bold, oversized lens suits those with stronger jawlines or well-balanced features.

	Frame Types:
	Rimless: No visible frame, lenses connected directly to the temples and nose bridge.
	Semi-Rimless: Frame on the top or bottom only, minimalist look with more structure.
	Full-Rim: Frame surrounds the entire lens for durability and bold style.
	Geometric: Angular shapes like hexagons or squares, often with full or semi-rimless frames.

	Lens types:
	Polarized lenses: have a chemical coating that effectively reduces glare. As a result, the wearer can see images and colors more clearly and vividly. Polarization is ideal for engaging in water activities, such as fishing or boating, or for those particularly sensitive to glare. They come in grey, brown and black colors.
	Mirrored Lenses: With mirrored lenses, a reflective film is applied to the outside surface of the lenses. This film reduces visible light and some glare, providing a more comfortable viewing experience when in environments with bright, harsh light.

	Colors: 
	For plastic frames: Classic black, grey, translucent, white, dark brown, light brown, ash brown, warm brown and Tortoiseshell, which are dark brown and made from plastical material that replicates the look and pattern of a tortoise shell.
	For metal: Silver, Gold, Black

	Materials:
	Metal: Durable, sleek, commonly used for aviators, browline, and rimless styles. Common metals include titanium, aluminum, and stainless steel.
	Acetate/Plastic: Lightweight and versatile, often used for wayfarers, cat-eye, and oversized styles. Acetate is highly durable and comes in a wide range of colors and patterns.
	Glossy or matte finish
"""