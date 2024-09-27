from .slimeface import detectRGB as c_detectRGB
import warnings

def detectRGB(w: int, h: int, img: bytes):
    '''
    @param width: int, image width
    @param height: int, image height
    @param bytes: bytes, image RGB date in bytes
    
    @return: 
        bboxe_and_confs: list[list[int]], each inner list is of form [x, y, w, h, confidence]
    '''
    if h > 960 or w > 960:
        warnings.warn(f'Image size ({w}, {h}) is too large, it may cause detection performance degradation.')
    return c_detectRGB(w, h, img)
