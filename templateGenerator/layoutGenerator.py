import re
import os
from typing import Dict, List, Tuple, Optional

class LayoutGenerator:
    def __init__(self):
        # Mapping from image names to layout variable names
        self.name_mapping = {
            "GainKnob": "GainKnob",
            "LcQ": "LCQ",
            "LcFreq": "LCFreq", 
            "Bell1Freq": "Bell1Freq",
            "Bell1Gain": "Bell1Gain",
            "Bell1Q": "Bell1Q",
            "Bell2Freq": "Bell2Freq",
            "Bell2Gain": "Bell2Gain",
            "Bell2Q": "Bell2Q",
            "HSFreq": "HSFreq",
            "HSGain": "HSGain",
            "HSq": "HSQ",
            "outputGain": "OutputGain"
        }
    
    def parse_crop_line(self, line: str) -> Optional[Tuple[str, int, int, int, int]]:
        """
        Parse a crop box line and extract image name and coordinates.
        Example: "Crop Box LcQ.png: x: 321, y: 900, width: 193, height: 155"
        Returns: (image_name, x, y, width, height) or None if parsing fails
        """
        # Remove "Crop Box " prefix and ".png" suffix
        pattern = r"Crop Box (.+?)\.png:\s*x:\s*(\d+),\s*y:\s*(\d+),\s*width:\s*(\d+),\s*height:\s*(\d+)"
        match = re.match(pattern, line.strip())
        
        if match:
            image_name = match.group(1)
            x = int(match.group(2))
            y = int(match.group(3))
            width = int(match.group(4))
            height = int(match.group(5))
            return (image_name, x, y, width, height)
        
        return None
    
    def image_name_to_layout_name(self, image_name: str) -> str:
        """
        Convert image name to layout variable name.
        Example: "LcQ" -> "LCQ", "Bell1Freq" -> "Bell1Freq"
        """
        return self.name_mapping.get(image_name, image_name)
    
    def generate_layout_code(self, image_name: str, x: int, y: int, width: int, height: int, 
                           is_child: bool = False, indent_level: int = 1) -> str:
        """
        Generate C++ layout code for a single knob.
        """
        layout_name = self.image_name_to_layout_name(image_name)
        var_name = f"m{layout_name}Layout"
        
        # Base indentation
        indent = "\t" * indent_level
        
        code_lines = [
            f"{indent}{var_name}.inLayout.x = {x} - mPositionInParent.x;",
            f"{indent}{var_name}.inLayout.y = {y} - mPositionInParent.y;",
            f"{indent}{var_name}.inLayout.frameWidth = {width};",
            f"{indent}{var_name}.inLayout.frameHeight = {height};",
            f"{indent}{var_name}.inLayout.ratio = mScale;",
            f"{indent}{var_name}.inLayout.textboxHeight = 0;",
            f"{indent}{var_name}.inLayout.textboxPadding = 0;",
            f"{indent}computeKnobLayout({var_name});",
            ""  # Empty line after each layout
        ]
        
        return "\n".join(code_lines)
    
    def parse_config_file(self, file_path: str) -> List[Tuple[str, int, int, int, int, bool]]:
        """
        Parse the entire configuration file.
        Returns list of (image_name, x, y, width, height, is_child)
        """
        layouts = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):  # Skip empty lines and comments
                        continue
                    
                    # Check if this is a child element
                    is_child = "children" in line.lower()
                    
                    # Parse the crop box data
                    parsed = self.parse_crop_line(line)
                    if parsed:
                        image_name, x, y, width, height = parsed
                        layouts.append((image_name, x, y, width, height, is_child))
                    else:
                        print(f"Warning: Could not parse line {line_num}: {line}")
        
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
        
        return layouts
    
    def generate_all_layouts(self, config_file_path: str, output_file_path: Optional[str] = None) -> str:
        """
        Generate complete C++ layout code from configuration file.
        """
        layouts = self.parse_config_file(config_file_path)
        
        if not layouts:
            return "// No valid layouts found in configuration file"
        
        code_parts = []
        code_parts.append("// Generated layout code")
        code_parts.append("// Auto-generated from crop box configuration")
        code_parts.append("")
        
        for image_name, x, y, width, height, is_child in layouts:
            indent_level = 2 if is_child else 1
            layout_code = self.generate_layout_code(image_name, x, y, width, height, is_child, indent_level)
            code_parts.append(layout_code)
        
        full_code = "\n".join(code_parts)
        
        # Save to file if output path provided
        if output_file_path:
            try:
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(full_code)
                print(f"Layout code saved to: {output_file_path}")
            except Exception as e:
                print(f"Error saving file: {e}")
        
        return full_code
    
    def create_sample_config(self, file_path: str):
        """
        Create a sample configuration file with the provided data.
        """
        sample_data = """Crop Box GainKnob.png: x: 15, y: 495, width: 160, height: 193
Crop Box LcQ.png: x: 321, y: 900, width: 193, height: 155
Crop Box LcFreq.png: x: 138, y: 802, width: 193, height: 159
Crop Box Bell1Freq.png: x: 457, y: 741, width: 188, height: 159
Crop Box Bell1Gain.png: x: 658, y: 898, width: 182, height: 157
Crop Box Bell2Freq.png: x: 933, y: 805, width: 178, height: 167
Crop Box Bell2Gain.png: x: 1111, y: 895, width: 175, height: 161
Crop Box Bell2Q.png: x: 1260, y: 713, width: 175, height: 169
Crop Box HSFreq.png: x: 1430, y: 889, width: 167, height: 166
Crop Box HSGain.png: x: 1434, y: 706, width: 158, height: 165
Crop Box HSq.png: x: 1627, y: 890, width: 176, height: 162
Crop Box outputGain.png: x: 1725, y: 507, width: 186, height: 164"""
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(sample_data)
            print(f"Sample configuration created: {file_path}")
        except Exception as e:
            print(f"Error creating sample file: {e}")


def main():
    """
    Main function to demonstrate usage
    """
    generator = LayoutGenerator()
    
    # Create sample config file
    config_file = "crop_config.txt"
    output_file = "generated_layout.cpp"
    
    print("Layout Generator - Crop Box to C++ Layout Converter")
    print("=" * 50)
    
    # Check if config file exists, if not create sample
    if not os.path.exists(config_file):
        print(f"Creating sample configuration file: {config_file}")
        generator.create_sample_config(config_file)
    
    # Generate layout code
    print(f"Generating layout code from: {config_file}")
    generated_code = generator.generate_all_layouts(config_file, output_file)
    
    print("\nGenerated C++ Layout Code:")
    print("-" * 30)
    print(generated_code)
    
    # Interactive mode
    print("\nInteractive Mode:")
    print("Enter crop box lines manually (press Enter twice to finish):")
    manual_lines = []
    while True:
        line = input("> ")
        if not line:
            break
        manual_lines.append(line)
    
    if manual_lines:
        print("\nProcessing manual input:")
        for line in manual_lines:
            parsed = generator.parse_crop_line(line)
            if parsed:
                image_name, x, y, width, height = parsed
                code = generator.generate_layout_code(image_name, x, y, width, height)
                print(code)


if __name__ == "__main__":
    main()