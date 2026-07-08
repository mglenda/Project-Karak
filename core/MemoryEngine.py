from core.Buffer import ImageBuffer,TextImageBuffer,FittedTextImageBuffer,RectBuffer

class MemoryEngine():
    img_buffer = ImageBuffer
    text_buffer = TextImageBuffer
    fitted_text_buffer = FittedTextImageBuffer
    rect_buffer = RectBuffer
    def __init__(self) -> None:
        self.buffer = ImageBuffer()
        self.text_buffer = TextImageBuffer()
        self.fitted_text_buffer = FittedTextImageBuffer()
        self.rect_buffer = RectBuffer()

    def get_img_buffer(self) -> ImageBuffer:
        return self.buffer
    
    def get_txt_buffer(self) -> TextImageBuffer:
        return self.text_buffer

    def get_fitted_txt_buffer(self) -> FittedTextImageBuffer:
        return self.fitted_text_buffer
    
    def get_rect_buffer(self) -> RectBuffer:
        return self.rect_buffer
        
MEMORY_ENGINE = MemoryEngine()
