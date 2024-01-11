from random import randrange
import cv2

class Person:
    def __init__(self, rectangle: tuple, frame):
        self.id = 0
        self.color = (randrange(255), randrange(255), randrange(255))
        self.rectangle = rectangle
        self.template = self.getRoi(frame)
        self.state = True
        self.frame = frame

    def updateRectangle(self, newRectangle: tuple):
        self.rectangle = newRectangle

    def topLeft(self):
        return (self.rectangle[0], self.rectangle[1])

    def bottonRight(self):
        x, y, w, h = self.rectangle
        return (x + w, y + h)

    def calculate_center(self):
        x, y, w, h = self.rectangle
        return (x + w // 2, y + h // 2)

    def drawRectangle(self, frame):
        cv2.rectangle(frame, self.topLeft(), self.bottonRight(), self.color, 2)
        cv2.putText(frame, f'Person {self.id}', (self.rectangle[0], self.rectangle[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, self.color, 2)

    def getRoi(self, frame):
        x, y, w, h = self.rectangle
        return frame[y:y + h, x:x + w]



    def find_matching(self, frame):
        h, w, _ = self.template.shape[:]
        res = cv2.matchTemplate(frame, self.template, cv2.TM_CCOEFF_NORMED)
        # Get the best match position
        _, _, _, max_loc = cv2.minMaxLoc(res)
        # Get the top-left position
        x, y = max_loc

        self.frame = frame
        self.updateRectangle((x, y, w, h))
        self.drawRectangle(frame)
        cv2.circle(frame, (x, y), 3, (0, 0, 255), 2)

        #intentamos usar template matching de forma que solo analice una región donde estaba la persona en el anterior frame.

    """
    def find_matching(self, frame):
        # Obtener las dimensiones de la plantilla redimensionada
        h, w, _ = self.template.shape[:]

        # Definir la región de búsqueda basada en las coordenadas anteriores
        search_x, search_y, search_w, search_h = self.rectangle.x, self.rectangle.y, self.rectangle.w, self.rectangle.h
        search_area, template_resized = self.getRoi2(frame)

        # Aplicar coincidencia de plantillas en la región de búsqueda
        res = cv2.matchTemplate(search_area, template_resized, cv2.TM_CCOEFF_NORMED)

        # Restaurar las dimensiones originales al actualizar el rectángulo asociado a la plantilla
        top_left, bottom_right = self.updateRectangle(Rectangle(search_x, search_y, search_w, search_h))

        # Dibujar un rectángulo alrededor de la región coincidente
        cv2.rectangle(frame, top_left, bottom_right, self.color, 2)

        # Añadir un texto con el identificador de persona
        cv2.putText(frame, f'P {self.id}', (self.rectangle.x, self.rectangle.y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, self.color, 2)

        # Dibujar un círculo en la esquina superior izquierda de la región coincidente
        cv2.circle(frame, top_left, 3, (0, 0, 255), 2)

        return frame
    """
