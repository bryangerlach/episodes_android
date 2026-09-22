import os
from PIL import Image, ImageDraw, ImageFont

def generate_app_icon():
    os.makedirs("assets/icon", exist_ok=True)
    
    size = 1024
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Modern Rounded Square App Base (Deep Blue/Slate Gradient fill simulation)
    margin = 80  # Optimized safe zone padding
    box = [margin, margin, size - margin, size - margin]
    draw.rounded_rectangle(box, radius=220, fill=(15, 23, 42, 255))  # Dark sleek background
    
    # Inner subtle border accent
    inner_box = [margin + 16, margin + 16, size - margin - 16, size - margin - 16]
    draw.rounded_rectangle(inner_box, radius=200, outline=(30, 41, 59, 255), width=8)

    # 2. Central Vibrant Blue Screen/Card Badge
    badge_margin = 200
    badge_box = [badge_margin, badge_margin, size - badge_margin, size - badge_margin]
    draw.rounded_rectangle(badge_box, radius=120, fill=(37, 99, 235, 255))  # Vibrant blue accent
    
    # Load bold font
    font_paths = [
        "C:\\Windows\\Fonts\\arialbd.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc"
    ]
    
    font = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, 320)  # Large, bold letterform
                break
            except IOError:
                continue
                
    if font is None:
        font = ImageFont.load_default()

    # 3. Draw Bold White "E" Centered
    text = "E"
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    center_x = size / 2
    center_y = size / 2
    
    text_x = center_x - (text_width / 2) - bbox[0]
    text_y = center_y - (text_height / 2) - bbox[1] - 10
    
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)

    # 4. Small Status Dot (Tracking / Active indicator)
    dot_center_x = size - 260
    dot_center_y = 260
    dot_radius = 24
    draw.ellipse(
        [dot_center_x - dot_radius, dot_center_y - dot_radius, 
         dot_center_x + dot_radius, dot_center_y + dot_radius], 
        fill=(34, 197, 94, 255)  # Fresh green completion dot
    )

    output_path = "assets/icon/app_icon.png"
    img.save(output_path, "PNG")
    print(f"Successfully generated modern minimalist app icon at: {output_path}")

if __name__ == "__main__":
    generate_app_icon()