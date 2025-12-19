import base64
import os

# Paths
workspace_dir = r"d:\domenico3622"
sprite_path = os.path.join(workspace_dir, "spritesheet.png")
output_svg_path = os.path.join(workspace_dir, "slam_dunk.svg")

# 1. Read and Base64 encode the sprite
with open(sprite_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    data_uri = f"data:image/png;base64,{encoded_string}"

# 2. Define the SVG content with pure CSS animation
# We need to replicate the 'Run -> Jump -> Dunk' sequence using CSS Keyframes only.
# Timeline (Total 4s):
# 0-2s: Run from left to hoop
# 2.0-2.1s: Prep
# 2.1-2.5s: Jump Up
# 2.5-2.7s: Mid Air
# 2.7-2.9s: Dunk
# 2.9-3.2s: Land
# 3.2-4.0s: Stay/Reset

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml" style="width:100%;height:100%;overflow:hidden;position:relative;background:#e8cd9a;">
      
      <!-- CSS Styles -->
      <style>
        .court {{
            width: 100%; height: 100%;
            background-image: 
                linear-gradient(90deg, transparent 49%, rgba(0,0,0,0.1) 50%, transparent 51%),
                linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px);
            background-size: 100px 100%, 100% 40px;
            position: absolute; top:0; left:0;
        }}
        .hoop-stand {{
            position: absolute; right: 50px; bottom: 150px;
            width: 20px; height: 250px; background: #555;
        }}
        .backboard {{
            position: absolute; top: 0; right: 0;
            width: 120px; height: 90px; background: white;
            border: 2px solid #ccc; box-sizing: border-box;
        }}
        .backboard::after {{
            content: ""; display: block;
            width: 50px; height: 40px; border: 3px solid red;
            position: absolute; bottom: 10px; left: 32px;
        }}
        .rim {{
            width: 60px; height: 5px; background: orange;
            position: absolute; bottom: 10px; right: 30px;
            border-radius: 50%;
        }}
        
        .sakuragi {{
            width: 128px; height: 128px;
            position: absolute; bottom: 40px; left: -150px;
            background-image: url('{data_uri}');
            background-size: 400% 200%;
            image-rendering: pixelated;
            
            /* Master Animation */
            animation: sequence-move 5s linear infinite, sequence-sprite 5s step-end infinite;
        }}

        @keyframes sequence-move {{
            0% {{ left: -150px; bottom: 40px; }}
            40% {{ left: 450px; bottom: 40px; }} /* Run duration */
            42% {{ left: 450px; bottom: 40px; }} /* Prep pause */
            50% {{ left: 580px; bottom: 200px; }} /* Jump peak */
            55% {{ left: 580px; bottom: 180px; }} /* Dunk drop */
            65% {{ left: 580px; bottom: 40px; }} /* Land */
            100% {{ left: 580px; bottom: 40px; }} /* Wait */
        }}

        @keyframes sequence-sprite {{
            /* Running (Cycle 0,1,2) */
            0% {{ background-position: 0% 0%; }}
            5% {{ background-position: 33.33% 0%; }}
            10% {{ background-position: 66.66% 0%; }}
            15% {{ background-position: 0% 0%; }}
            20% {{ background-position: 33.33% 0%; }}
            25% {{ background-position: 66.66% 0%; }}
            30% {{ background-position: 0% 0%; }}
            35% {{ background-position: 33.33% 0%; }}
            
            /* Prep (Frame 4) */
            40% {{ background-position: 100% 0%; }}
            
            /* Jump Up (Frame 5) */
            42% {{ background-position: 0% 100%; }}
            
            /* Mid Air (Frame 6) */
            48% {{ background-position: 33.33% 100%; }}
            
            /* Dunk (Frame 7) */
            52% {{ background-position: 66.66% 100%; }}
            
            /* Land (Frame 8) */
            64% {{ background-position: 100% 100%; }}
            
            /* Reset/Blank or Stand */
            100% {{ background-position: 100% 100%; }}
        }}

      </style>

      <div class="court">
          <div class="hoop-stand">
              <div class="backboard">
                  <div class="rim"></div>
              </div>
          </div>
          <div class="sakuragi"></div>
      </div>

    </div>
  </foreignObject>
</svg>'''

with open(output_svg_path, "w", encoding='utf-8') as f:
    f.write(svg_content)

print(f"SVG generated at {output_svg_path}")
