import base64
import os
import io

# Try importing PIL for image manipulation (transparency)
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: PIL/Pillow not found. Image transparency processing might be skipped.")

# Paths
workspace_dir = r"d:\domenico3622"
sprite_path = os.path.join(workspace_dir, "sakuragi_new.png")
bg_path = os.path.join(workspace_dir, "court_bg.png")
output_svg_path = os.path.join(workspace_dir, "slam_dunk.svg")

def get_base64_image(file_path, make_transparent=False):
    if not os.path.exists(file_path):
        return ""
    
    if make_transparent and HAS_PIL:
        try:
            img = Image.open(file_path).convert("RGBA")
            datas = img.getdata()
            
            # Get background color from top-left pixel
            bg_color = datas[0]
            # Threshold for similarity? For pixel art, exact match usually works if it's a solid block.
            # But generated images might have noise.
            # We'll stick to simple exact match of the corner pixel for now or a known key color.
            # Assuming the generation used a distinct background.
            
            new_data = []
            for item in datas:
                # If pixel matches background color (within small tolerance), make it transparent
                if abs(item[0] - bg_color[0]) < 10 and abs(item[1] - bg_color[1]) < 10 and abs(item[2] - bg_color[2]) < 10:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            
            img.putdata(new_data)
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            encoded_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return f"data:image/png;base64,{encoded_string}"
        except Exception as e:
            print(f"Error processing image {file_path}: {e}")
            # Fallback to normal read
            pass

    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded_string}"

# Get Base64 strings
# Sprite needs transparency
sprite_b64 = get_base64_image(sprite_path, make_transparent=True)
# Background is opaque
bg_b64 = get_base64_image(bg_path, make_transparent=False)


# SVG Construction
# Key Changes:
# 1. Background image replaces CSS court.
# 2. Sprite keyframes adapted for new sheet layout (assumed 4 run frames, etc.)
# New Sheet Layout:
# Row 1: Run 1, Run 2, Run 3, Run 4? (Based on 4 columns typically)
# Row 2: Jump, Mid, Dunk, Land? 
# We need to guess the exact layout or trial-and-error. 
# Visual inspection of the generated image earlier (if I could see it) would help.
# Assuming standard 4x2 grid based on prompt.

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml" style="width:100%;height:100%;overflow:hidden;position:relative;">
      
      <!-- CSS Styles -->
      <style>
        .container {{
            width: 100%; height: 100%;
            position: absolute; top:0; left:0;
            background-image: url('{bg_b64}');
            background-size: cover;
            background-position: center;
        }}
        
        .sakuragi {{
            width: 128px; height: 128px;
            position: absolute; bottom: 40px; left: -150px;
            background-image: url('{sprite_b64}');
            background-size: 400% 200%; /* 4 columns, 2 rows */
            image-rendering: pixelated;
            z-index: 10;
            
            /* Master Animations */
            animation: sequence-move 5s linear infinite, sequence-sprites 5s step-end infinite;
        }}

        @keyframes sequence-move {{
            0% {{ left: -150px; bottom: 40px; }}
            40% {{ left: 450px; bottom: 40px; }} /* Run to paint */
            42% {{ left: 450px; bottom: 40px; }} /* Prep */
            50% {{ left: 580px; bottom: 200px; }} /* Jump peak */
            55% {{ left: 580px; bottom: 180px; }} /* Dunk */
            65% {{ left: 580px; bottom: 40px; }} /* Land */
            100% {{ left: 580px; bottom: 40px; }} /* Stay */
        }}

        @keyframes sequence-sprites {{
            /* Running Dribble (Row 1: 0-3) */
            0% {{ background-position: 0% 0%; }}
            5% {{ background-position: 33.33% 0%; }}
            10% {{ background-position: 66.66% 0%; }}
            15% {{ background-position: 100% 0%; }} /* 4th run frame if exists, else cycle */
            20% {{ background-position: 0% 0%; }}
            25% {{ background-position: 33.33% 0%; }}
            30% {{ background-position: 66.66% 0%; }}
            35% {{ background-position: 100% 0%; }}
            
            /* Prep (Last run frame or Frame 5) - Let's use Frame 5 (Row 2 Col 1) */
            40% {{ background-position: 0% 100%; }}
            
            /* Jump Up (Frame 6) */
            43% {{ background-position: 33.33% 100%; }}
            
            /* Dunk (Frame 7) */
            50% {{ background-position: 66.66% 100%; }}
            
            /* Land (Frame 8) */
            60% {{ background-position: 100% 100%; }}
            
            /* Reset */
            100% {{ background-position: 100% 100%; }}
        }}

      </style>

      <div class="container">
          <!-- Character -->
          <div class="sakuragi"></div>
      </div>

    </div>
  </foreignObject>
</svg>'''

with open(output_svg_path, "w", encoding='utf-8') as f:
    f.write(svg_content)

print(f"SVG regenerated at {output_svg_path}")

