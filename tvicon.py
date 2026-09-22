import os
from PIL import Image, ImageDraw

def generate_app_icon():
    os.makedirs("assets/icon", exist_ok=True)
    
    size = 1024
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Background with safe zone padding
    margin = 80
    box = [margin, margin, size - margin, size - margin]
    draw.rounded_rectangle(box, radius=220, fill=(29, 78, 216, 255))
    
    # Inner subtle accent border
    inner_box = [margin + 12, margin + 12, size - margin - 12, size - margin - 12]
    draw.rounded_rectangle(inner_box, radius=200, outline=(59, 130, 246, 255), width=6)

    center_x = size / 2
    center_y = size / 2

    # 2. Draw 3 Shorter, Thicker Horizontal List Bars / Cards
    bar_width = 400  # More compact width
    bar_height = 110
    bar_radius = 24
    row_spacing = 135
    
    # Center the stack vertically
    start_y = center_y - row_spacing  
    
    for i in range(3):
        current_y = start_y + (i * row_spacing)
        bar_left = center_x - (bar_width / 2)
        bar_top = current_y - (bar_height / 2)
        bar_right = center_x + (bar_width / 2)
        bar_bottom = current_y + (bar_height / 2)
        
        if i == 0:
            # Top bar (active/highlighted white card)
            draw.rounded_rectangle([bar_left, bar_top, bar_right, bar_bottom], radius=bar_radius, fill=(255, 255, 255, 255))
            
            # Green check / status box on the left inside the bar
            check_box = [bar_left + 24, bar_top + 24, bar_left + 86, bar_bottom - 24]
            draw.rounded_rectangle(check_box, radius=14, fill=(34, 197, 94, 255))
            
            # Text/content lines inside the bar
            line1_box = [bar_left + 110, bar_top + 32, bar_right - 30, bar_top + 54]
            draw.rounded_rectangle(line1_box, radius=6, fill=(29, 78, 216, 255))
            line2_box = [bar_left + 110, bar_top + 66, bar_right - 100, bar_top + 84]
            draw.rounded_rectangle(line2_box, radius=5, fill=(147, 197, 253, 255))
        else:
            # Secondary/pending bars (translucent light blue cards)
            draw.rounded_rectangle([bar_left, bar_top, bar_right, bar_bottom], radius=bar_radius, fill=(191, 219, 254, 110))
            
            # Pending indicator box on the left
            check_box = [bar_left + 24, bar_top + 24, bar_left + 86, bar_bottom - 24]
            draw.rounded_rectangle(check_box, radius=14, fill=(191, 219, 254, 200))
            
            # Content lines inside
            line1_box = [bar_left + 110, bar_top + 32, bar_right - 30, bar_top + 54]
            draw.rounded_rectangle(line1_box, radius=6, fill=(255, 255, 255, 200))
            line2_box = [bar_left + 110, bar_top + 66, bar_right - 120, bar_top + 84]
            draw.rounded_rectangle(line2_box, radius=5, fill=(255, 255, 255, 120))

    output_path = "assets/icon/app_icon.png"
    img.save(output_path, "PNG")
    print(f"Successfully generated compact thick list bar app icon at: {output_path}")

if __name__ == "__main__":
    generate_app_icon()