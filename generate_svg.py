# ... (Previous imports and get_base64_image function remain same, implicit context)
# We assume the imports and get_base64_image function are present above this block in the final file.
# BUT I need to provide the FULL file content to be safe with `replace_file_content` unless I use `MultiReplace`.
# I will output the FULL file again to avoid errors.

import base64
import os
import io

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: PIL/Pillow not found. Transparency might fail.")

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
            bg_color = datas[0]
            new_data = []
            for item in datas:
                if abs(item[0]-bg_color[0])<10 and abs(item[1]-bg_color[1])<10 and abs(item[2]-bg_color[2])<10:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        except:
            pass
    with open(file_path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

sprite_b64 = get_base64_image(sprite_path, True)
bg_b64 = get_base64_image(bg_path, False)

# SMIL Animation Logic
# Total Duration: 5s
# Coordinates:
# Floor Y = 232 (360-128)
# Jump Y = 72 (200-128)
# Dunk Y = 92 (220-128)

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="800" height="400" viewBox="0 0 800 400">
  <!-- Background -->
  <image href="{bg_b64}" xlink:href="{bg_b64}" width="800" height="400" x="0" y="0" preserveAspectRatio="none" />

  <!-- Player Group (Movement) -->
  <!-- We move a nested SVG viewport -->
  <svg width="128" height="128" viewBox="0 0 128 128" overflow="hidden">
     <!-- Position Animation of Container -->
     <animate attributeName="x" 
              values="-150; 450; 450; 580; 580; 580; 580" 
              keyTimes="0; 0.4; 0.42; 0.5; 0.55; 0.65; 1" 
              dur="5s" repeatCount="indefinite" />
     <animate attributeName="y" 
              values="232; 232; 232; 72; 92; 232; 232" 
              keyTimes="0; 0.4; 0.42; 0.5; 0.55; 0.65; 1" 
              dur="5s" repeatCount="indefinite" />

     <!-- Sprite Sheet Image -->
     <image href="{sprite_b64}" xlink:href="{sprite_b64}" width="512" height="256">
        <!-- Frame X Animation (Column) -->
        <!-- 
           0-40%: Run Cycle (0, -128, -256, -384...)
           Let's do 8 steps logic for run (5% each): 0, 1, 2, 3, 0, 1, 2, 3
           40-42%: Prep (Row 2 Col 1 -> X=0)
           42-50%: Jump (Row 2 Col 2 -> X=-128)
           50-55%: Dunk (Row 2 Col 3 -> X=-256)
           55-65%: Land (Row 2 Col 4 -> X=-384)
           65-100%: Land/Stay (X=-384)
        -->
        <animate attributeName="x" 
                 calcMode="discrete" 
                 values="0; -128; -256; -384; 0; -128; -256; -384; 0; -128; -256; -384; 0; -128; -256; -384; 0; -128; -256; -384"
                 keyTimes="0; 0.4; 0.42; 0.5; 0.55; 0.65; 1"
                 dur="5s" repeatCount="indefinite"
                 />
                 <!-- Correction: The 'values' list above must match 'keyTimes' count or use proportional.
                      With discrete, we need precise timing.
                      Let's simplify:
                      0.0 - 0.4 (Run): 8 frames. (0, -128, -256, -384 repeated).
                      0.4: Prep (0)
                      0.42: Jump (-128)
                      0.5: Dunk (-256)
                      0.55: Land (-384)
                      0.65: Stay (-384)
                      
                      KeyTimes length must match Values length.
                      Run Frames: 0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35
                      Action Frames: 0.40, 0.42, 0.50, 0.55, 0.65
                      Total 13 keyframes.
                  -->
        <animate attributeName="x" 
                 calcMode="discrete" 
                 values="0; -128; -256; -384; 0; -128; -256; -384; 0; -128; -256; -384; -384"
                 keyTimes="0; 0.05; 0.10; 0.15; 0.20; 0.25; 0.30; 0.35; 0.40; 0.42; 0.50; 0.55; 1.0"
                 dur="5s" repeatCount="indefinite" />

        <!-- Frame Y Animation (Row) -->
        <!-- 
           0-0.4: Row 1 (Y=0)
           0.4-1.0: Row 2 (Y=-128)
        -->
        <animate attributeName="y" 
                 calcMode="discrete" 
                 values="0; -128"
                 keyTimes="0; 0.4"
                 dur="5s" repeatCount="indefinite" />
     </image>
  </svg>
</svg>'''

with open(output_svg_path, "w", encoding='utf-8') as f:
    f.write(svg_content)

print(f"SVG regenerated (SMIL+xlink) at {output_svg_path}")
