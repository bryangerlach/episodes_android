import os
from PIL import Image, ImageDraw, ImageFont

def generate_app_icon():
    # Create assets/icon directory if it doesn't exist
    os.makedirs("assets/icon", exist_ok=True)
    
    # High resolution canvas (1024x1024)
    size = 1024
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Background with generous padding to prevent Android adaptive mask clipping
    # Keeping the core graphic smaller ensures it stays safely inside the circular/squircle crop mask
    margin = 120  # Increased margin for adaptive icon safe zone
    box = [margin, margin, size - margin, size - margin]
    draw.rounded_rectangle(box, radius=180, fill=(30, 41, 59, 255))
    
    # Inner border / glow
    inner_box = [margin + 12, margin + 12, size - margin - 12, size - margin - 12]
    draw.rounded_rectangle(inner_box, radius=160, outline=(51, 65, 85, 255), width=6)

    # 2. Draw TV Body (Scaled down to fit nicely within the safe zone)
    tv_left = 240
    tv_top = 300
    tv_right = size - 240
    tv_bottom = size - 280
    
    draw.rounded_rectangle(
        [tv_left, tv_top, tv_right, tv_bottom],
        radius=40,
        fill=(226, 232, 240, 255)
    )
    
    # 3. Draw TV Screen (Dark inset screen)
    screen_margin_x = 45
    screen_margin_y = 45
    screen_box = [
        tv_left + screen_margin_x,
        tv_top + screen_margin_y,
        tv_right - screen_margin_x,
        tv_bottom - screen_margin_y - 35
    ]
    draw.rounded_rectangle(screen_box, radius=20, fill=(15, 23, 42, 255))
    
    # 4. Draw Bold Uppercase Letter "E" and 4-Item Checklist
    screen_center_x = (screen_box[0] + screen_box[2]) / 2
    screen_center_y = (screen_box[1] + screen_box[3]) / 2
    
    e_offset_x = 60
    
    # Load bold system font paths
    font_paths = [
        "C:\\Windows\\Fonts\\arialbd.ttf",                    # Windows Arial Bold
        "C:\\Windows\\Fonts\\segoeuib.ttf",                   # Windows Segoe UI Bold
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", # Linux
        "/System/Library/Fonts/Helvetica.ttc"                 # macOS
    ]
    
    font = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, 190)
                break
            except IOError:
                continue
                
    if font is None:
        font = ImageFont.load_default()

    text = "E"
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = screen_center_x + e_offset_x - (text_width / 2) - bbox[0]
    text_y = screen_center_y - (text_height / 2) - bbox[1]
    
    # Draw bold uppercase 'E'
    draw.text(
        (text_x, text_y), 
        text, 
        fill=(56, 189, 248, 255), 
        font=font, 
        stroke_width=5, 
        stroke_fill=(56, 189, 248, 255)
    )

    # Draw 4-line List design to the left of the bold 'E'
    list_center_x = screen_center_x - 110
    row_spacing = 35
    list_start_y = screen_center_y - (1.5 * row_spacing) - 5
    
    for i in range(4):
        current_y = list_start_y + (i * row_spacing)
        
        if i == 0:
            # Top checked item
            draw.rounded_rectangle(
                [list_center_x - 12, current_y - 5, list_center_x + 2, current_y + 10],
                radius=2,
                fill=(56, 189, 248, 255)
            )
            draw.rounded_rectangle(
                [list_center_x + 16, current_y, list_center_x + 65, current_y + 5],
                radius=2,
                fill=(56, 189, 248, 255)
            )
        else:
            # Pending checklist items
            draw.rounded_rectangle(
                [list_center_x - 12, current_y - 5, list_center_x + 2, current_y + 10],
                radius=2,
                outline=(148, 163, 184, 255),
                width=2
            )
            draw.rounded_rectangle(
                [list_center_x + 16, current_y, list_center_x + 65, current_y + 5],
                radius=2,
                fill=(148, 163, 184, 255)
            )

    # 5. TV Details & Stand
    draw.ellipse([tv_right - 75, tv_bottom - 30, tv_right - 60, tv_bottom - 15], fill=(34, 197, 94, 255))
    
    stand_width = 130
    stand_height = 18
    stand_y = tv_bottom
    center_x = size / 2
    draw.rounded_rectangle(
        [center_x - stand_width/2, stand_y, center_x + stand_width/2, stand_y + stand_height], 
        radius=6, 
        fill=(148, 163, 184, 255)
    )

    output_path = "assets/icon/app_icon.png"
    img.save(output_path, "PNG")
    print(f"Successfully generated padded adaptive app icon at: {output_path}")

if __name__ == "__main__":
    generate_app_icon()