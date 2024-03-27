from core.Buffer import ImageBuffer,TextImageBuffer,RectBuffer

class MemoryEngine():
    img_buffer = ImageBuffer
    text_buffer = TextImageBuffer
    rect_buffer = RectBuffer
    def __init__(self) -> None:
        self.buffer = ImageBuffer()
        self.text_buffer = TextImageBuffer()
        self.rect_buffer = RectBuffer()

    def get_img_buffer(self) -> ImageBuffer:
        return self.buffer
    
    def get_txt_buffer(self) -> TextImageBuffer:
        return self.text_buffer
    
    def get_rect_buffer(self) -> RectBuffer:
        return self.rect_buffer
        
MEMORY_ENGINE = MemoryEngine()