import re
import urllib.request
from datetime import datetime, timedelta

import face_recognition

from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect
from PySide6.QtGui import QImage, QColor, QPixmap, QIcon, QPainter, QBrush, QWindow
from PySide6.QtCore import Qt, QRect


class ModIcon:
    """Modify icon size or color.
    
    Parameters
    ---
    image: QImage
        The image to be modified.
    """
    def __init__(self, image: QImage):
        self._img: QImage = image

    def set_size(self, size: int):
        """Modifies existing ModIcon object with new size
        
        Parameters
        ----
        size: int
            The new size to use.

        :returns: Self
        :rtype: ModIcon
        :raise Exception: If set to be set is greater than icon default size.
        """
        img_size = self._img.size()
        
        if size > img_size.width() or size > img_size.height():
            raise Exception('Set size below or equal to existing size.')

        self._img = self._img.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        return self

    def set_color(self, color: str):
        """Modifies existing ModIcon object with new size
        
        Parameters
        ----
        color: str
            The new color to use.

        :returns: Self
        :rtype: ModIcon
        """
        color = QColor(color)
        for x in range(self._img.height()):
            for y in range(self._img.width()):
                color.setAlpha(self._img.pixelColor(x, y).alpha())
                self._img.setPixelColor(x, y, color)

        return self

    def get_pixmap(self) -> QPixmap:
        return QPixmap.fromImage(self._img)

    def get_icon(self) -> QIcon:
        return QIcon(self.get_pixmap())


def is_email_address(text: str):
    return re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)


def wait(msec: int) -> None:
    """ Wait for a certain amount of time and continue execution of specific process """

    end = datetime.now() + timedelta(milliseconds=msec)
    while datetime.now() < end:
        QApplication.processEvents()


def rounded_image(image: QImage, size=32):
    """Make rounded image from image.

    Parameters
    ---
    image: QImage
        The image to be converted into rounded form
    size: int
        The size to use. (default 32) 

    Returns
    ----
    Image as QPixmap 
    """
  
    # convert image to 32-bit ARGB (adds an alpha
    # channel ie transparency factor):
    image.convertToFormat(QImage.Format_ARGB32)
  
    # Crop image to a square:
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
    )
       
    image = image.copy(rect)
  
    # Create the output image with the same dimensions 
    # and an alpha channel and make it completely transparent:
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)
  
    # Create a texture brush and paint a circle 
    # with the original image onto the output image:
    brush = QBrush(image)
  
    # Paint the output image
    painter = QPainter(out_img)
    painter.setBrush(brush)
  
    # Don't draw an outline
    painter.setPen(Qt.NoPen)
  
    # drawing circle
    painter.drawEllipse(0, 0, imgsize, imgsize)
  
    # closing painter event
    painter.end()
  
    # Convert the image to a pixmap and rescale it. 
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
  
    # return back the pixmap data
    return pm


def drop_shadow(parent, color='#000', alpha=0.2, blur=25, x=.5, y=3):
    """ Create box shadow

    """

    color = QColor(color)
    color.setAlphaF(alpha)

    ds = QGraphicsDropShadowEffect(parent)
    ds.setBlurRadius(blur)
    ds.setXOffset(x)
    ds.setYOffset(y)
    ds.setColor(color)
    return ds


def verify_face(known_photo_url):
    urllib.request.urlretrieve(known_photo_url, "temp/known.jpg")

    try:
        known_photo = face_recognition.load_image_file("temp/known.jpg")
        known_encoding = face_recognition.face_encodings(known_photo)[0]

        unknown_photo = face_recognition.load_image_file("temp/unknown.jpg")
        unknown_encoding = face_recognition.face_encodings(unknown_photo)[0]

        results = face_recognition.compare_faces([known_encoding], unknown_encoding)

        if results[0] == True:
            return 
    except:
        pass
        
    return False
