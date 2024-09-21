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

# Oval Face: Narrow forehead and chin, high and wide cheekbones, subtly curved jawline. Most frame shapes work well. Use wide, bold, oversized frames (square, rectangular, trapezoid). Avoid narrow or heavily designed frames.
# Square Face: Broad forehead, wide angular jawline, strong jawline with equal width from forehead to jaw. Use rounded or oval frames to soften angular features. Rimless or semi-rimless styles work well. Avoid square or angular frames.
# Round Face: Forehead, cheeks, and chin have similar width with soft cheekbones and jawline. Full cheeks, few angles. Use angular, geometric frames (rectangular, square) to add definition. Cat-eye or upswept frames. Avoid round or small frames.
# Heart-Shaped Face: Wide forehead, narrow chin, high cheekbones. Find frames that are Winged-out frames, oval, bottom-heavy frames to balance narrow chin. Light-colored or rimless frames for a softer look.
# Diamond Face: Narrow forehead and chin, wider cheekbones, angular jawline. Use frames that are rimless or oval frames with strong browlines to balance features. Cat-eye, rectangle, or horn-rim frames. Avoid frames that accentuate angular features.
# Triangular Face: Narrow forehead, wide jawline and chin. Use frames that are bold on top and lighter on the bottom (aviators, cat-eye). Look for wider frames with heavy detailing at the top to balance the wider jaw.
#     Respond first with face shape decided. Then provide a short summary of the shapes of sunglasses that would be complimentary for that shape.


# When examining a face in an image, follow these guidelines to determine the correct face shape. After identifying the face shape, provide a recommendation on sunglasses styles that best suit the identified shape.

# Step-by-Step Process:
# Analyze the Forehead, Cheekbones, Jawline, and Chin:

# Focus on the width and proportions of these areas to identify which parts of the face are the widest or most prominent.
# Compare the Face to the Following Shape Categories:

# Round Face:

# Characteristics: A round face has soft angles with the width almost equal to the length. The cheeks are typically the widest part, and the jawline is rounded rather than angular.
# Sunglasses Recommendation: Angular frames like square or rectangular sunglasses work well to add definition to soft facial features.
# Square Face:

# Characteristics: A square face has a broad forehead, wide cheekbones, and a strong jawline with minimal curvature. The face appears to have straight, sharp lines.
# Sunglasses Recommendation: Rounded or oval sunglasses are ideal for softening the strong angles of a square face.
# Heart-Shaped Face:

# Characteristics: A heart-shaped face has a broad forehead and a narrower, tapered chin. The cheekbones are typically prominent, and the chin comes to a point.
# Sunglasses Recommendation: Aviator or round sunglasses help balance the broad forehead and draw attention away from the narrow chin.
# Oval Face:

# Characteristics: An oval face is well-proportioned, with the length of the face longer than the width, and a softly rounded jawline.
# Sunglasses Recommendation: Most sunglasses styles complement an oval face, as the balanced proportions allow for versatility.
# Triangle Face:

# Characteristics: A triangle face has a narrow forehead and broad jawline, with the width increasing as you move down the face.
# Sunglasses Recommendation: Cat-eye or round frames are ideal for balancing a narrow forehead and adding width to the upper portion of the face.
# Diamond Face:

# Characteristics: A diamond face is narrow at both the forehead and chin, with wide cheekbones being the most prominent feature.
# Sunglasses Recommendation: Oval or rimless frames work well to soften the angles of a diamond-shaped face and balance the cheekbones.
# Rectangle Face:

# Characteristics: A rectangular face is longer than it is wide, with a straight jawline and evenly spaced cheekbones and forehead. The face may appear angular or sharp.
# Sunglasses Recommendation: Oversized or wrap-around sunglasses help shorten the length of the face and add balance to its features.
# Task:
# Identify the Face Shape:

# Using the guidelines above, analyze the proportions of the face in the image. Determine which of the seven face shape categories (round, square, heart, oval, triangle, diamond, rectangle) best fits the facial structure.
# Respond first with the identified face shape.
# Provide a Sunglasses Recommendation:

# After identifying the face shape, recommend one or more styles of sunglasses that would complement the identified face shape, based on the guidelines provided above.


# Look at this image and decide which face shape is closest to the face in the image.

# Step-by-Step Process:
# Look at the Forehead, Cheekbones, Jawline, and Chin:

# Focus on the width and proportions of these areas to identify which parts of the face are the widest or most prominent.

# Compare the Face to the Following Shape Categories:
# Round: A round face has soft angles with the width almost equal to the length. The cheeks are typically the widest part, and the jawline is rounded rather than angular.
# Sunglasses Recommendation: Angular frames like square or rectangular sunglasses work well to add definition to soft facial features.

# Square: A square face has a broad forehead, wide cheekbones, and a strong jawline with minimal curvature. The face appears to have straight, sharp lines.
# Sunglasses Recommendation: Rounded or oval sunglasses are ideal for softening the strong angles of a square face.

# Heart-shaped: A heart-shaped face has a broad forehead and a narrower, tapered chin. The cheekbones are typically prominent, and the chin comes to a point.
# Sunglasses Recommendation: Aviator or round sunglasses help balance the broad forehead and draw attention away from the narrow chin.

# Oval: An oval face is well-proportioned, with the length of the face longer than the width, and a softly rounded jawline.
# Sunglasses Recommendation: Most sunglasses styles complement an oval face, as the balanced proportions allow for versatility.

# Triangle: A triangle face has a narrow forehead and broad jawline, with the width increasing as you move down the face.
# Sunglasses Recommendation: Cat-eye or round frames are ideal for balancing a narrow forehead and adding width to the upper portion of the face.

# Diamond: A diamond face is narrow at both the forehead and chin, with wide cheekbones being the most prominent feature.
# Sunglasses Recommendation: Oval or rimless frames work well to soften the angles of a diamond-shaped face and balance the cheekbones.

# Rectangular: A rectangular face is longer than it is wide, with a straight jawline and evenly spaced cheekbones and forehead. The face may appear angular or sharp.
# Sunglasses Recommendation: Oversized or wrap-around sunglasses help shorten the length of the face and add balance to its features.

# Task:
# Identify the Face Shape:
# Using the guidelines above, look at the proportions of the face in the image. Decide which of the seven face shape categories (round, square, heart, oval, triangle, diamond, rectangle) best fits the facial structure.
# Provide a Sunglasses Recommendation:
# After identifying the face shape, recommend one or more styles of sunglasses that would complement the identified face shape, based on the guidelines provided above.