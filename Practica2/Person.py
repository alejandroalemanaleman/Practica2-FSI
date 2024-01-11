from random import randrange
import cv2

class Person:
    def __init__(self, x, y, w, h, frame):
        self.id = 0
        self.color = (randrange(255), randrange(255), randrange(255))
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = self.calculate_center(x, y, w, h)
        self.template = self.getRoi(frame)

    def updateRectangle(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = self.calculate_center(x, y, w, h)

    def topLeft(self):
        return (self.x, self.y)

    def bottonRight(self):
        return (self.x + self.w, self.y + self.h)

    def calculate_center(self, x, y, w, h):
        return (x + w // 2, y + h // 2)

    def drawRectangle(self, frame):
        cv2.rectangle(frame, self.topLeft(), self.bottonRight(), self.color, 2)
        cv2.putText(frame, f'Person {self.id}', (self.x, self.y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, self.color, 2)

    def updateTemplate(self, frame):
        self.template = self.getRoi(frame)

    def getRoi(self, frame):
        y = self.y
        x = self.x
        h = self.h
        w = self.w
        return frame[y:y + h, x:x + w]



    def find_matching(self, frame):
        h, w, _ = self.template.shape[:]
        res = cv2.matchTemplate(frame, self.template, cv2.TM_CCOEFF_NORMED)
        # Get the best match position
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # Get the top-left position
        top_left = max_loc
        # Get the bottom-right position
        bottom_right = (top_left[0] + w, top_left[1] + h)

        self.updateRectangle(top_left[0], top_left[1], w, h)
        cv2.rectangle(frame, top_left, bottom_right, self.color, 2)
        self.drawRectangle(frame)
        cv2.circle(frame, top_left, 3, (0,0,255), 2)

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
