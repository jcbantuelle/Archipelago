from PIL import Image
import io
import Utils

class GraphicsMod:

    def __init__(self, options):
        file_path = Utils.user_path('01effect.png')
        self.graphics_file = Image.open(file_path)
        self.original_graphics_height = self.graphics_file.height
        self.options = options

    def apply_mods(self):
        custom_graphics_path = Utils.user_path('worlds/lamulana/01effect-custom.png')
        custom_graphics_file = Image.open(custom_graphics_path)

        self.graphics_file = self.graphics_file.resize((self.graphics_file.width, self.graphics_file.height + custom_graphics_file.height))
        self.graphics_file.paste(custom_graphics_file, (0, self.original_graphics_height))

    def write_file(self):
        png_bytes = io.BytesIO()
        self.graphics_file.save(png_bytes, format='PNG')

        return png_bytes.getvalue()
