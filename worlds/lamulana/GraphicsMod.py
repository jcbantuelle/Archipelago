from PIL import Image
import io
import Utils

class GraphicsMod:

    def __init__(self, options):
        file_path = Utils.user_path('01effect.png')
        self.graphics_file = Image.open(file_path)
        self.options = options

    def apply_mods(self):
        custom_graphics_path = Utils.user_path('worlds/lamulana/01effect-custom.png')
        custom_graphics_file = Image.open(custom_graphics_path)

        self.new_graphics_file = Image.new(self.graphics_file.mode, (self.graphics_file.width, self.graphics_file.height + custom_graphics_file.height))
        self.new_graphics_file.paste(self.graphics_file, (0,0))
        self.new_graphics_file.paste(custom_graphics_file, (0, self.graphics_file.height))

    def write_file(self):
        png_bytes = io.BytesIO()
        self.new_graphics_file.save(png_bytes, format='PNG')

        return png_bytes.getvalue()
