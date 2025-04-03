import cv2
import numpy as np
from sklearn.cluster import KMeans
import colorsys

def load_and_process_image(image_path, resize_dim=(100, 100)):
    """Loads an image, converts to RGB, and resizes."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image from path: {image_path}")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, resize_dim, interpolation=cv2.INTER_AREA)
    return img_resized

def extract_dominant_colors(image, k=3):
    """Extracts the k dominant colors from an image using KMeans clustering."""
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10) # Set n_init explicitly
    kmeans.fit(pixels)

    dominant_colors = kmeans.cluster_centers_
    return dominant_colors.astype(int)

def get_mood_from_color(rgb_color):
    """Maps an RGB color to a mood based on its hue."""
    r, g, b = rgb_color / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    hue_deg = h * 360

    # Define mood based on hue ranges and lightness/saturation
    if l < 0.2: # Dark tones
        return "Moody / Melancholic"
    if l > 0.85 and s < 0.15: # Bright / White shades
        return "Uplifting / Hopeful"

    if 0 <= hue_deg < 30 or hue_deg >= 330: # Red shades
        return "Energetic / Passionate"
    elif 30 <= hue_deg < 75: # Yellow / Orange shades
        return "Happy / Cheerful"
    elif 75 <= hue_deg < 150: # Green shades
        return "Relaxed / Peaceful"
    elif 150 <= hue_deg < 270: # Blue shades
        return "Calm / Sad"
    else: # Magenta/Pink ranges, can be grouped or have a separate mood
        return "Mysterious / Playful" # Default fallback or specific mood

def analyze_image(image_path):
    """Analyzes an image to find dominant colors and determine the overall mood."""
    processed_image = load_and_process_image(image_path)
    dominant_colors = extract_dominant_colors(processed_image, k=3)
    # Determine mood based on the *most* dominant color (first cluster center)
    mood = get_mood_from_color(dominant_colors[0])
    return dominant_colors, mood